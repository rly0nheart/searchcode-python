from types import SimpleNamespace
from typing import Optional, List

import rich_click as click
from rich import print as rprint, box
from rich.syntax import Syntax
from rich.table import Table
from whats_that_code.election import guess_language_all_methods

from .api import Searchcode

sc = Searchcode(user_agent="searchCode-sdk/cli")

__all__ = ["cli"]


@click.group()
def cli():
    """
    Searchcode CLI

    Simple, comprehensive code search.
    """
    ...


@cli.command()
@click.argument("query", type=str)
@click.option("--pretty", help="Return results in raw JSON format.", is_flag=True)
@click.option(
    "--page",
    type=int,
    default=0,
    help="Start page number (defaults to 0).",
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
def search(
    query: str,
    page: int = 0,
    per_page: int = 100,
    pretty: bool = False,
    lines_of_code_lt: Optional[int] = None,
    lines_of_code_gt: Optional[int] = None,
    languages: Optional[str] = None,
    sources: Optional[str] = None,
):
    """
    Query the code index and (returns 100 results by default).

    e.g., searchcode search "gsub ext:erb" --pretty
    """
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
    )
    if pretty:
        rprint(results)
    else:
        print_table(records=results.results, ignore_keys=["lines"])


@cli.command()
@click.argument("id", type=int)
def code(id: int):
    """
    Get the raw data from a code file.

    e.g., searchcode code 4061576
    """
    code_data = sc.code(id)
    if code_data:
        language = guess_language_all_methods(code=code_data)
        syntax = Syntax(code=code_data, lexer=language, line_numbers=True)
        rprint(syntax)


def print_table(records: List[SimpleNamespace], ignore_keys: List[str] = None) -> None:
    """
    Creates a rich table from a list of SimpleNamespace objects,
    ignoring specified keys.

    :param records: List of SimpleNamespace instances.
    :param ignore_keys: List of keys to exclude from the table.
    :return: None. Prints the table using rich.
    """
    if not records:
        raise ValueError("Data must be a non-empty list of SimpleNamespace objects.")

    ignore_keys = ignore_keys or []

    # Collect all unique keys across all records, excluding ignored ones
    all_keys = set()
    for record in records:
        all_keys.update(key for key in record.__dict__.keys() if key not in ignore_keys)

    columns = sorted(all_keys)

    table = Table(box=box.ROUNDED, highlight=True, header_style="bold")

    for index, column in enumerate(columns):
        style = "dim" if index == 0 else None
        table.add_column(column.capitalize(), style=style)

    for record in records:
        data = record.__dict__
        row = [str(data.get(column, "")) for column in columns]
        table.add_row(*row)

    rprint(table)
