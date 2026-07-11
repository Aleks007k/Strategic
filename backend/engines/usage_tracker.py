"""
Strategic AI Core Backend
LLM usage tracker
"""


class UsageTracker:
    def __init__(self):
        self.records = []

    def record_usage(self, provider: str, model: str, input_tokens: int, output_tokens: int) -> None:
        self.records.append({
            "provider": provider,
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
        })

    def get_total_usage(self) -> dict:
        return {
            "total_requests": len(self.records),
            "total_input_tokens": sum(r["input_tokens"] for r in self.records),
            "total_output_tokens": sum(r["output_tokens"] for r in self.records),
        }
