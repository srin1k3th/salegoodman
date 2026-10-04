"""
Speech-to-Text — Gemini Audio Transcription.

Uses gemini-3.5-transcribe for high-accuracy speech transcription.
Falls back to gemini-2.0-flash multimodal audio input if transcribe
model is unavailable.

Requires GEMINI_API_KEY in .env.
"""

import base64
import httpx
from app.config import settings


class SpeechToText:
    """Gemini STT client using gemini-3.5-transcribe."""

    def __init__(self):
        self.api_key = settings.gemini_api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        # Primary: multimodal flash for rapid inline audio transcription
        self.models = ["gemini-3.5-flash", "gemini-flash-latest", "gemini-3.8-flash"]

    async def transcribe(self, audio_bytes: bytes, language: str = "en") -> dict:
        """
        Transcribe audio bytes to text using Gemini.

        Args:
            audio_bytes: Raw audio data (wav, mp3, webm, etc.)
            language:    Language code (default: "en")

        Returns:
            {"text": "transcribed text", "segments": [], "model": "..."}
        """
        if not self.api_key:
            return {
                "text": "[STT placeholder — set GEMINI_API_KEY in .env]",
                "segments": [],
                "error": "GEMINI_API_KEY not configured",
            }

        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

        # Try models in order of latency and preference
        for model in self.models:
            result = await self._transcribe_with_model(model, audio_b64, language)
            if result.get("text"):
                return result

        return {"text": "", "segments": [], "error": "Transcription failed on all candidate models"}

    async def _transcribe_with_model(
        self, model: str, audio_b64: str, language: str
    ) -> dict:
        """Call Gemini API for transcription with a specific model."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/models/{model}:generateContent",
                    params={"key": self.api_key},
                    json={
                        "contents": [{
                            "parts": [
                                {
                                    "inlineData": {
                                        "mimeType": "audio/wav",
                                        "data": audio_b64,
                                    }
                                },
                                {
                                    "text": (
                                        f"Transcribe this audio exactly as spoken in {language}. "
                                        "Output only the transcript text, no commentary."
                                    )
                                },
                            ]
                        }],
                        "generationConfig": {"temperature": 0},
                    },
                    timeout=30.0,
                )
                response.raise_for_status()
                data = response.json()

                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return {
                            "text": parts[0].get("text", "").strip(),
                            "segments": [],
                            "model": model,
                        }

                return {"text": "", "segments": [], "model": model}

        except Exception as e:
            return {"text": "", "segments": [], "error": str(e), "model": model}


# Singleton
stt = SpeechToText()
