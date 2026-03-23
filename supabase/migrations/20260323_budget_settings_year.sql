-- Add year column to budget_settings for per-year rate/cost configuration
-- Existing row gets year=2026 (current active year)

ALTER TABLE public.budget_settings
  ADD COLUMN year int NOT NULL DEFAULT 2026;

-- Update the unique constraint from (calendar_id) to (calendar_id, year)
ALTER TABLE public.budget_settings
  DROP CONSTRAINT budget_settings_calendar_id_key;

ALTER TABLE public.budget_settings
  ADD CONSTRAINT budget_settings_calendar_year_key UNIQUE (calendar_id, year);

-- Create index for faster year-based lookups
CREATE INDEX idx_budget_settings_calendar_year
  ON public.budget_settings (calendar_id, year);
