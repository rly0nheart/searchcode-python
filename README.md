<p align="center"><img src="https://github.com/user-attachments/assets/d28934e1-a1ab-4b6e-9d12-d64067a65a60"><br>Python SDK for <a href="https://searchcode.com">Searchcode</a>.<br><i>Search 75 billion lines of code from 40 million projects</i></p>
<p align="center"></p>
<p align="center">
  <a href="https://github.com/knewkarma-io/knewkarma"><img alt="Code Style" src="https://img.shields.io/badge/code%20style-black-000000?logo=github&link=https%3A%2F%2Fgithub.com%2Frly0nheart%2Fknewkarma"></a>
</p>

## Installation

```bash

pip install searchcode

```

## Documentation

### Code Search

Query the code index with optional filters

#### Params

- `query`: Search term (required).
    - The following filters are textual and can be added into query directly
        - Filter by file extention **ext:EXTENTION** e.g., _"gsub ext:erb"_
        - Filter by language **lang:LANGUAGE** e.g., _"import lang:python"_
        - Filter by repository **repo:REPONAME** e.g., _"float Q_rsqrt repo:quake"_
        - Filter by user/repository **repo:USERNAME/REPONAME** e.g., _"batf repo:boyter/batf"_
- `page`: Page number for paginated results.
- `per_page`: Number of results wanted per page (max 100).
- `languages`: List of programming languages to filter by.
- `sources`: List of code sources (e.g., GitHub, BitBucket).
- `lines_of_code_gt`: Filter to sources with greater lines of code than supplied int. Valid values 0 to 10000.
- `lines_of_code_lt`: Filter to sources with less lines of code than supplied int. Valid values 0 to 10000.
- `callback`: Callback function (JSONP only)

#### Code Search Without Filters

```python

import searchcode as sc

search = sc.code_search(query="test")

for result in search.results:
    print(result)
```

#### Filter by Language (Java and JavaScript)

```python

import searchcode as sc

search = sc.code_search(query="test", languages=["Java", "JavaScript"])

for result in search.results:
    print(result.language)
```

#### Filter by Source (BitBucket and CodePlex)

```python

import searchcode as sc

search = sc.code_search(query="test", sources=["BitBucket", "CodePlex"])

for result in search.results:
    print(result.filename)
```

#### Filter by Lines of Code (Between 500 and 1000)

```python

import searchcode as sc

search = sc.code_search(query="test", lines_of_code_gt=500, lines_of_code_lt=1000)

for result in search.results:
    print(result)
```

#### With Callback Function (JSONP only)

```python
import searchcode as sc

search = sc.code_search(query="test", callback="myCallback")
print(search)
```

#### Response Attribute Definitions

| Attribute            | Description                                                                                                                                                                                               |
|----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **searchterm**       | Search term supplied to the API through the use of the `q` parameter.                                                                                                                                     |
| **query**            | Identical to `searchterm` and included for historical reasons to maintain backward compatibility.                                                                                                         |
| **matchterm**        | Identical to `searchterm` and included for historical reasons to maintain backward compatibility.                                                                                                         |
| **page**             | ID of the current page that the query has returned. This is a zero-based index.                                                                                                                           |
| **nextpage**         | ID of the offset of the next page. Always set to the current page + 1, even if you have reached the end of the results. This is a zero-based index.                                                       |
| **previouspage**     | ID of the offset of the previous page. If no previous page is available, it will be set to `null`. This is a zero-based index.                                                                            |
| **total**            | The total number of results that match the `searchterm` in the index. Note that this value is approximate. It becomes more accurate as you go deeper into the results or use more filters.                |
| **language_filters** | Returns an array containing languages that exist in the result set.                                                                                                                                       |
| **id**               | Unique ID for this language used by searchcode, which can be used in other API calls.                                                                                                                     |
| **count**            | Total number of results that are written in this language.                                                                                                                                                |
| **language**         | The name of this language.                                                                                                                                                                                |
| **source_filters**   | Returns an array containing sources that exist in the result set.                                                                                                                                         |
| **id**               | Unique ID for this source used by searchcode, which can be used in other API calls.                                                                                                                       |
| **count**            | Total number of results that belong to this source.                                                                                                                                                       |
| **source**           | The name of this source.                                                                                                                                                                                  |
| **results**          | Returns an array containing the matching code results.                                                                                                                                                    |
| **id**               | Unique ID for this code result used by searchcode, which can be used in other API calls.                                                                                                                  |
| **filename**         | The filename for this file.                                                                                                                                                                               |
| **repo**             | HTML link to the location of the repository where this code was found.                                                                                                                                    |
| **linescount**       | Total number of lines in the matching file.                                                                                                                                                               |
| **location**         | Location inside the repository where this file exists.                                                                                                                                                    |
| **name**             | Name of the repository that this file belongs to.                                                                                                                                                         |
| **language**         | The identified language of this result.                                                                                                                                                                   |
| **url**              | URL to searchcode's location of the file.                                                                                                                                                                 |
| **md5hash**          | Calculated MD5 hash of the file's contents.                                                                                                                                                               |
| **lines**            | Contains line numbers and lines which match the `searchterm`. Lines immediately before and after the match are included. If only the filename matches, up to the first 15 lines of the file are returned. |

### Code Result

Returns the raw data from a code file given the code id which can be found as the `id` in a code search result.

#### Params

- `_id`: Unique identifier for the code file (required).

```python

import searchcode as sc

code = sc.code_result(123456)
print(code)
```

### Related Results

Returns an array of results given a searchcode unique code id which are considered to be duplicates.

#### Params

- `_id`: Unique identifier for the code file (required).

```python

import searchcode as sc

related = sc.related_results(123456)
print(related)
```

#### Response Attribute Definitions

| Attribute      | Description                                                                              |
|----------------|------------------------------------------------------------------------------------------|
| **reponame**   | Name of the repository which this related result belongs to.                             |
| **source**     | The source which this code result comes from.                                            |
| **sourceurl**  | URL to the repository this result belongs to.                                            |
| **md5hash**    | Calculated MD5 hash of the file's contents.                                              |
| **location**   | Location inside the repository where this file exists.                                   |
| **language**   | Name of the language which this file is identified to be.                                |
| **linescount** | Total number of lines in this file.                                                      |
| **id**         | Unique ID for this code result used by searchcode, which can be used in other API calls. |
| **filename**   | The filename for this file.                                                              |

## About Searchcode

Searchcode is a simple, comprehensive source code search engine that indexes billions of lines of code from open-source
projects,
helping you find real world examples of functions, API's and libraries in 243 languages across 10+ public code sources.

[Learn more](https://searchcode.com/about)

## Acknowledgements

This SDK is developed and maintained by [Richard Mwewa](https://gravatar.com/rly0nheart), in collaboration
with [Ben Boyter](https://boyter.org/about/), the creator of [Searchcode.com](https://searchcode.com).
