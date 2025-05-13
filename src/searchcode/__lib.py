import os
import subprocess
import typing as t
from types import SimpleNamespace

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from . import __pkg__, __version__

console = Console(highlight=True)


def print_jsonp(jsonp: str) -> None:
    """
    Pretty-prints a raw JSONP string.

    :param jsonp: A complete JSONP string.
    """
    syntax = Syntax(jsonp, "text", line_numbers=True)
    console.print(syntax)


def print_panels(data: t.List[SimpleNamespace]):
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
        filename = item.filename
        repo = item.repo
        language = item.language
        lines_count = item.linescount
        lines = item.lines

        code_string = extract_code_string_with_linenumbers(lines_dict=lines.__dict__)

        syntax = Syntax(
            code=code_string,
            lexer=language,
            word_wrap=False,
            indent_guides=True,
            theme="dracula",
        )

        panel = Panel(
            renderable=syntax,
            box=box.ROUNDED,
            title=f"[bold]{filename}[/] ([blue]{repo}[/]) {language} ⸱ [cyan]{lines_count}[/] lines",
            highlight=True,
        )

        console.print(panel)


def update_window_title(text: str):
    """
    Update the current window title with the specified text.

    :param text: Text to update the window with.
    """
    console.set_window_title(f"{__pkg__.capitalize()} v{__version__} - {text}")


def clear_screen():
    """
    Clear the screen.

    Not using console.clear() because it doesn't really clear the screen.
    It instead creates a space between the items on top and below,
    then moves the cursor to the items on the bottom, thus creating the illusion of a "cleared screen".

    Using subprocess might be a bad idea, but I'm yet to see how bad of an idea that is.
    """
    subprocess.run(["cls" if os.name == "nt" else "clear"])
