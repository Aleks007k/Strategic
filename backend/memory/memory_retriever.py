"""
Strategic AI Core Backend
Memory retriever
"""

from pathlib import Path

MEMORY_DIR = Path(__file__).resolve().parent.parent.parent / "memory"

VALID_CATEGORIES = ["conversations", "decisions", "insights"]


class MemoryRetriever:
    def get_recent_memories(self, category: str = None, limit: int = 5) -> list:
        categories = [category] if category else VALID_CATEGORIES

        files = []
        for cat in categories:
            folder = MEMORY_DIR / cat
            if not folder.exists():
                continue
            files.extend(f for f in folder.iterdir() if f.is_file() and f.name != ".gitkeep")

        files.sort(key=lambda f: f.stat().st_mtime, reverse=True)

        memories = []
        for f in files[:limit]:
            with open(f, "r", encoding="utf-8") as file:
                memories.append(file.read())

        return memories
