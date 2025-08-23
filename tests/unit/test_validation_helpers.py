import pytest
from scdocbuilder.validation import _find_question_answer

@pytest.mark.parametrize("next_para", ["2) Another question", "2- Another question"])
def test_find_question_answer_recognises_alternate_question_formats(next_para):
    paragraphs = ["Question 1:", next_para]
    assert _find_question_answer(paragraphs, 0) == ""
