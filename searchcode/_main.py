from types import SimpleNamespace
from typing import List, Union, Dict, Optional, Tuple

import requests

from ._filters import (
    CODE_SOURCES,
    CODE_LANGUAGES,
    get_language_ids,
    get_source_ids,
)

__all__ = ["code_result", "code_search", "related_results"]


_BASE_API_ENDPOINT = "https://searchcode.com/api"


def _get_response(
    endpoint: str,
    headers: Optional[Dict] = None,
    params: Optional[List[Tuple[str, str]]] = None,
) -> Union[Dict, List, str]:
    """
    Sends a GET request to the specified endpoint with the given headers and parameters.

    :param endpoint: The API endpoint to send the request to.
    :type endpoint: str
    :param headers: Optional HTTP headers to include in the request.
    :type headers: Optional[Dict]
    :param params: Optional list of query parameters as key-value tuples.
    :type params: Optional[List[Tuple[str, str]]]
    :return: The parsed JSON response, which could be a dictionary, list, or string.
    :rtype: Union[Dict, List, str]
    :raises Exception: If the request fails or the server returns an error.
    """

    try:
        response = requests.get(url=endpoint, params=params, headers=headers)
        response.raise_for_status()
        return response.json()

    except Exception as e:
        raise e


def _object_to_namespace(
    obj: Union[List[Dict], Dict]
) -> Union[List[SimpleNamespace], SimpleNamespace, List[Dict], Dict]:
    """
    Recursively converts dictionaries and lists of dictionaries into SimpleNamespace objects.

    :param obj: The object to convert, either a dictionary or a list of dictionaries.
    :type obj: Union[List[Dict], Dict]
    :return: A SimpleNamespace object or list of SimpleNamespace objects.
    :rtype: Union[List[SimpleNamespace], SimpleNamespace, None]
    """

    if isinstance(obj, Dict):
        return SimpleNamespace(
            **{key: _object_to_namespace(obj=value) for key, value in obj.items()}
        )
    elif isinstance(obj, List):
        return [_object_to_namespace(obj=item) for item in obj]
    else:
        return obj


def code_search(
    query: str,
    page: int = 0,
    per_page: int = 100,
    languages: Optional[List[CODE_LANGUAGES]] = None,
    sources: Optional[List[CODE_SOURCES]] = None,
    lines_of_code: Optional[int] = None,
    lines_of_code2: Optional[int] = None,
    callback: Optional[str] = None,
) -> SimpleNamespace:
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
    :param lines_of_code: Filter to sources with greater lines of code then supplied int. Valid values 0 to 10000.
    :type lines_of_code: int
    :param lines_of_code2: Filter to sources with fewer lines of code then supplied int. Valid values 0 to 10000.
    :type lines_of_code2: int
    :param callback: Callback function (JSONP only)
    :type callback: str
    :return: The search results as a SimpleNamespace object.
    :rtype: SimpleNamespace
    """

    language_ids = [] if not languages else get_language_ids(language_names=languages)
    source_ids = [] if not sources else get_source_ids(source_names=sources)

    response = _get_response(
        endpoint=f"{_BASE_API_ENDPOINT}/codesearch_I/",
        params=[
            ("q", query),
            ("p", page),
            ("per_page", per_page),
            ("loc", lines_of_code),
            ("loc2", lines_of_code2),
            ("callback", callback),
            *[("lan", language_id) for language_id in language_ids],
            *[("src", source_id) for source_id in source_ids],
        ],
    )

    return _object_to_namespace(obj=response)


def code_result(id: int) -> SimpleNamespace:
    """
    Returns the raw data from a code file given the code ID which can be found as the `id` in a code search result.

    :param id: The unique identifier of the code result.
    :type id: int
    :return: The code result details as a SimpleNamespace object.
    :rtype: SimpleNamespace
    """

    response = _get_response(endpoint=f"{_BASE_API_ENDPOINT}/result/{id}")
    return response.get("code")


def related_results(id: int) -> SimpleNamespace:
    """
    Returns an array of results given a searchcode unique code id which are considered to be duplicates.

    The matching is slightly fuzzy allowing so that small differences between files are ignored.

    :param id: The unique identifier of the code result.
    :type id: int
    :return: A list of related results as a SimpleNamespace object.
    :rtype: SimpleNamespace
    """

    response = _get_response(endpoint=f"{_BASE_API_ENDPOINT}/related_results/{id}")
    return _object_to_namespace(obj=response)
