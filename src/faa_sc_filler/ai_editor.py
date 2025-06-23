"""Helper utilities for optional AI-style editorial review."""

from __future__ import annotations

import logging
import re
from enum import Enum, auto
from typing import Dict, Iterable, List

logger = logging.getLogger(__name__)

ALLOWED_FIELDS = {"{Summary}", "{Description}", "{SpecialConditions}"}


class EditType(Enum):
    """Supported editorial edit operations."""

    STRIP = auto()
    NORMALIZE_SPACES = auto()
    CAPITALIZE_SENTENCES = auto()
    UPPERCASE = auto()


EDITOR_LEVELS: Dict[str, List[EditType]] = {
    "minimal": [EditType.STRIP, EditType.NORMALIZE_SPACES],
    "basic": [EditType.STRIP, EditType.NORMALIZE_SPACES, EditType.CAPITALIZE_SENTENCES],
    "full": [
        EditType.STRIP,
        EditType.NORMALIZE_SPACES,
        EditType.CAPITALIZE_SENTENCES,
        EditType.UPPERCASE,
    ],
}


class AIEditor:
    """Apply simple rule-based editorial cleanups."""

    def __init__(self, model: str = "OpenAI") -> None:
        self.model = model

    @staticmethod
    def _apply_edits(text: str, edits: Iterable[EditType]) -> str:
        result = text
        for edit in edits:
            if edit is EditType.STRIP:
                result = result.strip()
            elif edit is EditType.NORMALIZE_SPACES:
                result = re.sub(r"\s+", " ", result)
            elif edit is EditType.CAPITALIZE_SENTENCES:
                sentences = re.split(r"(?<=[.!?])\s+", result)
                result = " ".join(s.strip().capitalize() for s in sentences)
            elif edit is EditType.UPPERCASE:
                result = result.upper()
        return result

    def review(self, text: str, level: str) -> str:
        logger.debug("Applying %s review using model %s", level, self.model)
        edits = EDITOR_LEVELS.get(level, EDITOR_LEVELS["minimal"])
        return self._apply_edits(text, edits)


def apply_editorial_review(
    replacements: Dict[str, str], level: str, model: str
) -> Dict[str, str]:
    """Apply editorial review to allowed fields only."""
    editor = AIEditor(model=model)
    for field in ALLOWED_FIELDS:
        if field in replacements and replacements[field]:
            replacements[field] = editor.review(replacements[field], level)
    return replacements
