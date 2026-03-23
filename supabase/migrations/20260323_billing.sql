-- Billing: subscriptions and billing events tables
CREATE TABLE IF NOT EXISTS subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE REFERENCES auth.users(id) ON DELETE CASCADE,
    stripe_customer_id TEXT UNIQUE,
    stripe_subscription_id TEXT UNIQUE,
    plan TEXT NOT NULL DEFAULT 'free' CHECK (plan IN ('free', 'pro', 'family_plus')),
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'past_due', 'canceled', 'incomplete')),
    current_period_end TIMESTAMPTZ,
    cancel_at_period_end BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_subscriptions_user ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_stripe_customer ON subscriptions(stripe_customer_id);

-- Enable RLS
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can read own subscription" ON subscriptions FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Service role can insert subscriptions" ON subscriptions FOR INSERT WITH CHECK (true);
CREATE POLICY "Service role can update subscriptions" ON subscriptions FOR UPDATE USING (true);

-- Billing events for SaaS analytics (SAS-06)
CREATE TABLE IF NOT EXISTS billing_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    event_type TEXT NOT NULL CHECK (event_type IN ('signup', 'subscribe', 'plan_change', 'cancel', 'churn', 'payment_failed')),
    plan TEXT,
    stripe_event_id TEXT UNIQUE,
    metadata JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_billing_events_user_created ON billing_events(user_id, created_at DESC);
CREATE INDEX idx_billing_events_stripe_event ON billing_events(stripe_event_id);

ALTER TABLE billing_events ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can read own billing events" ON billing_events FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Service role can insert billing events" ON billing_events FOR INSERT WITH CHECK (true);
