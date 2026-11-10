-- Additive behaviors only; no records or credentials deleted/rewritten.
create or replace function ict12_private.access(p_secret text, p_action text, p_collection text, p_id text default '', p_data jsonb default '{}'::jsonb, p_version integer default null)
returns jsonb language plpgsql security definer set search_path = '' as $$
declare result jsonb; v integer; bucket jsonb; count_value integer; until_ms bigint; now_ms bigint;
begin
 if not exists(select 1 from ict12_private.config where secret_hash=pg_catalog.encode(pg_catalog.sha256(pg_catalog.convert_to(p_secret,'UTF8')),'hex')) then raise exception 'Access denied' using errcode='42501'; end if;
 if p_action='throttle' and p_collection='rate' then
  perform pg_catalog.pg_advisory_xact_lock(pg_catalog.hashtext('throttle:'||p_id));
  now_ms=(extract(epoch from clock_timestamp())*1000)::bigint;
  select data into bucket from ict12_private.documents where collection='rate' and id=p_id;
  until_ms=coalesce((bucket->>'until')::bigint,0);
  count_value=coalesce((bucket->>'count')::integer,0);
  if until_ms<=now_ms then count_value=0; until_ms=now_ms+least(86400000,greatest(1000,(p_data->>'windowMs')::integer)); end if;
  if count_value >= greatest(1,(p_data->>'limit')::integer) then
   return jsonb_build_object('allowed',false,'retryAfter',greatest(1,ceil((until_ms-now_ms)/1000.0)));
  end if;
  insert into ict12_private.documents(collection,id,data) values('rate',p_id,jsonb_build_object('id',p_id,'count',count_value+1,'until',until_ms))
   on conflict(collection,id) do update set data=excluded.data,version=ict12_private.documents.version+1,updated_at=now();
  return jsonb_build_object('allowed',true);
 elsif p_action='get' then
  select data || jsonb_build_object('_version',version) into result from ict12_private.documents where collection=p_collection and id=p_id;
 elsif p_action='list' then
  select coalesce(jsonb_agg(data || jsonb_build_object('_version',version)),'[]'::jsonb) into result from ict12_private.documents where collection=p_collection and (p_id='' or data->>'userId'=p_id);
 elsif p_action='put' then
  if p_version is null then
   insert into ict12_private.documents(collection,id,data) values(p_collection,p_id,p_data) on conflict(collection,id) do nothing returning version into v;
  else
   update ict12_private.documents set data=p_data,version=version+1,updated_at=now() where collection=p_collection and id=p_id and version=p_version returning version into v;
  end if;
  if v is null then raise exception 'Conflict' using errcode='40001';end if;
  result=p_data || jsonb_build_object('_version',v);
 elsif p_action='start' and p_collection='attempts' then
  perform pg_catalog.pg_advisory_xact_lock(pg_catalog.hashtext(p_data->>'userId'));
  if exists(select 1 from ict12_private.documents where collection='attempts' and data->>'userId'=p_data->>'userId' and data->>'status'='active') then raise exception 'Bạn còn một bài đang làm, hãy tiếp tục bài đó'; end if;
  if (select count(*) from ict12_private.documents where collection='attempts' and data->>'userId'=p_data->>'userId' and data->>'examId'=p_data->>'examId') >= (p_data->>'attemptLimit')::integer then raise exception 'Đã hết số lượt làm bài'; end if;
  insert into ict12_private.documents(collection,id,data) values(p_collection,p_id,p_data);
  result=p_data||jsonb_build_object('_version',1);
 else raise exception 'Invalid operation';end if;
 return result;
end;$$;

create or replace function ict12_private.enforce_assignment_deadline()
returns trigger language plpgsql set search_path='' as $$
declare assignment jsonb; member jsonb; now_ms numeric;
begin
 if new.collection<>'attempts' or new.data->>'assignmentId' is null then return new; end if;
 now_ms=extract(epoch from clock_timestamp())*1000;
 if new.data->>'status' in ('active','submitted') then
  select data into member from ict12_private.documents where collection='users' and id=new.data->>'userId' for share;
  if member is null or member->>'className' is distinct from new.data->>'className' then
   raise exception 'Bạn không còn thuộc lớp nhận bài giao.' using errcode='42501';
  end if;
  if new.data->>'assignmentClose' is null or now_ms >= (new.data->>'assignmentClose')::numeric then
   raise exception 'Đã quá hạn bài giao. Không nhận bài nộp sau hạn.' using errcode='42501';
  end if;
 end if;
 if TG_OP='INSERT' then
  select data into assignment from ict12_private.documents where collection='assignments' and id=new.data->>'assignmentId' for share;
  if assignment is null or (assignment->>'disabled')::boolean or assignment->>'className' is distinct from member->>'className' or assignment->>'examId' is distinct from new.data->>'examId' then
   raise exception 'Bài giao không hợp lệ với lớp của bạn.' using errcode='42501';
  end if;
  if now_ms < (assignment->>'opensAt')::numeric then raise exception 'Bài giao chưa mở.' using errcode='42501'; end if;
  if new.data->>'assignmentOpen' is distinct from assignment->>'opensAt' or new.data->>'assignmentClose' is distinct from assignment->>'closesAt' then
   raise exception 'Lịch bài giao không khớp.' using errcode='42501';
  end if;
 elsif new.data->>'assignmentOpen' is distinct from old.data->>'assignmentOpen' or new.data->>'assignmentClose' is distinct from old.data->>'assignmentClose' or new.data->>'assignmentId' is distinct from old.data->>'assignmentId' then
  raise exception 'Không được thay lịch đã chốt của bài làm.' using errcode='42501';
 end if;
 return new;
end;$$;
revoke all on function ict12_private.enforce_assignment_deadline() from public,anon,authenticated;
