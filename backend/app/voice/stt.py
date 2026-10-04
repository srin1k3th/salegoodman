"""
Speech-to-Text — Groq Whisper API client.

Transcribes audio from outreach calls into text.
Requires GROQ_API_KEY in .env.
"""

import httpx
from app.config import settings


class SpeechToText:
    """Groq Whisper STT client."""

    def __init__(self):
        self.api_key = settings.groq_api_key
        self.base_url = "https://api.groq.com/openai/v1"
        self.model = "whisper-large-v3"

    async def transcribe(self, audio_bytes: bytes, language: str = "en") -> dict:
        """
        Transcribe audio bytes to text using Groq Whisper.

        Args:
            audio_bytes: Raw audio data (wav, mp3, etc.)
            language: Language code (default: "en")

        Returns:
            {"text": "transcribed text", "segments": [...]}
        """
        if not self.api_key:
            return {
                "text": "[STT placeholder — set GROQ_API_KEY in .env]",
                "segments": [],
                "error": "GROQ_API_KEY not configured",
            }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/audio/transcriptions",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    files={"file": ("audio.wav", audio_bytes, "audio/wav")},
                    data={
                        "model": self.model,
                        "language": language,
                        "response_format": "verbose_json",
                    },
                    timeout=30.0,
                )
                response.raise_for_status()
                data = response.json()

                return {
                    "text": data.get("text", ""),
                    "segments": data.get("segments", []),
                }

        except Exception as e:
            return {
                "text": "",
                "segments": [],
                "error": str(e),
            }


# Singleton
stt = SpeechToText()
