"""
Strategic AI Core Backend
Input analysis engine
"""

from core.information_gap import InformationGap

REQUIRED_INFORMATION = [
    "budget",
    "timeframe",
    "risk tolerance",
    "priorities",
    "success criteria",
]

CONTEXT_FIELDS = [
    "facts",
    "preferences",
    "constraints",
    "previous_decisions",
    "relevant_history",
]

QUESTION_TEMPLATE = "What is your {item}?"
_TEMPLATE_PREFIX, _TEMPLATE_SUFFIX = QUESTION_TEMPLATE.split("{item}")

TOPIC_FIELD_MAP = {
    "budget": "constraints",
    "timeframe": "constraints",
    "risk tolerance": "preferences",
    "priorities": "preferences",
    "success criteria": "facts",
}

DEFAULT_FIELD = "facts"


class InputAnalysisEngine:
    def analyze(self, question: str, context=None, goal=None) -> dict:
        information_gap = InformationGap()
        known_text = self._build_known_text(context)

        for item in REQUIRED_INFORMATION:
            if item not in known_text:
                information_gap.add_missing_information(item)

        return {
            "question": question,
            "context": context,
            "goal": goal,
            "information_gap": information_gap,
        }

    @staticmethod
    def _build_known_text(context) -> str:
        if not isinstance(context, dict):
            return ""

        values = []
        for field in CONTEXT_FIELDS:
            values.extend(context.get(field) or [])

        return " ".join(str(value) for value in values).lower()

    @staticmethod
    def build_question(item: str) -> str:
        return QUESTION_TEMPLATE.format(item=item)

    @staticmethod
    def extract_topic(question: str):
        if not isinstance(question, str):
            return None

        if not question.startswith(_TEMPLATE_PREFIX) or not question.endswith(_TEMPLATE_SUFFIX):
            return None

        return question[len(_TEMPLATE_PREFIX):len(question) - len(_TEMPLATE_SUFFIX)]

    @staticmethod
    def map_topic_to_field(topic: str) -> str:
        return TOPIC_FIELD_MAP.get(topic, DEFAULT_FIELD)

    @classmethod
    def map_question_to_field(cls, question: str):
        topic = cls.extract_topic(question)
        if topic is None:
            return None

        return cls.map_topic_to_field(topic)
