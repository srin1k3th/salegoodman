-- SaleGoodman — Seed Data
-- Matches the frontend mock data exactly
-- Run AFTER 001_initial.sql

-- ── Demo Workspace ──────────────────────────────────────────
INSERT INTO workspace (id, name, domain, timezone, notification_prefs) VALUES
('a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'Goodman & Co.', 'goodman.co', 'America/Chicago',
 '{"instant_escalations": true, "daily_briefing": true, "weekly_summary": true, "high_value_alerts": true}');

-- ── Demo Users ──────────────────────────────────────────────
-- NOTE: In production, these IDs come from Supabase Auth.
-- For seed data, we use static UUIDs.
INSERT INTO "user" (id, email, name, role, initials, tone, workspace_id) VALUES
('11111111-1111-1111-1111-111111111111', 'sarah@goodman.co', 'Sarah Goodman', 'Owner / Admin', 'SG', 'coral', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'),
('22222222-2222-2222-2222-222222222222', 'maya@goodman.co', 'Maya Chen', 'VP of Revenue', 'MC', 'gold', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'),
('33333333-3333-3333-3333-333333333333', 'marcus@goodman.co', 'Marcus Bell', 'Revenue Operations', 'MB', 'blue', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890');

-- ── Contacts ────────────────────────────────────────────────
INSERT INTO contact (id, name, role, company, location, relevance_score, initials, tone, source, status, workspace_id) VALUES
('c1000001-0000-0000-0000-000000000001', 'Maya Chen', 'VP of Revenue', 'Northstar Labs', 'Austin, TX', 96, 'MC', 'gold', 'agent', 'warm', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'),
('c1000002-0000-0000-0000-000000000002', 'Marcus Bell', 'Founder & CEO', 'Harbor Systems', 'New York, NY', 92, 'MB', 'blue', 'agent', 'warm', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'),
('c1000003-0000-0000-0000-000000000003', 'Elena Rossi', 'Head of Growth', 'Verity Health', 'San Francisco, CA', 89, 'ER', 'coral', 'agent', 'new', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'),
('c1000004-0000-0000-0000-000000000004', 'Theo Adams', 'CRO', 'Latticeworks', 'Chicago, IL', 86, 'TA', 'green', 'agent', 'new', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'),
('c1000005-0000-0000-0000-000000000005', 'Nina Patel', 'Director of Sales', 'Orbit Commerce', 'Boston, MA', 84, 'NP', 'lavender', 'agent', 'warm', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'),
('c1000006-0000-0000-0000-000000000006', 'Jon Bellamy', 'VP Partnerships', 'Clearpath AI', 'Denver, CO', 81, 'JB', 'gold', 'agent', 'new', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890');

-- ── Leads ───────────────────────────────────────────────────
INSERT INTO lead (id, contact_id, stage, value, company, initials, tone, workspace_id) VALUES
('d1000001-0000-0000-0000-000000000001', 'c1000001-0000-0000-0000-000000000001', 'Closing', '$48,000', 'Northstar Labs', 'MC', 'gold', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'),
('d1000002-0000-0000-0000-000000000002', 'c1000002-0000-0000-0000-000000000002', 'Following Up', '$32,500', 'Harbor Systems', 'MB', 'blue', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'),
('d1000003-0000-0000-0000-000000000003', 'c1000003-0000-0000-0000-000000000003', 'Contacted', '$18,200', 'Verity Health', 'ER', 'coral', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'),
('d1000004-0000-0000-0000-000000000004', 'c1000004-0000-0000-0000-000000000004', 'Found', '$64,000', 'Latticeworks', 'TA', 'green', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'),
('d1000005-0000-0000-0000-000000000005', 'c1000005-0000-0000-0000-000000000005', 'Won', '$26,000', 'Orbit Commerce', 'NP', 'lavender', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'),
('d1000006-0000-0000-0000-000000000006', 'c1000006-0000-0000-0000-000000000006', 'Lost', '$12,800', 'Clearpath AI', 'JB', 'gold', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890');

-- ── Deals ───────────────────────────────────────────────────
INSERT INTO deal (id, lead_id, company, contact_name, value, stage, checklist, workspace_id) VALUES
('e1000001-0000-0000-0000-000000000001', 'd1000001-0000-0000-0000-000000000001', 'Northstar Labs', 'Maya Chen', '$48,000', 'contract_review',
 '[{"item": "Security review", "completed": true}, {"item": "Final pricing", "completed": false}, {"item": "Legal approval", "completed": false}]',
 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'),
('e1000002-0000-0000-0000-000000000002', 'd1000002-0000-0000-0000-000000000002', 'Harbor Systems', 'Marcus Bell', '$32,500', 'in_negotiation',
 '[{"item": "Confirm seats", "completed": true}, {"item": "ROI business case", "completed": false}, {"item": "Procurement", "completed": false}]',
 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'),
('e1000003-0000-0000-0000-000000000003', 'd1000004-0000-0000-0000-000000000004', 'Latticeworks', 'Theo Adams', '$64,000', 'proposal_sent',
 '[{"item": "Proposal viewed", "completed": true}, {"item": "Schedule review call", "completed": false}, {"item": "Mutual action plan", "completed": false}]',
 'a1b2c3d4-e5f6-7890-abcd-ef1234567890');

-- ── Escalations ─────────────────────────────────────────────
INSERT INTO escalation (id, lead_id, title, source_agent, contact_info, summary, workspace_id) VALUES
('f1000001-0000-0000-0000-000000000001', 'd1000001-0000-0000-0000-000000000001',
 'Pricing objection from Maya Chen', 'closing_agent', 'Maya Chen · Northstar Labs',
 'Maya asked for a 28% discount and wants to compare against an incumbent vendor. The agent recommends holding price and offering an annual commitment incentive.',
 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'),
('f1000002-0000-0000-0000-000000000002', 'd1000003-0000-0000-0000-000000000003',
 'Unclear buying committee', 'outreach_agent', 'Elena Rossi · Verity Health',
 'Elena is excited, but mentioned that her co-founder signs off on all new tooling. Should we ask for an introduction?',
 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'),
('f1000003-0000-0000-0000-000000000003', 'd1000002-0000-0000-0000-000000000002',
 'Contract clause needs review', 'closing_agent', 'Marcus Bell · Harbor Systems',
 'Marcus requested a custom data retention clause that falls outside the agent''s approval guardrails.',
 'a1b2c3d4-e5f6-7890-abcd-ef1234567890');

-- ── Agent Configs ───────────────────────────────────────────
INSERT INTO agent_config (agent_type, config, workspace_id) VALUES
('contact_finder', '{"formality": 3, "directness": 4, "daily_quota": 50, "min_fit_score": 85, "auto_enrich": true, "escalate_enterprise": true}', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'),
('outreach', '{"formality": 2, "directness": 4, "voice_profile": "Sarah (Warm Consultative)", "daily_limit": 25, "escalate_competitor": true, "escalate_integration": true, "sentiment_guardrail": true}', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'),
('follow_up', '{"formality": 3, "directness": 4, "touch_days": [1, 4, 8, 14], "max_touches": 4, "auto_pause": true, "escalate_unanswered": 3}', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'),
('closing', '{"formality": 4, "directness": 3, "max_discount_pct": 15, "max_term_extension_days": 30, "payment_terms": "Allow Net 45 without approval", "mutual_nda": true, "strict_redlines": true}', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'),
('orchestrator', '{"confidence_threshold": 90, "coordination_mode": "Adaptive Parallel Hand-off", "briefing_time": "8:30 AM", "safety_switch": false}', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890');

-- ── Activity Log (recent activity feed) ─────────────────────
INSERT INTO activity_log (agent_name, description, lead_id, initials, tone, workspace_id) VALUES
('Contact Finder', 'Found a high-fit contact at Northstar Labs', 'd1000001-0000-0000-0000-000000000001', 'MC', 'gold', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'),
('Outreach Agent', 'Call completed with Elena Rossi', 'd1000003-0000-0000-0000-000000000003', 'ER', 'coral', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'),
('Follow-Up Agent', 'Scheduled follow-up for Theo Adams', 'd1000004-0000-0000-0000-000000000004', 'TA', 'green', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'),
('Closing Agent', 'Proposal sent to Maya Chen', 'd1000001-0000-0000-0000-000000000001', 'SG', 'blue', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890');

-- ── Calls (today's queue) ───────────────────────────────────
INSERT INTO call (lead_id, scheduled_at, status, duration, interest_level, next_step, transcript, workspace_id) VALUES
('d1000001-0000-0000-0000-000000000001', now() - interval '2 hours', 'completed', '8m 24s', 'warm', 'Send proposal',
 '[{"speaker": "Maya", "text": "We have been looking for a way to improve how our team handles inbound demand."}, {"speaker": "Sarah", "text": "That is exactly where we help. Our agents qualify and route those conversations automatically."}, {"speaker": "__signal", "text": "Strong buying signal: asked about implementation timeline."}]',
 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'),
('d1000003-0000-0000-0000-000000000003', now() - interval '90 minutes', 'completed', '11m 02s', 'warm', 'Schedule follow-up', NULL, 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'),
('d1000002-0000-0000-0000-000000000002', now() + interval '30 minutes', 'pending', NULL, NULL, NULL, NULL, 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'),
('d1000004-0000-0000-0000-000000000004', now() + interval '1 hour', 'no_answer', NULL, NULL, NULL, NULL, 'a1b2c3d4-e5f6-7890-abcd-ef1234567890');

-- ── Follow-Ups ──────────────────────────────────────────────
INSERT INTO follow_up (lead_id, touch_number, type, message_subject, message_body, temperature, scheduled_at, status, workspace_id) VALUES
('d1000001-0000-0000-0000-000000000001', 1, 'email', 'Proposal recap and implementation timeline', 'Send proposal recap and implementation timeline', 'warm', now() + interval '3 hours', 'scheduled', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'),
('d1000003-0000-0000-0000-000000000003', 1, 'email', 'Pricing review before next touch', 'Review pricing objection before next touch', 'escalated', now() + interval '5 hours', 'scheduled', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'),
('d1000006-0000-0000-0000-000000000006', 2, 'email', 'Customer story from Clearpath AI', 'Share customer story from Clearpath AI', 'cold', now() + interval '1 day', 'scheduled', 'a1b2c3d4-e5f6-7890-abcd-ef1234567890');
