"""
Strategic AI Core Backend
Knowledge domain loader
"""

from pathlib import Path

KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent.parent / "knowledge" / "domains"


class KnowledgeLoader:
    def load_domain(self, domain_name: str) -> str:
        path = KNOWLEDGE_DIR / f"{domain_name}.md"
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
