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
            "assumptions": data.get("assumptions", []),
            "confidence": data.get("confidence"),
        }

    @staticmethod
    def _resolve_model() -> str:
        return llm_config.get("providers", {}).get("ollama", {}).get("model") or DEFAULT_MODEL

    @staticmethod
    def _build_prompt(agent_name, reasoning_context) -> str:
        return (
            f"You are acting as the {agent_name} agent in a strategic analysis system.\n\n"
            f"Reasoning context (JSON):\n{json.dumps(reasoning_context, indent=2)}\n\n"
            "Before producing your analysis, reason through the mission in this order:\n"
            "1. Understand the mission question, goal, and constraints.\n"
            "2. Identify the load-bearing assumptions the analysis depends on. Write each "
            "assumption as a falsifiable statement, and avoid trivial assumptions that "
            "would not change the conclusion if they turned out to be false.\n"
            "3. Identify the key factors that most influence the outcome.\n"
            "4. Generate risks, each linked to a key factor.\n"
            "5. Generate opportunities, each linked to a key factor.\n"
            "6. Write the summary after this reasoning is complete.\n"
            "7. Estimate your confidence after the analysis is complete.\n\n"
            "Respond with a JSON object containing exactly these fields: "
            "summary (string), key_factors (array of strings), "
            "risks (array of strings), opportunities (array of strings), "
            "assumptions (array of strings), confidence (number between 0 and 1)."
        )
