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

import rich_click as click
from rich.console import Console
from rich.pretty import pprint
from rich.syntax import Syntax

from . import License
from .__lib import (
    __pkg__,
    __version__,
    update_window_title,
    clear_screen,
    print_jsonp,
    print_panels,
)
from .api import Searchcode

sc = Searchcode(user_agent=f"{__pkg__}-sdk/cli")

__all__ = ["cli"]

console = Console(highlight=True)


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


@cli.command()
@click.argument("query", type=str)
@click.option("--pretty", help="Return results in raw JSON format.", is_flag=True)
@click.option(
    "--page",
    type=int,
    default=0,
    help="Start page (defaults to 0).",
)
@click.option(
    "--per-page",
    type=int,
    default=100,
    help="Results per page (defaults to 100).",
)
@click.option(
    "--lines-of-code-lt",
    type=int,
    help="Filter to sources with less lines of code than the supplied value (Valid values: 0 to 10000).",
)
@click.option(
    "--lines-of-code-gt",
    type=int,
    help="Filter to sources with greater lines of code than the supplied value (Valid values: 0 to 10000).",
)
@click.option(
    "--sources",
    type=str,
    help="A comma-separated list of code sources to filter results.",
)
@click.option(
    "--languages",
    type=str,
    help="A comma-separated list of code languages to filter results.",
)
@click.option(
    "--callback",
    type=str,
    help="callback function (returns JSONP)",
)
def search(
    query: str,
    page: int = 0,
    per_page: int = 100,
    pretty: bool = False,
    lines_of_code_lt: t.Optional[int] = None,
    lines_of_code_gt: t.Optional[int] = None,
    languages: t.Optional[str] = None,
    sources: t.Optional[str] = None,
    callback: t.Optional[str] = None,
):
    """
    Query the code index (returns 100 results by default).

    e.g., sc search "import module"
    """
    clear_screen()
    update_window_title(text=query)

    with console.status(
        f"Querying code index with search string: [green]{query}[/]..."
    ):
        languages = languages.split(",") if languages else None
        sources = sources.split(",") if sources else None

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

        (
            print_jsonp(jsonp=response)
            if callback
            else (pprint(response) if pretty else print_panels(data=response.results))
        )


@cli.command()
@click.argument("id", type=int)
def code(id: int):
    """
    Get the raw data from a code file.

    e.g., sc code 4061576
    """
    clear_screen()
    update_window_title(text=str(id))
    with console.status(f"Fetching data for code file with ID: [cyan]{id}[/]..."):
        data = sc.code(id)
        lines = data.code
        language = data.language
        if lines:
            syntax = Syntax(
                code=lines, lexer=language, line_numbers=True, theme="dracula"
            )
            console.print(syntax)
