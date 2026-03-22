create table if not exists public.carry_forward_overrides (
  id uuid primary key default gen_random_uuid(),
  calendar_id text not null references public.calendars(id) on delete cascade,
  year int not null,
  amount numeric not null default 0,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (calendar_id, year)
);

alter table public.carry_forward_overrides enable row level security;

create policy "Users can manage their own carry-forward overrides"
  on public.carry_forward_overrides
  for all
  using (
    calendar_id in (
      select u.calendar_id from public.users u
      where u.google_id::text = auth.uid()::text
         or lower(u.email::text) = lower(coalesce(auth.jwt() ->> 'email', ''))
    )
  )
  with check (
    calendar_id in (
      select u.calendar_id from public.users u
      where u.google_id::text = auth.uid()::text
         or lower(u.email::text) = lower(coalesce(auth.jwt() ->> 'email', ''))
    )
  );
