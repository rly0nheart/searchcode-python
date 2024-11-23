import searchcode as sc


def test_filter_by_language():
    search = sc.code_search(query="fn main()", languages=["Rust", "Go"])
    for result in search.results:
        assert result.filename.endswith(".rs") or result.filename.endswith(".go")
        assert result.language in ["Rust", "Go"]


def test_filter_by_extension():
    search = sc.code_search(query="gsub ext:erb")
    for result in search.results:
        assert result.filename.endswith(".erb")


def test_code_result():
    code = sc.code_result(4061576)
    assert isinstance(code, str)
    assert "This file is part of Quake III Arena source code" in code


def test_related_results():
    related = sc.related_results(4061576)
    assert isinstance(related, list)
    assert len(related) == 0
