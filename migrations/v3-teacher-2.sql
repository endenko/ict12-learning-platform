-- ICT12 v3 follow-up (additive): a teacher may only create a NEW class whose name is not already used by any account,
-- so a class name can never be used to take over existing students.
create or replace function ict12_private.scoped_check_class_name(p_name text)
returns boolean language sql stable set search_path = '' as $$
 select not exists(select 1 from ict12_private.documents where collection='users' and data->>'className'=p_name)
$$;
revoke all on function ict12_private.scoped_check_class_name(text) from public,anon,authenticated;
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
  if old is null and not ict12_private.scoped_check_class_name(p_doc->>'name') then
   raise exception 'Tên lớp đang được dùng cho tài khoản khác.' using errcode='42501'; end if;
  if old is not null and old->>'name' is distinct from p_doc->>'name' then
   raise exception 'Không đổi tên lớp.' using errcode='42501'; end if;
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
