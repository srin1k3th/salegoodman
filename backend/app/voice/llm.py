"""
LLM Conversation Engine — Gemini-powered conversational AI.

Generates context-aware responses during outreach calls using few-shot
personality prompts tuned to the agent's configured formality and tone.
"""

import httpx
from app.config import settings


class ConversationEngine:
    """Gemini-based conversational AI for voice calls."""

    def __init__(self):
        self.api_key = settings.gemini_api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.model = "gemini-2.0-flash"

    async def generate_response(
        self,
        transcript: list[dict],
        agent_config: dict,
        prospect_context: dict | None = None,
    ) -> str:
        """
        Generate a contextual response during a live call.

        Args:
            transcript: Conversation history [{speaker, text}]
            agent_config: Outreach agent config (formality, directness, etc.)
            prospect_context: {name, company, role, previous_interactions}

        Returns:
            Generated response text
        """
        if not self.api_key:
            return "[LLM placeholder — set GEMINI_API_KEY in .env to enable AI responses]"

        system_prompt = self._build_system_prompt(agent_config, prospect_context)
        conversation = self._format_transcript(transcript)

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/models/{self.model}:generateContent",
                    params={"key": self.api_key},
                    json={
                        "system_instruction": {"parts": [{"text": system_prompt}]},
                        "contents": [{"parts": [{"text": conversation}]}],
                        "generationConfig": {
                            "temperature": 0.7,
                            "maxOutputTokens": 200,
                        }
                    },
                    timeout=15.0,
                )
                response.raise_for_status()
                data = response.json()

                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "")

                return "I appreciate you sharing that. Let me get back to you with more details."

        except Exception:
            return "That's a great point. Let me look into that and follow up with you shortly."

    def _build_system_prompt(self, config: dict, context: dict | None) -> str:
        """Build a personality-tuned system prompt based on agent config."""
        formality = config.get("formality", 2)
        directness = config.get("directness", 4)
        voice = config.get("voice_profile", "Sarah (Warm Consultative)")

        # Base personality
        if formality <= 2:
            tone = "casual, friendly, and approachable"
        elif formality >= 4:
            tone = "professional, polished, and executive-level"
        else:
            tone = "balanced, consultative, and natural"

        if directness <= 2:
            style = "Get to the point quickly. Lead with value proposition."
        elif directness >= 4:
            style = "Build rapport first. Focus on understanding their challenges before presenting solutions."
        else:
            style = "Balance between understanding needs and presenting solutions."

        prospect_info = ""
        if context:
            prospect_info = f"""
Prospect Info:
- Name: {context.get('name', 'the prospect')}
- Company: {context.get('company', '')}
- Role: {context.get('role', '')}
"""

        return f"""You are {voice.split('(')[0].strip()}, an AI sales development representative for SaleGoodman.

Tone: {tone}
Style: {style}

Rules:
1. Never make promises about pricing, discounts, or contract terms.
2. If the prospect asks about specific pricing or legal terms, say you'll have your team follow up.
3. Keep responses concise — this is a phone call, not an essay.
4. Listen for buying signals (timeline questions, budget mentions, stakeholder references).
5. If the prospect seems frustrated or disinterested, gracefully offer to schedule a better time.
6. Never reveal that you are an AI unless directly asked.
{prospect_info}

Respond naturally as if you're on a live phone call. Keep it under 3 sentences."""

    def _format_transcript(self, transcript: list[dict]) -> str:
        """Format transcript for LLM context."""
        lines = []
        for entry in transcript[-10:]:  # Last 10 exchanges for context window
            speaker = entry.get("speaker", "Unknown")
            text = entry.get("text", "")
            lines.append(f"{speaker}: {text}")

        return "\n".join(lines) + "\n\nGenerate the next response for Sarah:"


# Singleton
llm = ConversationEngine()
