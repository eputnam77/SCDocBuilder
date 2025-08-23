from __future__ import annotations

import re
from docx.document import Document

from .processing import extract_fields

MANDATORY_PLACEHOLDERS = [
    "{Applicant name}",
    "{Airplane model}",
]

MANDATORY_QUESTIONS = ["15", "16", "17"]


def _find_question_answer(paragraphs: list[str], index: int) -> str:
    """Return the answer following a question prompt.

    The worksheet can list a question followed by its answer on the same
    paragraph or on the next line. Earlier versions naively returned the next
    paragraph even if it was another question, leading to a false positive when
    a question was left unanswered. This helper now ensures that we only return
    the next paragraph if it does **not** look like another question prompt.
    """

    current = paragraphs[index].split(":", 1)
    if len(current) > 1 and current[1].strip():
        return current[1].strip()

    if index + 1 < len(paragraphs):
        nxt = paragraphs[index + 1].strip()
        if re.match(r"(Question\s+\d+|\d+\.)", nxt):
            return ""
        return nxt
    return ""


def validate_mandatory_fields(doc: Document) -> None:
    """Check worksheet for required fields and questions.

    Args:
        doc: Worksheet document to validate.

    Raises:
        ValueError: If any mandatory field or question is missing.
    """

    values = extract_fields(doc)
    for key in MANDATORY_PLACEHOLDERS:
        if not values.get(key):
            raise ValueError(f"Missing field: {key}")

    texts = [p.text.strip() for p in doc.paragraphs]
    for q in MANDATORY_QUESTIONS:
        for idx, text in enumerate(texts):
            if text.startswith(f"Question {q}") or text.startswith(f"{q}."):
                answer = _find_question_answer(texts, idx)
                if not answer:
                    raise ValueError(f"Question {q} answer missing")
                break
        else:
            raise ValueError(f"Question {q} answer missing")
