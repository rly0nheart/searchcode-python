"""
Copyright (C) 2024  Ritchie Mwewa

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

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
