<p align="center">
<img src="https://searchcode.com/static/searchcode_logo.png" width=300><br><strong>Searchcode SDK</strong>: Python library and CLI utility for <a href="https://searchcode.com">Searchcode</a>.<br><i>Simple, comprehensive code search.</i></p>
<p align="center"></p>

```commandline
searchcode search "import module"
```

Or simply:

```commandline
sc search "import module"
```

```python
from pprint import pprint
from searchcode import Searchcode

sc = Searchcode(user_agent="My-Searchcode-script")
search = sc.search(query="import module")

pprint(search)
```

## Installation

```bash

pip install searchcode
```

## Getting Started

### Code Search Without Filters

#### Command-Line Interface

```commandline
searchcode "import module"
```

#### In Code

```python
from pprint import pprint
from searchcode import Searchcode

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
from searchcode import Searchcode

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
from searchcode import Searchcode

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
from searchcode import Searchcode

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
from searchcode import Searchcode

sc = Searchcode(user_agent="My-Searchcode-script")
search = sc.search(query="import module", callback="myCallback")

pprint(search)
```

### Params

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

from searchcode import Searchcode

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
