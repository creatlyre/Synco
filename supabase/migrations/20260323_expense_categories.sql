-- Expense categories table
create table if not exists public.expense_categories (
  id uuid primary key default gen_random_uuid(),
  calendar_id text not null references public.calendars(id) on delete cascade,
  name text not null,
  color text not null,
  is_preset boolean not null default false,
  sort_order int not null default 0,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (calendar_id, name)
);

-- RLS disabled: app uses service-role key without JWT
alter table public.expense_categories disable row level security;

-- Add category_id to expenses table
alter table public.expenses add column if not exists category_id uuid references public.expense_categories(id) on delete set null;
