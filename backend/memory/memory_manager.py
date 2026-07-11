"""
Strategic AI Core Backend
Memory manager
"""

from pathlib import Path

MEMORY_DIR = Path(__file__).resolve().parent.parent.parent / "memory"

VALID_CATEGORIES = {"conversations", "decisions", "insights"}


class MemoryManager:
    def save_memory(self, category: str, filename: str, content: str) -> None:
        path = self._resolve_path(category, filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    def load_memory(self, category: str, filename: str) -> str:
        path = self._resolve_path(category, filename)
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def _resolve_path(self, category: str, filename: str) -> Path:
        if category not in VALID_CATEGORIES:
            raise ValueError(f"Unknown memory category: {category}")
        return MEMORY_DIR / category / filename
