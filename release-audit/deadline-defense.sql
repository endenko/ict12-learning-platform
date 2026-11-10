create or replace function ict12_private.enforce_assignment_deadline()
returns trigger language plpgsql set search_path='' as $$
declare assignment jsonb; member jsonb; now_ms numeric;
begin
 if new.collection<>'attempts' then return new; end if;
 now_ms=extract(epoch from clock_timestamp())*1000;
 if new.data->>'status' in ('active','submitted') and new.data->>'assignmentClose' is not null and now_ms >= (new.data->>'assignmentClose')::numeric then raise exception 'Đã quá hạn bài giao. Không nhận bài nộp sau hạn.' using errcode='42501'; end if;
 if TG_OP='UPDATE' and (old.data->>'assignmentId' is not null or new.data->>'assignmentId' is not null) and (new.data->>'assignmentOpen' is distinct from old.data->>'assignmentOpen' or new.data->>'assignmentClose' is distinct from old.data->>'assignmentClose' or new.data->>'assignmentId' is distinct from old.data->>'assignmentId') then raise exception 'Không được thay lịch đã chốt của bài làm.' using errcode='42501'; end if;
 if new.data->>'assignmentId' is null then return new; end if;
 if new.data->>'status' in ('active','submitted') then
  select data into member from ict12_private.documents where collection='users' and id=new.data->>'userId' for share;
  if member is null or coalesce((member->>'locked')::boolean,false) or member->>'className' is distinct from new.data->>'className' then
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
