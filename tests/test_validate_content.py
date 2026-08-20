from validate_content_module import problems_in


def test_rejects_dash_punctuation_in_public_copy():
    assert problems_in("One thought — another thought.")
    assert problems_in("One thought - another thought.")


def test_allows_markdown_list_markers_and_compound_words():
    text = "- policy-first copy\n- evidence-backed records\n"

    assert problems_in(text) == []
