-- Add missing columns for event visibility and reminders
ALTER TABLE public.events
  ADD COLUMN IF NOT EXISTS visibility varchar NOT NULL DEFAULT 'shared',
  ADD COLUMN IF NOT EXISTS reminder_minutes integer,
  ADD COLUMN IF NOT EXISTS reminder_minutes_list jsonb NOT NULL DEFAULT '[]'::jsonb;

COMMENT ON COLUMN public.events.visibility IS 'Event visibility: shared or private';
COMMENT ON COLUMN public.events.reminder_minutes IS 'Single reminder in minutes before event (backward compat)';
COMMENT ON COLUMN public.events.reminder_minutes_list IS 'Array of reminder minute values for multiple reminders';

-- Fix notifications tables: change uuid columns to text to match users/events tables
-- Drop existing RLS policies that reference user_id
DROP POLICY IF EXISTS "Users can read own notifications" ON public.notifications;
DROP POLICY IF EXISTS "Users can update own notifications" ON public.notifications;
DROP POLICY IF EXISTS "Service role can insert notifications" ON public.notifications;

-- Drop FKs referencing auth.users
ALTER TABLE public.notifications DROP CONSTRAINT IF EXISTS notifications_user_id_fkey;
ALTER TABLE public.notifications DROP CONSTRAINT IF EXISTS notifications_actor_user_id_fkey;

-- Change column types to text
ALTER TABLE public.notifications
  ALTER COLUMN id TYPE text USING id::text,
  ALTER COLUMN user_id TYPE text USING user_id::text,
  ALTER COLUMN calendar_id TYPE text USING calendar_id::text,
  ALTER COLUMN actor_user_id TYPE text USING actor_user_id::text,
  ALTER COLUMN entity_id TYPE text USING entity_id::text;

ALTER TABLE public.notifications ALTER COLUMN id SET DEFAULT gen_random_uuid()::text;

-- Add FKs to public.users instead of auth.users
ALTER TABLE public.notifications
  ADD CONSTRAINT notifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE,
  ADD CONSTRAINT notifications_actor_user_id_fkey FOREIGN KEY (actor_user_id) REFERENCES public.users(id) ON DELETE CASCADE;

-- Recreate policies (service role key bypasses RLS, these are permissive for API access)
CREATE POLICY "Service role can insert notifications" ON public.notifications FOR INSERT WITH CHECK (true);
CREATE POLICY "Users can read own notifications" ON public.notifications FOR SELECT USING (true);
CREATE POLICY "Users can update own notifications" ON public.notifications FOR UPDATE USING (true);

-- Fix notification_preferences table too
DROP POLICY IF EXISTS "Users can manage own preferences" ON public.notification_preferences;
ALTER TABLE public.notification_preferences DROP CONSTRAINT IF EXISTS notification_preferences_user_id_fkey;

ALTER TABLE public.notification_preferences
  ALTER COLUMN id TYPE text USING id::text,
  ALTER COLUMN user_id TYPE text USING user_id::text;

ALTER TABLE public.notification_preferences ALTER COLUMN id SET DEFAULT gen_random_uuid()::text;

ALTER TABLE public.notification_preferences
  ADD CONSTRAINT notification_preferences_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;

CREATE POLICY "Users can manage own preferences" ON public.notification_preferences FOR ALL USING (true);
