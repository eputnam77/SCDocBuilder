import pytest

from faa_sc_filler.ai_editor import apply_editorial_review


@pytest.mark.parametrize(
    "level,input_text,expected",
    [
        ("minimal", "  hello   world  ", "hello world"),
        (
            "basic",
            "hello world. second sentence",
            "Hello world. Second sentence",
        ),
        ("full", "hello world", "HELLO WORLD"),
    ],
)
def test_editor_levels(level: str, input_text: str, expected: str) -> None:
    data = {
        "{Summary}": input_text,
        "{Other}": "keep",
    }
    result = apply_editorial_review(data, level=level, model="Mock")
    assert result["{Summary}"] == expected
    assert result["{Other}"] == "keep"
