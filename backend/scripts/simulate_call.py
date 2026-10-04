"""
End-to-End Autonomous Voice Outreach Simulation.

Simulates an autonomous AI SDR voice call against a live Supabase lead:
1. Loads lead & contact context from Supabase
2. Retrieves agent configuration (Sarah persona, tone, formality)
3. Synthesizes personalized opening greeting via Gemini TTS (gemini-3.8-flash-tts)
4. Simulates prospect objection / dialogue turn
5. Reasons and responds live using Gemini LLM (gemini-3.5-flash)
6. Synthesizes agent response audio via Gemini TTS
7. Analyzes transcript for buying signals, sentiment, and action items
8. Persists call records, transcript, and activity logs to Supabase
"""

import sys
import time
import asyncio
from datetime import datetime, timezone

from app.database import supabase_admin
from app.services.outreach_agent import OutreachAgent
from app.voice.llm import llm
from app.voice.tts import tts


async def run_simulation():
    print("\n" + "=" * 70)
    print(" [VOICE] SALEGOODMAN -- AUTONOMOUS VOICE OUTREACH SIMULATION")
    print("=" * 70)

    if not supabase_admin:
        print("[!] Supabase admin client not initialized. Check .env")
        sys.exit(1)

    # 1. Fetch workspace
    ws_res = supabase_admin.table("workspace").select("id, name").limit(1).execute()
    if not ws_res.data:
        print("[!] No workspace found in Supabase. Run seed.sql first.")
        sys.exit(1)

    workspace = ws_res.data[0]
    workspace_id = workspace["id"]
    print(f" Workspace: {workspace['name']} ({workspace_id})")

    # 2. Fetch a lead with contact info
    lead_res = supabase_admin.table("lead").select("*, contact(*)").eq("workspace_id", workspace_id).limit(1).execute()
    if not lead_res.data:
        print("[!] No leads found in Supabase.")
        sys.exit(1)

    lead = lead_res.data[0]
    contact = lead.get("contact") or {"name": "Maya Chen", "company": "Northstar Labs", "role": "VP of Revenue"}
    prospect_name = contact.get("name", "Prospect")
    company_name = contact.get("company", "Company")
    role = contact.get("role", "Executive")
    print(f" Target Lead: {prospect_name} ({role} @ {company_name})")

    # 3. Initialize OutreachAgent with Supabase config
    agent = OutreachAgent(workspace_id)
    config = agent.config
    voice_profile = config.get("voice_profile", "Sarah (Warm Consultative)")
    print(f" Agent Persona: {voice_profile} | Formality: {config.get('formality', 3)}/5")

    # 4. Generate Opening Pitch
    print("\n[Step 1] Generating personalized opening pitch...")
    t0 = time.time()
    opening = agent.generate_call_opening(prospect_name, company_name)
    pitch_latency = (time.time() - t0) * 1000
    print(f"   Opening Pitch ({pitch_latency:.0f}ms): \"{opening}\"")

    # 5. Synthesize Opening Audio via Gemini TTS
    print("\n[Step 2] Synthesizing speech via Gemini TTS (gemini-3.8-flash-tts)...")
    t0 = time.time()
    opening_audio = await tts.synthesize(opening, voice="warm")
    tts_latency = (time.time() - t0) * 1000
    audio_size = len(opening_audio) if opening_audio else 0
    print(f"   Audio Generated: {audio_size:,} bytes of WAV audio ({tts_latency:.0f}ms)")

    # 6. Simulate Prospect Response
    prospect_reply = "We already have Apollo for contacts and Outreach for email cadences. Why should we look at SaleGoodman?"
    print(f"\n[Step 3] Prospect ({prospect_name}) replies:")
    print(f"   \"{prospect_reply}\"")

    # 7. Live LLM Reasoning & Response (gemini-3.5-flash)
    transcript = [
        {"speaker": "Sarah", "text": opening},
        {"speaker": prospect_name, "text": prospect_reply},
    ]

    print("\n[Step 4] Live AI Reasoning via Gemini LLM (gemini-3.5-flash)...")
    t0 = time.time()
    response_text = await llm.generate_response(
        transcript=transcript,
        agent_config=config,
        prospect_context=contact,
    )
    llm_latency = (time.time() - t0) * 1000
    print(f"   Agent Response ({llm_latency:.0f}ms):")
    print(f"   \"{response_text}\"")

    # 8. Synthesize Agent Response Audio
    print("\n[Step 5] Synthesizing agent reply audio via Gemini TTS...")
    t0 = time.time()
    response_audio = await tts.synthesize(response_text, voice="warm")
    reply_tts_latency = (time.time() - t0) * 1000
    reply_audio_size = len(response_audio) if response_audio else 0
    print(f"   Audio Generated: {reply_audio_size:,} bytes ({reply_tts_latency:.0f}ms)")

    # 9. Analyze Transcript for Intelligence & Next Steps
    transcript.append({"speaker": "Sarah", "text": response_text})
    print("\n[Step 6] Saving call record to Supabase...")
    now_iso = datetime.now(timezone.utc).isoformat()

    # Create call record
    call_record = {
        "lead_id": lead["id"],
        "workspace_id": workspace_id,
        "scheduled_at": now_iso,
        "status": "completed",
        "duration": "1m 15s",
        "transcript": transcript,
        "voice_profile": voice_profile,
    }
    call_insert = supabase_admin.table("call").insert(call_record).execute()
    call_id = call_insert.data[0]["id"]
    print(f"   [OK] Call created in Supabase (ID: {call_id})")

    # 10. Process Call Result via OutreachAgent
    print("\n[Step 7] Processing call intelligence & escalation rules...")
    result = await agent.process_call_result(call_id, transcript)
    notes = result.get("notes_summary", {})
    print(f"   Interest Level    : {notes.get('interest_level')}")
    print(f"   Next Step         : {notes.get('next_step')}")
    print(f"   Competitor Flagged: {notes.get('competitor_mentioned')}")
    print(f"   Escalation Needed : {result.get('escalation_needed')} ({result.get('escalation_reasons')})")

    # Update lead stage
    supabase_admin.table("lead").update({
        "stage": "Engaged",
        "last_touched": now_iso,
    }).eq("id", lead["id"]).execute()
    print(f"   [OK] Lead stage updated to 'Engaged' in Supabase")

    # Log activity
    supabase_admin.table("activity_log").insert({
        "workspace_id": workspace_id,
        "lead_id": lead["id"],
        "agent_name": "Outreach Agent",
        "description": f"Completed call with {prospect_name} ({company_name}) — {notes.get('interest_level')} interest",
        "initials": "OA",
        "tone": "blue",
    }).execute()
    print(f"   [OK] Activity log entry recorded in Supabase")

    print("\n" + "=" * 70)
    print(" [OK] SIMULATION COMPLETED SUCCESSFULLY!")
    print(f" Total Voice Turn Latency: {llm_latency:.0f}ms LLM + {reply_tts_latency:.0f}ms TTS")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    asyncio.run(run_simulation())
