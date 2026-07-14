"""
Strategic AI Core Backend
Anthropic LLM provider
"""

import json

import anthropic

from config import ANTHROPIC_API_KEY, llm_config
from engines.providers.base_provider import BaseProvider
from engines.usage_tracker import UsageTracker

DEFAULT_MODEL = "claude-opus-4-8"

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "key_factors": {"type": "array", "items": {"type": "string"}},
        "risks": {"type": "array", "items": {"type": "string"}},
        "opportunities": {"type": "array", "items": {"type": "string"}},
        "assumptions": {"type": "array", "items": {"type": "string"}},
        "confidence": {"type": "number"},
    },
    "required": ["summary", "key_factors", "risks", "opportunities", "assumptions", "confidence"],
    "additionalProperties": False,
}


class AnthropicProvider(BaseProvider):
    def __init__(self):
        self.usage_tracker = UsageTracker()

    def generate_analysis(self, llm_input: dict) -> dict:
        if not ANTHROPIC_API_KEY:
            raise RuntimeError(
                "ANTHROPIC_API_KEY is not set. "
                "Set this environment variable to use the Anthropic provider."
            )

        agent_name = llm_input.get("agent")
        reasoning_context = llm_input.get("reasoning_context") or {}
        model = self._resolve_model()
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

        usage = getattr(response, "usage", None)
        self.usage_tracker.record_usage(
            provider="anthropic",
            model=model,
            input_tokens=getattr(usage, "input_tokens", 0) if usage else 0,
            output_tokens=getattr(usage, "output_tokens", 0) if usage else 0,
        )

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
            "assumptions": data.get("assumptions", []),
            "confidence": data.get("confidence"),
        }

    @staticmethod
    def _resolve_model() -> str:
        return llm_config.get("providers", {}).get("anthropic", {}).get("model") or DEFAULT_MODEL

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
