import pytest
from scdocbuilder.validation import _find_question_answer


@pytest.mark.parametrize("next_para", ["16) Another question", "16- Another question"])
def test_find_question_answer_recognises_alternate_question_formats(
    next_para: str,
) -> None:
    paragraphs = ["Question 1:", next_para]
    assert _find_question_answer(paragraphs, 0) == ""


def test_find_question_answer_same_line() -> None:
    paragraphs = ["Question 1: yes"]
    assert _find_question_answer(paragraphs, 0) == "yes"
