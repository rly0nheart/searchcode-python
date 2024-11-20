<p align="center"><img src="https://github.com/user-attachments/assets/d28934e1-a1ab-4b6e-9d12-d64067a65a60"><br>An unofficial Python SDK for <a href="https://searchcode.com">SearchCode</a>.<br><i>Search 75 billion lines of code from 40 million projects</i></p>
<p align="center"></p>
<p align="center">
  <a href="https://github.com/knewkarma-io/knewkarma"><img alt="Code Style" src="https://img.shields.io/badge/code%20style-black-000000?logo=github&link=https%3A%2F%2Fgithub.com%2Frly0nheart%2Fknewkarma"></a>
</p>

## Table Of Contents
* [Code_search](#code_search)
    * [Example (Without Filters)](#example-without-filters)
    * [Example Language Filter (Java and Javascript)](#example-language-filter-java-and-javascript)
    * [Example Source Filter (Bitbucket and CodePlex)](#example-source-filter-bitbucket-and-codeplex)
    * [Example Lines of Code Filter (Between 500 and 1000)](#example-lines-of-code-filter-between-500-and-1000)
    * [Example (JSONP)](#example-jsonp)
    * [Response Attribute Definitions](#response-attribute-definitions)
* [code_result](#code_result)
    * [Example](#example)
* [related_results](#related_results)
    * [Example](#example-1)
    * [Response Attribute Definitions](#response-attribute-definitions-1)
* [About Searchcode](#about-searchcode)
* [Credit](#credit)

***

## code_search

Queries the code index and returns at most 100 results.

> [!TIP]
All filters supported by searchcode are available. These include
`sources`, `languages` and `lines_of_code`. These work in the same way that the main page works; See the examples below for how to use them.

> [!TIP] 
To fetch all results for a given query, keep incrementing the `page` parameter until you get a page with an empty
results list.

> [!IMPORTANT]
If the results list is empty, then this indicates that you have reached the end of the available results.


### Example (Without Filters):

```python
import searchcode as sc

search = sc.code_search(query="test")

for result in search.results:
    print(result)
```

### Example Language Filter (Java and Javascript):

```python
import searchcode as sc

search = sc.code_search(query="test", languages=["Java", "JavaScript"])

for result in search.results:
    print(result.language)
```

### Example Source Filter (Bitbucket and CodePlex):

```python
import searchcode as sc

search = sc.code_search(query="test", sources=["BitBucket", "CodePlex"])

for result in search.results:
    print(result.filename)
```

### Example Lines of Code Filter (Between 500 and 1000):

```python
import searchcode as sc

search = sc.code_search(query="test", lines_of_code=500, lines_of_code2=1000)

for result in search.results:
    print(result.linescount)
```

### Example (JSONP):

```python
import searchcode as sc

search = sc.code_search(query="soup", page=1, callback="myCallback")

for result in search.results:
    print(result)
```

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

## code_result

Returns the raw data from a code file given the code id which can be found as the id in a code search result.

### Example:

```python
import searchcode as sc

result = sc.code_result(id=4061576)
print(result)
```

> Returns raw data from the code file.

## related_results

Returns an array of results given a searchcode unique code id which are considered to be duplicates. 

> [!IMPORTANT]
The matching is
slightly fuzzy allowing so that small differences between files are ignored.

### Example:

```python
import searchcode as sc

related = sc.related_results(id=4061576)
print(related)
```

### Response Attribute Definitions

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

Read more about searchcode [here](https://searchcode.com/about/)

## Credit

Special thanks to [Ben Boyter](https://boyter.org/about/), developer of [searchcode.com](https://searchcode.com)
