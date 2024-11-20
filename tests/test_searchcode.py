import searchcode as sc


def test_code_search():
    search = sc.code_search(query="fn main()", per_page=10, languages=["Rust", "Go"])
    assert len(search.results) >= 10
    for result in search.results:
        assert result.filename.endswith(".rs") or result.filename.endswith(".go")
        assert result.language in ["Rust", "Go"]


def test_code_result():
    code_result = sc.code_result(id=4061576)
    assert isinstance(code_result, str)
    assert "This file is part of Quake III Arena source code" in code_result


def test_related_results():
    related = sc.related_results(id=4061576)
    assert isinstance(related, list)
    assert len(related) == 0
