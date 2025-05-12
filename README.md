<p align="center"><img src="https://searchcode.com/static/searchcode_logo.png" width=300 height=60><br>Python SDK and CLI utility for <a href="https://searchcode.com">Searchcode</a>.<br><i>Simple, comprehensive code search.</i></p>
<p align="center"></p>

---

```commandline
searchcode search "import module"
```

Or simply:

```commandline
sc search "import module"
```

```python
from pprint import pprint
from src.searchcode import Searchcode

sc = Searchcode(user_agent="My-Searchcode-script")
search = sc.search(query="import module")

pprint(search)
```

## Installation

```bash

pip install searchcode
```

## Getting Started

### Code Search

Queries the code index and returns at most 100 results.

#### Params

- `query`: Search term (required).
    - The following filters are textual and can be added into query directly
        - Filter by file extention **ext:EXTENTION** e.g., _"gsub ext:erb"_
        - Filter by language **lang:LANGUAGE** e.g., _"import lang:python"_
        - Filter by repository **repo:REPONAME** e.g., _"float Q_rsqrt repo:quake"_
        - Filter by user/repository **repo:USERNAME/REPONAME** e.g., _"batf repo:boyter/batf"_
- `page`: Result page starting at 0 through to 49
- `per_page`: Number of results wanted per page (max 100).
- `languages`: List of programming languages to filter by.
- `sources`: List of code sources (e.g., GitHub, BitBucket).
- `lines_of_code_gt`: Filter to sources with greater lines of code than supplied int. Valid values 0 to 10000.
- `lines_of_code_lt`: Filter to sources with less lines of code than supplied int. Valid values 0 to 10000.
- `callback`: Callback function (JSONP only)

> If the results list is empty, then this indicates that you have reached the end of the available results.

> To fetch all results for a given query, keep incrementing `page` parameter until you get a page with an empty results
> list.
---

### Code Search Without Filters

#### Command-Line Interface

```commandline
searchcode "import module"
```

#### In Code

```python
from pprint import pprint
from src.searchcode import Searchcode

sc = Searchcode(user_agent="My-Searchcode-script")
search = sc.search(query="import module")

pprint(search)
```

---

### Filter by Language (Java and JavaScript)

#### Command-Line Interface

````commandline
searchcode "import module" --languages java,javascript
````

#### In Code

```python
from pprint import pprint
from src.searchcode import Searchcode

sc = Searchcode(user_agent="My-Searchcode-script")
search = sc.search(query="import module", languages=["Java", "JavaScript"])

for result in search.results:
    pprint(result.language)
```

___

### Filter by Source (BitBucket and CodePlex)

#### Command-Line Interface

```commandline
searchcode "import module" --sources bitbucket,codeplex
```

#### In Code

```python
from pprint import pprint
from src.searchcode import Searchcode

sc = Searchcode(user_agent="My-Searchcode-script")
search = sc.search(query="import module", sources=["BitBucket", "CodePlex"])

for result in search.results:
    pprint(result.filename)
```

___

### Filter by Lines of Code (Between 500 and 1000)

#### Command-Line Interface

```commandline
searchcode "import module" --lines-of-code-gt 500 --lines-of-code-lt 1000
```

#### In Code

```python
from pprint import pprint
from src.searchcode import Searchcode

sc = Searchcode(user_agent="My-Searchcode-script")
search = sc.search(query="import module", lines_of_code_gt=500, lines_of_code_lt=1000)

for result in search.results:
    pprint(result)
```

___

### With Callback Function (JSONP only)

#### Command-Line Interface

```commandline
searchcode "import module" --callback myCallback
```

#### In Code

```python
from pprint import pprint
from src.searchcode import Searchcode

sc = Searchcode(user_agent="My-Searchcode-script")
search = sc.search(query="import module", callback="myCallback")

pprint(search)
```

`

### Response Attribute Definitions

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

___

### Code Result

Returns the raw data from a code file given the code id which can be found as the `id` in a code search result.

#### Command-Line Interface

```commandline
searchode code 4061576
```

#### In Code

#### Params

- `_id`: Unique identifier for the code file (required).

```python

from src.searchcode import Searchcode

sc = Searchcode(user_agent="My-Searchcode-script")
data = sc.code(4061576)

print(data.language)
print(data.code)
```

---

## About Searchcode

Searchcode is a simple, comprehensive source code search engine that indexes billions of lines of code from open-source
projects,
helping you find real world examples of functions, API's and libraries in 243 languages across 10+ public code sources.

[Learn more](https://searchcode.com/about)

## Credits

This SDK is developed and maintained by [Ritchie Mwewa](https://gravatar.com/rly0nheart), in collaboration
with [Ben Boyter](https://boyter.org/about/), the creator of [Searchcode.com](https://searchcode.com).
