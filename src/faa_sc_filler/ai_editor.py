import logging
from typing import Dict

logger = logging.getLogger(__name__)

ALLOWED_FIELDS = {"{Summary}", "{Description}", "{SpecialConditions}"}


class AIEditor:
    """Simple AI editorial rewrite stub."""

    def __init__(self, model: str = "OpenAI") -> None:
        self.model = model

    def review(self, text: str, level: str) -> str:
        logger.debug("Applying %s review using model %s", level, self.model)
        cleaned = text.strip()
        if level == "basic":
            return cleaned.capitalize()
        if level == "full":
            return cleaned.upper()
        return cleaned


def apply_editorial_review(
    replacements: Dict[str, str], level: str, model: str
) -> Dict[str, str]:
    """Apply editorial review to allowed fields only."""
    editor = AIEditor(model=model)
    for field in ALLOWED_FIELDS:
        if field in replacements and replacements[field]:
            replacements[field] = editor.review(replacements[field], level)
    return replacements
