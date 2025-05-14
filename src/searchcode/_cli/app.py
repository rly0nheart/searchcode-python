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
from types import SimpleNamespace

import rich_click as click

from .panels import console, print_panels
from .. import __pkg__, __version__, License
from .._lib import (
    clear_screen,
    namespace_to_dict,
    update_window_title,
)
from ..api import Searchcode

__all__ = ["cli"]
sc = Searchcode(user_agent=f"{__pkg__}-sdk/__cli")


@click.group()
@click.version_option(version=__version__, package_name=__pkg__)
def cli():
    """
    Searchcode

    Simple, comprehensive code search.
    """

    update_window_title(text="Source code search engine.")


@cli.command("license")
@click.option("--conditions", help="License terms and conditions.", is_flag=True)
@click.option("--warranty", help="License warranty.", is_flag=True)
@click.pass_context
def licence(
    ctx: click.Context, conditions: t.Optional[bool], warranty: t.Optional[bool]
):
    """
    Show license information
    """
    clear_screen()
    update_window_title(
        text="Terms and Conditions" if conditions else "Warranty" if warranty else None
    )
    if conditions:
        console.print(
            License.terms_and_conditions,
            justify="center",
        )
    elif warranty:
        console.print(
            License.warranty,
            justify="center",
        )
    else:
        click.echo(ctx.get_help())


@click.option(
    "--page", type=int, default=0, show_default=True, help="Start page number."
)
@click.option(
    "--pages",
    type=int,
    default=1,
    show_default=True,
    help="Number of pages to fetch (maximum 5). Ignored if --callback is set.",
)
@click.option(
    "--per-page",
    type=int,
    default=50,
    show_default=True,
    help="Results per page (maximum 100).",
)
@click.option(
    "--lines-of-code-lt",
    type=int,
    help="Filter to sources with fewer lines of code (0 to 10000).",
)
@click.option(
    "--lines-of-code-gt",
    type=int,
    help="Filter to sources with more lines of code (0 to 10000).",
)
@click.option("--sources", type=str, help="Comma-separated list of source filters.")
@click.option("--languages", type=str, help="Comma-separated list of language filters.")
@click.option(
    "--callback",
    type=str,
    help="Callback function for JSONP output (disables pagination).",
)
@click.option("--pretty", is_flag=True, help="Print raw JSON output.")
@click.argument("query", type=str)
@cli.command()
def search(
    query: str,
    page: int,
    pages: int,
    per_page: int,
    pretty: bool,
    lines_of_code_lt: t.Optional[int],
    lines_of_code_gt: t.Optional[int],
    languages: t.Optional[str],
    sources: t.Optional[str],
    callback: t.Optional[str],
):
    """
    Query the code index (paginated or JSONP).

    e.g., sc search "import module"
    """
    clear_screen()
    update_window_title(text=query)

    languages = languages.split(",") if languages else None
    sources = sources.split(",") if sources else None
    pages = max(1, min(pages, 5))  # limit 1 <= pages <= 5

    if callback:
        # JSONP mode = single page only
        response = sc.search(
            query=query,
            page=page,
            per_page=per_page,
            languages=languages,
            sources=sources,
            lines_of_code_lt=lines_of_code_lt,
            lines_of_code_gt=lines_of_code_gt,
            callback=callback,
        )
        print_panels(data=response)
        return

    # normal paginated search
    with console.status(f"Querying code index with [green]{query}[/]...") as status:
        results, total = _fetch_paginated_results(
            query=query,
            start_page=page,
            per_page=per_page,
            pages=pages,
            languages=languages,
            sources=sources,
            lines_of_code_lt=lines_of_code_lt,
            lines_of_code_gt=lines_of_code_gt,
            status=status,
        )

    if results:
        if not callback and not pretty:
            console.log(f"Showing {len(results)} of {total} results for '{query}'")
        if pretty:
            console.print(namespace_to_dict(obj=results))
        else:
            print_panels(data=results)
    else:
        console.log(
            f"[bold yellow]✘[/bold yellow] No results found for [bold yellow]{query}[/bold yellow]."
        )


def _fetch_paginated_results(
    query: str,
    start_page: int,
    per_page: int,
    pages: int,
    languages: t.Optional[t.List[str]],
    sources: t.Optional[t.List[str]],
    lines_of_code_lt: t.Optional[int],
    lines_of_code_gt: t.Optional[int],
    status: console.status,
) -> t.Tuple[t.List[SimpleNamespace], int]:
    """
    Fetch paginated results from the code index.

    :return: Tuple of (results list, total number of results)
    """
    all_results = []
    current_page = start_page
    total_results = 0

    for current_iteration in range(1, pages + 1):
        response = sc.search(
            query=query,
            page=current_page,
            per_page=per_page,
            languages=languages,
            sources=sources,
            lines_of_code_lt=lines_of_code_lt,
            lines_of_code_gt=lines_of_code_gt,
            callback=None,
        )
        status.update(
            f"Getting page results on page [cyan]{current_iteration}[/] of [cyan]{pages}[/] "
            f"([cyan]{len(all_results)}[/] results collected)..."
        )

        if isinstance(response, str):
            break
        elif response.results:
            all_results.extend(response.results)
            total_results = response.total

            if len(all_results) >= response.total:
                break

            current_page += 1
        else:
            break

    return all_results, total_results


@cli.command()
@click.argument("id", type=int)
def code(id: int):
    """
    Get the raw data from a code file.

    e.g., sc code 4061576
    """
    clear_screen()
    update_window_title(text=str(id))
    with console.status(f"Getting code file [cyan]{id}[/]..."):
        data = sc.code(id)
        print_panels(data=data, id=id)
