-- Telemetry: track Synco installations for license compliance
CREATE TABLE IF NOT EXISTS installations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    installation_id TEXT NOT NULL,
    version TEXT,
    environment TEXT,
    license_valid BOOLEAN DEFAULT false,
    integrity_ok BOOLEAN DEFAULT true,
    file_hashes JSONB DEFAULT '{}',
    host_fingerprint TEXT,
    python_version TEXT,
    os TEXT,
    reported_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- One row per unique installation; upsert on heartbeat
CREATE UNIQUE INDEX IF NOT EXISTS idx_installations_install_id
    ON installations (installation_id);

-- Fast lookups for admin dashboard
CREATE INDEX IF NOT EXISTS idx_installations_license_valid
    ON installations (license_valid);
CREATE INDEX IF NOT EXISTS idx_installations_integrity_ok
    ON installations (integrity_ok);

-- RLS: only service role can read/write (backend uses service role key)
ALTER TABLE installations ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Service role full access on installations"
    ON installations FOR ALL
    USING (auth.role() = 'service_role')
    WITH CHECK (auth.role() = 'service_role');
