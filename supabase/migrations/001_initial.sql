-- SaleGoodman — Initial Database Schema
-- Run this in the Supabase SQL Editor to create all tables

-- ── Extensions ──────────────────────────────────────────────
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ── Tables ──────────────────────────────────────────────────

CREATE TABLE workspace (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    domain TEXT,
    timezone TEXT NOT NULL DEFAULT 'America/Chicago',
    notification_prefs JSONB DEFAULT '{}',
    safety_killswitch BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE "user" (
    id UUID PRIMARY KEY,  -- References auth.users(id)
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'Sales Representative',
    initials TEXT,
    tone TEXT DEFAULT 'blue',
    workspace_id UUID REFERENCES workspace(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE contact (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    role TEXT,
    company TEXT,
    location TEXT,
    relevance_score INT DEFAULT 0 CHECK (relevance_score >= 0 AND relevance_score <= 100),
    initials TEXT,
    tone TEXT DEFAULT 'blue',
    source TEXT DEFAULT 'agent',
    status TEXT DEFAULT 'new',
    email TEXT,
    phone TEXT,
    last_contacted DATE,
    enriched BOOLEAN DEFAULT FALSE,
    workspace_id UUID NOT NULL REFERENCES workspace(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE lead (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contact_id UUID REFERENCES contact(id) ON DELETE SET NULL,
    stage TEXT NOT NULL DEFAULT 'Found',
    value TEXT,
    company TEXT,
    initials TEXT,
    tone TEXT,
    agent_notes JSONB DEFAULT '{}',
    last_touched TIMESTAMPTZ DEFAULT now(),
    workspace_id UUID NOT NULL REFERENCES workspace(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE call (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID REFERENCES lead(id) ON DELETE CASCADE,
    scheduled_at TIMESTAMPTZ NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    duration TEXT,
    transcript JSONB,
    notes_summary JSONB,
    interest_level TEXT,
    next_step TEXT,
    follow_up_date DATE,
    voice_profile TEXT DEFAULT 'Sarah (Warm Consultative)',
    recording_url TEXT,
    workspace_id UUID REFERENCES workspace(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE follow_up (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID REFERENCES lead(id) ON DELETE CASCADE,
    touch_number INT NOT NULL,
    type TEXT DEFAULT 'email',
    message_subject TEXT,
    message_body TEXT,
    temperature TEXT NOT NULL DEFAULT 'warm',
    scheduled_at TIMESTAMPTZ NOT NULL,
    status TEXT DEFAULT 'scheduled',
    workspace_id UUID REFERENCES workspace(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE deal (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID REFERENCES lead(id) ON DELETE CASCADE,
    company TEXT NOT NULL,
    contact_name TEXT,
    value TEXT,
    stage TEXT NOT NULL DEFAULT 'proposal_sent',
    checklist JSONB DEFAULT '[]',
    discount_offered NUMERIC(5,2),
    term_extension_days INT,
    payment_terms TEXT,
    workspace_id UUID REFERENCES workspace(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE escalation (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID REFERENCES lead(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    source_agent TEXT NOT NULL,
    contact_info TEXT,
    summary TEXT,
    status TEXT DEFAULT 'pending',
    resolution TEXT,
    resolved_by UUID REFERENCES "user"(id),
    workspace_id UUID REFERENCES workspace(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT now(),
    resolved_at TIMESTAMPTZ
);

CREATE TABLE agent_config (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_type TEXT NOT NULL,
    config JSONB NOT NULL,
    workspace_id UUID REFERENCES workspace(id) ON DELETE CASCADE,
    updated_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE(workspace_id, agent_type)
);

CREATE TABLE activity_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID REFERENCES lead(id) ON DELETE SET NULL,
    agent_name TEXT NOT NULL,
    description TEXT NOT NULL,
    initials TEXT,
    tone TEXT,
    workspace_id UUID REFERENCES workspace(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- ── Indexes ─────────────────────────────────────────────────

CREATE INDEX idx_contact_workspace ON contact(workspace_id);
CREATE INDEX idx_contact_score ON contact(workspace_id, relevance_score DESC);
CREATE INDEX idx_contact_name_trgm ON contact USING gin (name gin_trgm_ops);

CREATE INDEX idx_lead_workspace ON lead(workspace_id);
CREATE INDEX idx_lead_stage ON lead(workspace_id, stage);
CREATE INDEX idx_lead_last_touched ON lead(workspace_id, last_touched DESC);

CREATE INDEX idx_call_workspace ON call(workspace_id);
CREATE INDEX idx_call_scheduled ON call(workspace_id, scheduled_at);
CREATE INDEX idx_call_status ON call(workspace_id, status);

CREATE INDEX idx_followup_workspace ON follow_up(workspace_id);
CREATE INDEX idx_followup_scheduled ON follow_up(workspace_id, scheduled_at);
CREATE INDEX idx_followup_status ON follow_up(workspace_id, status);

CREATE INDEX idx_deal_workspace ON deal(workspace_id);
CREATE INDEX idx_escalation_workspace ON escalation(workspace_id);
CREATE INDEX idx_escalation_status ON escalation(workspace_id, status);
CREATE INDEX idx_escalation_created ON escalation(workspace_id, created_at DESC);

CREATE INDEX idx_activity_workspace ON activity_log(workspace_id);
CREATE INDEX idx_activity_created ON activity_log(workspace_id, created_at DESC);

-- ── Row Level Security ──────────────────────────────────────

ALTER TABLE workspace ENABLE ROW LEVEL SECURITY;
ALTER TABLE "user" ENABLE ROW LEVEL SECURITY;
ALTER TABLE contact ENABLE ROW LEVEL SECURITY;
ALTER TABLE lead ENABLE ROW LEVEL SECURITY;
ALTER TABLE call ENABLE ROW LEVEL SECURITY;
ALTER TABLE follow_up ENABLE ROW LEVEL SECURITY;
ALTER TABLE deal ENABLE ROW LEVEL SECURITY;
ALTER TABLE escalation ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_config ENABLE ROW LEVEL SECURITY;
ALTER TABLE activity_log ENABLE ROW LEVEL SECURITY;

-- RLS Policies: Users can only access records in their workspace
CREATE POLICY "workspace_access" ON workspace FOR ALL
    USING (id = (SELECT workspace_id FROM "user" WHERE id = auth.uid()));
CREATE POLICY "workspace_isolation" ON contact FOR ALL
    USING (workspace_id = (SELECT workspace_id FROM "user" WHERE id = auth.uid()));

CREATE POLICY "workspace_isolation" ON lead FOR ALL
    USING (workspace_id = (SELECT workspace_id FROM "user" WHERE id = auth.uid()));

CREATE POLICY "workspace_isolation" ON call FOR ALL
    USING (workspace_id = (SELECT workspace_id FROM "user" WHERE id = auth.uid()));

CREATE POLICY "workspace_isolation" ON follow_up FOR ALL
    USING (workspace_id = (SELECT workspace_id FROM "user" WHERE id = auth.uid()));

CREATE POLICY "workspace_isolation" ON deal FOR ALL
    USING (workspace_id = (SELECT workspace_id FROM "user" WHERE id = auth.uid()));

CREATE POLICY "workspace_isolation" ON escalation FOR ALL
    USING (workspace_id = (SELECT workspace_id FROM "user" WHERE id = auth.uid()));

CREATE POLICY "workspace_isolation" ON agent_config FOR ALL
    USING (workspace_id = (SELECT workspace_id FROM "user" WHERE id = auth.uid()));

CREATE POLICY "workspace_isolation" ON activity_log FOR ALL
    USING (workspace_id = (SELECT workspace_id FROM "user" WHERE id = auth.uid()));

CREATE POLICY "users_own_workspace" ON "user" FOR ALL
    USING (workspace_id = (SELECT workspace_id FROM "user" WHERE id = auth.uid()));

-- ── Realtime ────────────────────────────────────────────────

ALTER PUBLICATION supabase_realtime ADD TABLE activity_log;
ALTER PUBLICATION supabase_realtime ADD TABLE escalation;
