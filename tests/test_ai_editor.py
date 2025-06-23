from faa_sc_filler.ai_editor import apply_editorial_review


def test_apply_editorial_review_basic():
    data = {
        "{Summary}": "test summary",
        "{Description}": "description text",
        "{SpecialConditions}": "conditions",
        "{Other}": "keep",
    }
    result = apply_editorial_review(data.copy(), level="basic", model="Mock")
    assert result["{Summary}"] == "Test summary"
    assert result["{Description}"] == "Description text"
    assert result["{SpecialConditions}"] == "Conditions"
    assert result["{Other}"] == "keep"
