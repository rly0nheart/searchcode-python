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

import os
import subprocess
import typing as t

import rich_click as click
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.pretty import pprint
from rich.syntax import Syntax
from whats_that_code.election import guess_language_all_methods

from . import License, __pkg__, __version__
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

    __update_window_title("Source code search engine.")


@cli.command("license")
@click.option("--conditions", help="License terms and conditions.", is_flag=True)
@click.option("--warranty", help="License warranty.", is_flag=True)
def licence(conditions: t.Optional[bool], warranty: t.Optional[bool]):
    """
    Show license
    """
    __clear_screen()
    __update_window_title(
        text="Terms and Conditions" if conditions else "Warranty" if warranty else None
    )
    if conditions:
        console.print(
            License.terms_and_conditions,
            justify="center",
            style="on #272822",  # monokai themed background :)
        )
    if warranty:
        console.print(
            License.warranty,
            justify="center",
            style="on #272822",
        )


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
    __clear_screen()
    __update_window_title(text=query)

    with console.status(f"Querying code index with [green]{query}[/]"):
        languages = languages.split(",") if languages else None
        sources = sources.split(",") if sources else None

        results = sc.search(
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
            __print_jsonp(jsonp=results)
            if callback
            else (
                pprint(results)
                if pretty
                else __print_panels(data=results.get("results"))
            )
        )


@cli.command()
@click.argument("id", type=int)
def code(id: int):
    """
    Get the raw data from a code file.

    e.g., sc code 4061576
    """
    __clear_screen()
    __update_window_title(text=str(id))
    with console.status(f"Retrieving code data for [cyan]{id}[/]") as status:
        code_data = sc.code(id)
        if code_data:
            status.update("Determining code language")
            language = guess_language_all_methods(code=code_data)
            syntax = Syntax(code=code_data, lexer=language, line_numbers=True)
            console.print(syntax)


def __print_jsonp(jsonp: str) -> None:
    """
    Pretty-prints a raw JSONP string.

    :param jsonp: A complete JSONP string.
    """
    syntax = Syntax(jsonp, "text", line_numbers=True)
    console.print(syntax)


def __print_panels(data: t.List[t.Dict]):
    """
    Render a list of code records as rich panels with syntax highlighting.
    Line numbers are preserved and displayed alongside code content.

    :param data: A list of dictionaries, where each dictionary represents a code record
    """

    def extract_code_string_with_linenumbers(lines_dict: t.Dict[str, str]) -> str:
        """
        Convert a dictionary of line_number: code_line into a single
        multiline string sorted by line number.

        Each line is right-aligned to maintain visual alignment in output.

        :param lines_dict: Dictionary where keys are line numbers (as strings) and values are lines of code.
        :return: Multiline string with original line numbers included.
        """
        sorted_lines = sorted(lines_dict.items(), key=lambda x: int(x[0]))
        numbered_lines = [
            f"{line_no.rjust(4)} {line.rstrip()}" for line_no, line in sorted_lines
        ]
        return "\n".join(numbered_lines)

    for item in data:
        filename = item.get("filename", "Unknown")
        repo = item.get("repo", "Unknown")
        language = item.get("language", "text")
        lines_count = item.get("linescount", "??")

        code_string = extract_code_string_with_linenumbers(
            lines_dict=item.get("lines", {})
        )

        syntax = Syntax(
            code=code_string, lexer=language, word_wrap=False, indent_guides=True
        )

        panel = Panel(
            renderable=syntax,
            box=box.ROUNDED,
            title=f"[bold]{filename}[/] ([blue]{repo}[/]) {language} ⸱ [cyan]{lines_count}[/] lines",
            highlight=True,
        )

        console.print(panel)


def __update_window_title(text: str):
    """
    Update the current window title with the specified text.

    :param text: Text to update the window with.
    """
    console.set_window_title(f"{__pkg__.capitalize()} - {text}")


def __clear_screen():
    """
    Clear the screen.

    Not using console.clear() because it doesn't really clear the screen.
    It instead creates a space between the items on top and below,
    then moves the cursor to the items on the bottom, thus creating the illusion of a "cleared screen".

    Using subprocess might be a bad idea, but I'm yet to see how bad of an idea that is.
    """
    subprocess.run(["cls" if os.name == "nt" else "clear"])
