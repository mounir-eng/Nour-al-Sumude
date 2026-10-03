-- Run once in the SAME Supabase project that contains student_profiles.
-- Non-destructive: keeps existing rows and row-level-security policies.
alter table public.student_profiles add column if not exists email text;
alter table public.student_profiles add column if not exists grades smallint[];
update public.student_profiles set grades = array[grade] where grades is null;

-- Update actual server receipt time on every Android/web upsert.
create or replace function public.set_progress_receipt_time()
returns trigger language plpgsql set search_path = public as $$
begin
  new.server_updated_at := now();
  return new;
end;
$$;
drop trigger if exists progress_receipt_time on public.progress_snapshots;
create trigger progress_receipt_time before insert or update on public.progress_snapshots
for each row execute function public.set_progress_receipt_time();

grant select on public.student_profiles to authenticated;
grant select, insert, update on public.progress_snapshots to authenticated;
grant all on public.student_profiles, public.progress_snapshots to service_role;
-- RLS remains enabled. Never disable it to debug registration.
