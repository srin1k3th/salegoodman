"""
Call Handler — orchestrates a voice call session.

Wires STT → LLM → TTS in sequence for each turn of a conversation.
"""

from app.voice.stt import stt
from app.voice.llm import llm
from app.voice.tts import tts
from app.database import supabase_admin


class CallHandler:
    """Manages a single voice call session."""

    def __init__(self, call_id: str, workspace_id: str, agent_config: dict):
        self.call_id = call_id
        self.workspace_id = workspace_id
        self.agent_config = agent_config
        self.transcript: list[dict] = []
        self.prospect_context: dict | None = None

    def set_prospect_context(self, context: dict):
        """Set prospect info for personalized responses."""
        self.prospect_context = context

    async def process_audio_turn(self, audio_bytes: bytes) -> dict:
        """
        Process one turn of conversation:
        1. Transcribe prospect's audio (STT)
        2. Generate agent response (LLM)
        3. Synthesize response audio (TTS)

        Returns:
            {
                "prospect_text": str,
                "agent_text": str,
                "agent_audio": bytes | None,
                "buying_signals": list
            }
        """
        # 1. Transcribe prospect audio
        stt_result = await stt.transcribe(audio_bytes)
        prospect_text = stt_result.get("text", "")

        # Add to transcript
        self.transcript.append({
            "speaker": self.prospect_context.get("name", "Prospect") if self.prospect_context else "Prospect",
            "text": prospect_text,
        })

        # 2. Generate agent response
        agent_text = await llm.generate_response(
            transcript=self.transcript,
            agent_config=self.agent_config,
            prospect_context=self.prospect_context,
        )

        # Add to transcript
        self.transcript.append({
            "speaker": "Sarah",
            "text": agent_text,
        })

        # 3. Synthesize response audio
        agent_audio = await tts.synthesize(agent_text)

        # Detect buying signals
        buying_signals = self._detect_buying_signals(prospect_text)

        return {
            "prospect_text": prospect_text,
            "agent_text": agent_text,
            "agent_audio": agent_audio,
            "buying_signals": buying_signals,
        }

    def _detect_buying_signals(self, text: str) -> list[str]:
        """Detect buying signals in prospect's speech."""
        signals = []
        text_lower = text.lower()

        signal_phrases = {
            "implementation timeline": "Asked about implementation timeline",
            "how soon": "Expressed urgency about getting started",
            "pricing": "Asked about pricing",
            "budget": "Mentioned budget discussions",
            "demo": "Requested a demo",
            "contract": "Asked about contract terms",
            "decision maker": "Referenced decision-making process",
            "next steps": "Asked about next steps",
            "roi": "Interested in ROI metrics",
        }

        for phrase, signal in signal_phrases.items():
            if phrase in text_lower:
                signals.append(signal)

        return signals

    async def end_call(self, status: str = "completed", duration: str = "") -> dict:
        """
        End the call and save results to DB.

        Returns the complete call record.
        """
        result = supabase_admin.table("call").update({
            "status": status,
            "duration": duration,
            "transcript": self.transcript,
        }).eq("id", self.call_id).execute()

        # Log activity
        supabase_admin.table("activity_log").insert({
            "agent_name": "Outreach Agent",
            "description": f"Call {status} ({duration})" if duration else f"Call {status}",
            "workspace_id": self.workspace_id,
        }).execute()

        return result.data[0] if result.data else {}

    def get_transcript(self) -> list[dict]:
        """Get the current transcript."""
        return self.transcript
