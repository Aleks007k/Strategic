"""
Strategic AI Core Backend
Prompt loader
"""

from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parent.parent.parent / "prompts"


class PromptLoader:
    def load_prompt(self, prompt_name: str) -> str:
        path = PROMPTS_DIR / f"{prompt_name}.md"
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
