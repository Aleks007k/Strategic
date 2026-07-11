"""
Strategic AI Core Backend
Memory retriever
"""

import re
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

    def get_relevant_memories(self, question: str, limit: int = 5) -> list:
        keywords = self._extract_keywords(question)
        if not keywords:
            return []

        files = []
        for cat in VALID_CATEGORIES:
            folder = MEMORY_DIR / cat
            if not folder.exists():
                continue
            files.extend(f for f in folder.iterdir() if f.is_file() and f.name != ".gitkeep")

        scored = []
        for f in files:
            with open(f, "r", encoding="utf-8") as file:
                content = file.read()
            score = self._score(content, keywords)
            if score > 0:
                scored.append((score, f.stat().st_mtime, content))

        scored.sort(key=lambda item: (item[0], item[1]), reverse=True)

        return [content for _, _, content in scored[:limit]]

    @staticmethod
    def _extract_keywords(question: str) -> list:
        words = re.findall(r"\w+", question.lower())
        return list(dict.fromkeys(words))

    @staticmethod
    def _score(content: str, keywords: list) -> int:
        lowered = content.lower()
        return sum(1 for keyword in keywords if keyword in lowered)
