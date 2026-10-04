"""
Text-to-Speech — Gemini TTS client.

Uses gemini-3.8-flash-tts for high-quality, controllable speech synthesis
with a wide library of prebuilt voices. Falls back to gemini-2.0-flash
for basic audio generation.

Requires GEMINI_API_KEY in .env.
"""

import base64
import httpx
from app.config import settings

# Prebuilt Gemini voices mapped to agent persona styles
VOICE_MAP = {
    "warm":        "Aoede",    # Warm, approachable — default Sarah persona
    "confident":   "Charon",   # Confident and direct
    "consultative":"Fenrir",   # Calm, consultative tone
    "formal":      "Kore",     # Professional, executive-level
    "authoritative":"Orus",    # Authoritative, commanding
}


class TextToSpeech:
    """Gemini TTS client using gemini-3.8-flash-tts."""

    def __init__(self):
        self.api_key = settings.gemini_api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        # Primary: dedicated high-quality TTS model
        self.tts_model = "gemini-3.8-flash-tts"
        # Fallback: fast low-latency flash-lite TTS
        self.fallback_model = "gemini-3.8-flash-lite-tts"

    def _resolve_voice(self, voice: str) -> str:
        """Resolve persona-style voice name to Gemini prebuilt voice ID."""
        # Accept direct Gemini voice names or persona-style keys
        if voice in VOICE_MAP.values():
            return voice
        return VOICE_MAP.get(voice.lower(), "Aoede")

    async def synthesize(
        self,
        text: str,
        voice: str = "warm",
        speaking_rate: float = 1.0,
    ) -> bytes | None:
        """
        Synthesize text to speech using Gemini TTS.

        Args:
            text:          Text to synthesize
            voice:         Persona style key or direct Gemini voice name
            speaking_rate: Speed multiplier (0.5 = slow, 2.0 = fast)

        Returns:
            Audio bytes (wav/pcm) or None if not configured
        """
        if not self.api_key:
            return None

        voice_name = self._resolve_voice(voice)

        # Try primary TTS model
        audio = await self._synthesize_with_model(
            self.tts_model, text, voice_name, speaking_rate
        )
        if audio:
            return audio

        # Fallback to multimodal flash
        return await self._synthesize_with_model(
            self.fallback_model, text, voice_name, speaking_rate
        )

    async def _synthesize_with_model(
        self,
        model: str,
        text: str,
        voice_name: str,
        speaking_rate: float,
    ) -> bytes | None:
        """Call Gemini API for TTS with a specific model."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/models/{model}:generateContent",
                    params={"key": self.api_key},
                    json={
                        "contents": [{
                            "parts": [{"text": text}]
                        }],
                        "generationConfig": {
                            "response_modalities": ["AUDIO"],
                            "speech_config": {
                                "voice_config": {
                                    "prebuilt_voice_config": {
                                        "voice_name": voice_name
                                    }
                                }
                            },
                        },
                    },
                    timeout=30.0,
                )
                response.raise_for_status()
                data = response.json()

                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    for part in parts:
                        if "inlineData" in part:
                            return base64.b64decode(part["inlineData"]["data"])

                return None

        except Exception:
            return None


# Singleton
tts = TextToSpeech()
