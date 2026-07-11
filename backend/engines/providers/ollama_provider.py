"""
Strategic AI Core Backend
Ollama LLM provider
"""

import json
import urllib.error
import urllib.request

from config import llm_config
from engines.providers.base_provider import BaseProvider

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "qwen2.5:7b"


class OllamaProvider(BaseProvider):
    def generate_analysis(self, llm_input: dict) -> dict:
        agent_name = llm_input.get("agent")
        reasoning_context = llm_input.get("reasoning_context") or {}
        model = self._resolve_model()
        prompt = self._build_prompt(agent_name, reasoning_context)

        payload = json.dumps({
            "model": model,
            "prompt": prompt,
            "format": "json",
            "stream": False,
        }).encode("utf-8")

        request = urllib.request.Request(
            OLLAMA_URL,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                body = response.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"Ollama returned an error response: {e.code} {e.reason}") from e
        except (urllib.error.URLError, OSError) as e:
            raise RuntimeError(
                f"Ollama is unavailable at {OLLAMA_URL}. "
                f"Make sure Ollama is running locally. ({e})"
            ) from e

        try:
            envelope = json.loads(body)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Ollama returned an invalid response: {e}") from e

        text = envelope.get("response")
        if not text:
            raise RuntimeError("Ollama returned no response content.")

        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Ollama returned invalid JSON in its response: {e}") from e

        return {
            "summary": data.get("summary", ""),
            "key_factors": data.get("key_factors", []),
            "risks": data.get("risks", []),
            "opportunities": data.get("opportunities", []),
            "recommendations": data.get("recommendations", []),
        }

    @staticmethod
    def _resolve_model() -> str:
        return llm_config.get("providers", {}).get("ollama", {}).get("model") or DEFAULT_MODEL

    @staticmethod
    def _build_prompt(agent_name, reasoning_context) -> str:
        return (
            f"You are acting as the {agent_name} agent in a strategic analysis system.\n\n"
            f"Reasoning context (JSON):\n{json.dumps(reasoning_context, indent=2)}\n\n"
            "Analyze the question using the provided context and respond with a JSON object "
            "containing exactly these fields: summary (string), key_factors (array of strings), "
            "risks (array of strings), opportunities (array of strings), "
            "recommendations (array of strings)."
        )
