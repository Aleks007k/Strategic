"""
Strategic AI Core Backend
Anthropic LLM provider
"""

import json

import anthropic

from config import ANTHROPIC_API_KEY, llm_config
from engines.providers.base_provider import BaseProvider

DEFAULT_MODEL = "claude-opus-4-8"

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "key_factors": {"type": "array", "items": {"type": "string"}},
        "risks": {"type": "array", "items": {"type": "string"}},
        "opportunities": {"type": "array", "items": {"type": "string"}},
        "recommendations": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["summary", "key_factors", "risks", "opportunities", "recommendations"],
    "additionalProperties": False,
}


class AnthropicProvider(BaseProvider):
    def generate_analysis(self, llm_input: dict) -> dict:
        if not ANTHROPIC_API_KEY:
            raise RuntimeError(
                "ANTHROPIC_API_KEY is not set. "
                "Set this environment variable to use the Anthropic provider."
            )

        agent_name = llm_input.get("agent")
        reasoning_context = llm_input.get("reasoning_context") or {}
        model = llm_config.get("providers", {}).get("anthropic", {}).get("model", DEFAULT_MODEL)
        prompt = self._build_prompt(agent_name, reasoning_context)

        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

        try:
            response = client.messages.create(
                model=model,
                max_tokens=1024,
                output_config={"format": {"type": "json_schema", "schema": RESPONSE_SCHEMA}},
                messages=[{"role": "user", "content": prompt}],
            )
        except anthropic.APIError as e:
            raise RuntimeError(f"Anthropic API request failed: {e}") from e

        text = next((block.text for block in response.content if block.type == "text"), None)
        if text is None:
            raise RuntimeError("Anthropic API returned no text content.")

        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Anthropic API returned invalid JSON: {e}") from e

        return {
            "summary": data.get("summary", ""),
            "key_factors": data.get("key_factors", []),
            "risks": data.get("risks", []),
            "opportunities": data.get("opportunities", []),
            "recommendations": data.get("recommendations", []),
        }

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
