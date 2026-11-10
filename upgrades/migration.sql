-- Additive feature expansion: no existing documents or credentials changed.
alter table ict12_private.documents drop constraint documents_collection_check;
alter table ict12_private.documents add constraint documents_collection_check
 check(collection in ('users','sessions','exams','attempts','violations','rate','classes','assignments','preferences'));
create or replace function ict12_private.enforce_assignment_deadline()
returns trigger language plpgsql set search_path = '' as $$
begin
 if new.collection='attempts' and new.data->>'assignmentClose' is not null then
  if new.data->>'status' in ('active','submitted') and
    (extract(epoch from clock_timestamp())*1000 >= (new.data->>'assignmentClose')::numeric) then
   raise exception 'Đã quá hạn bài giao. Không nhận bài nộp sau hạn.' using errcode='42501';
  end if;
  if TG_OP='INSERT' and extract(epoch from clock_timestamp())*1000 < (new.data->>'assignmentOpen')::numeric then
   raise exception 'Bài giao chưa mở.' using errcode='42501';
  end if;
 end if;
 return new;
end;$$;
revoke all on function ict12_private.enforce_assignment_deadline() from public,anon,authenticated;
create trigger ict12_assignment_deadline before insert or update on ict12_private.documents
 for each row execute function ict12_private.enforce_assignment_deadline();
