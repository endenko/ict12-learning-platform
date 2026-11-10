create schema if not exists ict12_private;
revoke all on schema ict12_private from public;
create table ict12_private.documents (
 collection text not null, id text not null, data jsonb not null,
 version integer not null default 1, updated_at timestamptz not null default now(),
 primary key(collection,id), check(collection in ('users','sessions','exams','attempts','violations','rate'))
);
alter table ict12_private.documents enable row level security;
revoke all on ict12_private.documents from public,anon,authenticated;
create index ict12_document_owner on ict12_private.documents ((data->>'userId'));
create table ict12_private.config (secret_hash text not null);
alter table ict12_private.config enable row level security;
revoke all on ict12_private.config from public,anon,authenticated;
create function ict12_private.access(p_secret text, p_action text, p_collection text, p_id text default '', p_data jsonb default '{}'::jsonb, p_version integer default null)
returns jsonb language plpgsql security definer set search_path = '' as $$
declare result jsonb; v integer;
begin
 if not exists(select 1 from ict12_private.config where secret_hash=pg_catalog.encode(pg_catalog.sha256(pg_catalog.convert_to(p_secret,'UTF8')),'hex')) then raise exception 'Access denied' using errcode='42501'; end if;
 if p_action='get' then
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
revoke all on function ict12_private.access(text,text,text,text,jsonb,integer) from public;
grant usage on schema ict12_private to anon;
grant execute on function ict12_private.access(text,text,text,text,jsonb,integer) to anon;
create function public.ict12_access(p_secret text, p_action text, p_collection text, p_id text default '', p_data jsonb default '{}'::jsonb, p_version integer default null)
returns jsonb language sql security invoker set search_path = '' as $$select ict12_private.access(p_secret,p_action,p_collection,p_id,p_data,p_version);$$;
revoke all on function public.ict12_access(text,text,text,text,jsonb,integer) from public,authenticated;
grant execute on function public.ict12_access(text,text,text,text,jsonb,integer) to anon;
