from searchcode import Searchcode

sc = Searchcode(user_agent="Pytest")


def test_filter_by_extension():
    search = sc.search("gsub ext:erb")
    for result in search.get("results"):
        assert result.get("filename").endswith(".erb")


def test_code_result():
    code = sc.code(4061576)
    assert isinstance(code, str)
    assert "This file is part of Quake III Arena source code" in code


# deprecated (for now)
# def test_related_results():
#    related = sc.related_results(4061576)
#    assert isinstance(related, list)
#    assert len(related) == 0
