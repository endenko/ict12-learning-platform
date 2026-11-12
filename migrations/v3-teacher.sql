-- ICT12 v3 (teacher portal). Additive and non-destructive: no rows are changed or removed.
-- 1) new document collections
alter table ict12_private.documents drop constraint documents_collection_check;
alter table ict12_private.documents add constraint documents_collection_check
 check(collection in ('users','sessions','exams','attempts','violations','rate','classes','assignments','preferences',
                      'notes','announcements','questions','activity','presence'));
create index if not exists ict12_document_class on ict12_private.documents ((data->>'className'));

-- 2) ownership helpers (teacher owns a class when classes.data.ownerId = teacher id)
create or replace function ict12_private.owns_class(p_actor text, p_class text, p_active boolean)
returns boolean language sql stable set search_path = '' as $$
 select p_class is not null and p_class<>'' and exists(select 1 from ict12_private.documents
  where collection='classes' and data->>'name'=p_class and data->>'ownerId'=p_actor
    and (not p_active or coalesce((data->>'disabled')::boolean,false)=false))
$$;
revoke all on function ict12_private.owns_class(text,text,boolean) from public,anon,authenticated;

-- 3) RPC-level ownership check for every teacher write (defence in depth behind the API checks)
create or replace function ict12_private.scoped_check(p_actor text, p_collection text, p_id text, p_doc jsonb)
returns void language plpgsql stable set search_path = '' as $$
declare t jsonb; old jsonb; ex jsonb;
begin
 select data into t from ict12_private.documents where collection='users' and id=p_actor;
 if t is null or t->>'role' is distinct from 'teacher' or coalesce((t->>'locked')::boolean,false) then
  raise exception 'Tài khoản giáo viên không hợp lệ.' using errcode='42501'; end if;
 select data into old from ict12_private.documents where collection=p_collection and id=p_id;
 if p_doc->>'id' is distinct from p_id then raise exception 'Mã tài liệu không khớp.' using errcode='42501'; end if;
 if p_collection='users' then
  if p_doc->>'role' is distinct from 'student' or not ict12_private.owns_class(p_actor,p_doc->>'className',true) then
   raise exception 'Học sinh phải thuộc lớp của bạn.' using errcode='42501'; end if;
  if old is not null and (old->>'role' is distinct from 'student' or not ict12_private.owns_class(p_actor,old->>'className',false)) then
   raise exception 'Không có quyền với học sinh này.' using errcode='42501'; end if;
 elsif p_collection='classes' then
  if p_doc->>'ownerId' is distinct from p_actor or (old is not null and old->>'ownerId' is distinct from p_actor) then
   raise exception 'Không có quyền với lớp này.' using errcode='42501'; end if;
 elsif p_collection in ('assignments','announcements') then
  if p_doc->>'ownerId' is distinct from p_actor or (old is not null and old->>'ownerId' is distinct from p_actor)
   or not exists(select 1 from ict12_private.documents where collection='classes' and id=p_doc->>'classId'
                 and data->>'ownerId'=p_actor and data->>'name'=p_doc->>'className') then
   raise exception 'Không có quyền với lớp này.' using errcode='42501'; end if;
  if p_collection='assignments' then
   select data into ex from ict12_private.documents where collection='exams' and id=p_doc->>'examId';
   if ex is not null and ex->>'ownerId' is not null and ex->>'ownerId'<>p_actor then
    raise exception 'Không thể giao đề của giáo viên khác.' using errcode='42501'; end if;
  end if;
 elsif p_collection='notes' then
  if p_doc->>'authorId' is distinct from p_actor or (old is not null and old->>'authorId' is distinct from p_actor)
   or not exists(select 1 from ict12_private.documents s where s.collection='users' and s.id=p_doc->>'userId'
                 and s.data->>'role'='student' and ict12_private.owns_class(p_actor,s.data->>'className',false)) then
   raise exception 'Không có quyền ghi chú cho học sinh này.' using errcode='42501'; end if;
 elsif p_collection in ('questions','activity') then
  if p_doc->>'userId' is distinct from p_actor or (old is not null and old->>'userId' is distinct from p_actor) then
   raise exception 'Không có quyền với dữ liệu này.' using errcode='42501'; end if;
 elsif p_collection='exams' then
  if p_doc->>'ownerId' is distinct from p_actor or p_id not like 'gv-%' or (old is not null and old->>'ownerId' is distinct from p_actor) then
   raise exception 'Không có quyền với đề này.' using errcode='42501'; end if;
 else
  raise exception 'Giáo viên không được ghi dữ liệu này.' using errcode='42501';
 end if;
end;$$;
revoke all on function ict12_private.scoped_check(text,text,text,jsonb) from public,anon,authenticated;

-- 4) access(): same signature; adds list_in and scoped_put, everything else unchanged
create or replace function ict12_private.access(p_secret text, p_action text, p_collection text, p_id text default '', p_data jsonb default '{}'::jsonb, p_version integer default null)
returns jsonb language plpgsql security definer set search_path = '' as $function$
declare result jsonb; v integer; bucket jsonb; count_value integer; until_ms bigint; now_ms bigint; doc jsonb;
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
 elsif p_action='list_in' then
  if p_id not in ('userId','classId','className','ownerId','authorId') then raise exception 'Invalid operation'; end if;
  select coalesce(jsonb_agg(data || jsonb_build_object('_version',version)),'[]'::jsonb) into result from ict12_private.documents
   where collection=p_collection and data->>p_id in (select jsonb_array_elements_text(coalesce(p_data->'values','[]'::jsonb)));
 elsif p_action in ('put','scoped_put') then
  doc=p_data;
  if p_action='scoped_put' then doc=p_data->'doc'; perform ict12_private.scoped_check(p_data->>'actor',p_collection,p_id,doc); end if;
  if p_version is null then
   insert into ict12_private.documents(collection,id,data) values(p_collection,p_id,doc) on conflict(collection,id) do nothing returning version into v;
  else
   update ict12_private.documents set data=doc,version=version+1,updated_at=now() where collection=p_collection and id=p_id and version=p_version returning version into v;
  end if;
  if v is null then raise exception 'Conflict' using errcode='PT409';end if;
  result=doc || jsonb_build_object('_version',v);
 elsif p_action='start' and p_collection='attempts' then
  perform pg_catalog.pg_advisory_xact_lock(pg_catalog.hashtext(p_data->>'userId'));
  if exists(select 1 from ict12_private.documents where collection='attempts' and data->>'userId'=p_data->>'userId' and data->>'status'='active') then raise exception 'Bạn còn một bài đang làm, hãy tiếp tục bài đó'; end if;
  if (select count(*) from ict12_private.documents where collection='attempts' and data->>'userId'=p_data->>'userId' and data->>'examId'=p_data->>'examId') >= (p_data->>'attemptLimit')::integer then raise exception 'Đã hết số lượt làm bài'; end if;
  insert into ict12_private.documents(collection,id,data) values(p_collection,p_id,p_data);
  result=p_data||jsonb_build_object('_version',1);
 else raise exception 'Invalid operation';end if;
 return result;
end;$function$;
revoke all on function ict12_private.access(text,text,text,text,jsonb,integer) from public;
grant execute on function ict12_private.access(text,text,text,text,jsonb,integer) to anon;
