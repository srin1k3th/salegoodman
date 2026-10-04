"""
Text-to-Speech — Gemini TTS client.

Synthesizes agent responses into natural speech for outreach calls.
Requires GEMINI_API_KEY in .env.
"""

import httpx
from app.config import settings


class TextToSpeech:
    """Gemini TTS client."""

    def __init__(self):
        self.api_key = settings.gemini_api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"

    async def synthesize(self, text: str, voice: str = "Kore") -> bytes | None:
        """
        Synthesize text to speech using Gemini TTS.

        Args:
            text: Text to synthesize
            voice: Voice profile name

        Returns:
            Audio bytes (wav format) or None if not configured
        """
        if not self.api_key:
            return None

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/models/gemini-2.0-flash:generateContent",
                    params={"key": self.api_key},
                    json={
                        "contents": [{
                            "parts": [{"text": f"Read the following aloud in a natural, warm tone: {text}"}]
                        }],
                        "generationConfig": {
                            "response_modalities": ["AUDIO"],
                            "speech_config": {
                                "voice_config": {
                                    "prebuilt_voice_config": {"voice_name": voice}
                                }
                            }
                        }
                    },
                    timeout=30.0,
                )
                response.raise_for_status()
                data = response.json()

                # Extract audio from response
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    for part in parts:
                        if "inlineData" in part:
                            import base64
                            return base64.b64decode(part["inlineData"]["data"])

                return None

        except Exception:
            return None


# Singleton
tts = TextToSpeech()
