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

import typing as t
from platform import python_version, platform
from types import SimpleNamespace

import requests

from ._lib import dict_to_namespace
from .filters import LANGUAGES, SOURCES, get_language_ids, get_source_ids

__all__ = ["Searchcode"]


class Searchcode:
    def __init__(self, user_agent: str):
        self.user_agent = user_agent
        self.__base_api_endpoint: str = "https://searchcode.com/api"

    def search(
        self,
        query: str,
        page: int = 0,
        per_page: int = 100,
        languages: t.Optional[t.List[LANGUAGES]] = None,
        sources: t.Optional[t.List[SOURCES]] = None,
        lines_of_code_gt: t.Optional[int] = None,
        lines_of_code_lt: t.Optional[int] = None,
        callback: t.Optional[str] = None,
    ) -> t.Union[SimpleNamespace, str]:
        """
        Searches and returns code snippets matching the query.

        The following filters are textual and can be added into query directly:
        ----------------------------------------------------------------------
            - Filter by file extention `ext:EXTENTION` E.g. `"gsub ext:erb"`
            - Filter by language `lang:LANGUAGE` E.g. `"import lang:python"`
            - Filter by repository `repo:REPONAME` E.g. `"float Q_rsqrt repo:quake"`
            - Filter by user/repository `repo:USERNAME/REPONAME` E.g. `"batf repo:boyter/batf"`

        :param query: Search term
        :type query: str
        :param page: Result page starting at 0 through to 49 (default is 0).
        :type page: int
        :param per_page: Number of results wanted per page max 100 (default is 100)
        :type per_page: int
        :param languages: Allows filtering to languages supplied by return types.
          Supply multiple to filter to multiple languages.
        :type languages: Optional[List[CODE_LANGUAGES]]
        :param sources: Allows filtering to sources supplied by return types.
          Supply multiple to filter to multiple sources.
        :type sources: Optional[List[CODE_SOURCES]]
        :param lines_of_code_gt: Filter to sources with greater lines of code than supplied int. Valid values 0 to 10000.
        :type lines_of_code_gt: int
        :param lines_of_code_lt: Filter to sources with fewer lines of code than supplied int. Valid values 0 to 10000.
        :type lines_of_code_lt: int
        :param callback: Callback function (JSONP only)
        :type callback: str
        :return: The search results as a Dict object.
        :rtype: Dict
        """

        language_ids = (
            [] if not languages else get_language_ids(language_names=languages)
        )
        source_ids = [] if not sources else get_source_ids(source_names=sources)

        response = self.__send_request(
            endpoint=f"{self.__base_api_endpoint}/{'jsonp_codesearch_I' if callback else 'codesearch_I'}/",
            params=[
                ("q", query),
                ("p", page),
                ("per_page", per_page),
                ("loc", lines_of_code_gt),
                ("loc2", lines_of_code_lt),
                ("callback", callback),
                *[("lan", language_id) for language_id in language_ids],
                *[("src", source_id) for source_id in source_ids],
            ],
            callback=callback,
        )

        if not callback:
            response = dict_to_namespace(obj=response)
            response.results = response.results[:per_page]

        return response

    def code(self, __id: int) -> SimpleNamespace:
        """
        Returns the raw data from a code file given the code ID which can be found as the `id` in a code search result.

        :param __id: The unique identifier of the code result.
        :type __id: int
        :return: SimpleNamespace object containing code file data.
        :rtype: SimpleNamespace
        """

        response = self.__send_request(
            endpoint=f"{self.__base_api_endpoint}/result/{__id}"
        )
        return dict_to_namespace(obj=response)

    # This is deprecated (for now).
    # def related(_id: int) -> Dict:
    #    """
    #    Returns an array of results given a searchcode unique code id which are considered to be duplicates.
    #
    #    The matching is slightly fuzzy allowing so that small differences between files are ignored.

    #    :param _id: The unique identifier of the code result.
    #    :type _id: int
    #    :return: A list of related results as a dictobject.
    #    :rtype: Dict
    #    """

    #    response = _get_response(endpoint=f"{_BASE_API_ENDPOINT}/related_results/{_id}")
    #    return _response_to_namespace_obj(response=response)

    def __send_request(
        self,
        endpoint: str,
        params: t.Optional[t.List[t.Tuple[str, str]]] = None,
        callback: str = None,
    ) -> t.Union[t.Dict, t.List, str]:
        """
        (Private function) Sends a GET request to the specified endpoint with the given headers and parameters.

        :param endpoint: The API endpoint to send the request to.
        :type endpoint: str
        :param params: Optional list of query parameters as key-value tuples.
        :type params: Optional[List[Tuple[str, str]]]
        :return: The parsed JSON response, which could be a dictionary, list, or string.
        :rtype: Union[Dict, List, str]
        :raises Exception: If the request fails or the server returns an error.
        """

        response = requests.get(
            url=endpoint,
            params=params,
            headers={
                "User-Agent": f"{self.user_agent.replace(' ', '-')} "
                f"(Python {python_version} on {platform}; +https://pypi.org/project/searchcode)"
            },
        )
        response.raise_for_status()
        return response.text if callback else response.json()
