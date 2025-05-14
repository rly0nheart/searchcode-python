import typing as t
from types import SimpleNamespace

from rich.console import Group, Console
from rich.panel import Panel
from rich.rule import Rule
from rich.syntax import Syntax
from rich.text import Text

console = Console(highlight=True, log_time=False)


def _extract_code_string_with_linenumbers(lines_dict: t.Dict[str, str]) -> str:
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


def _make_syntax(code: str, language: str, **syntax_kwargs) -> Syntax:
    """
    Create a Syntax object with consistent settings.

    :param code: The source code to render.
    :type code: str
    :param language: The programming language lexer to use.
    :type language: str
    :param syntax_kwargs: Additional keyword arguments for Syntax.
    :type syntax_kwargs: Any
    :return: A rich Syntax object for displaying code.
    :rtype: Syntax
    """
    return Syntax(code=code, lexer=language, theme="dracula", **syntax_kwargs)


def _make_syntax_panel(
    syntax: Syntax, header_text: t.Optional[str] = None, add_divider: bool = False
) -> Panel:
    """
    Wrap a Syntax (or any renderable) in a styled Panel. Optionally include a header and divider.

    :param syntax: The Syntax object to display inside the Panel.
    :type syntax: Syntax
    :param header_text: Optional markup string for the header above the syntax.
    :type header_text: Optional[str]
    :param add_divider: Whether to include a horizontal rule between header and syntax.
    :type add_divider: bool
    :return: A rich Panel containing the syntax (and optional header/divider).
    :rtype: Panel
    """
    if header_text:
        header = Text.from_markup(header_text, justify="left", overflow="ellipsis")
        divider = Rule(style="#444444") if add_divider else None
        content_items = [header, divider, syntax] if divider else [header, syntax]
        content = Group(*content_items)
    else:
        content = syntax

    return Panel(renderable=content, border_style="#444444", title_align="left")


def print_panels(
    data: t.Union[t.List[SimpleNamespace], SimpleNamespace, str], **kwargs
) -> None:
    """
    Print panels for displaying code or structured file information.

    Accepts either:
      - a single SimpleNamespace with fields `code`, `language`
      - a string of raw code
      - a list of SimpleNamespace objects with fields `filename`, `repo`, `language`, `linescount`, `lines`

    :param data: The input data to display as panels.
    :type data: Union[List[SimpleNamespace], SimpleNamespace, str]
    :param kwargs: Additional optional keyword arguments (e.g., id for logging).
    :type kwargs: Any
    :return: None
    :rtype: None
    """
    panels: t.List[Panel] = []

    if isinstance(data, SimpleNamespace):
        code = data.code
        language = data.language
        if code:
            syntax = _make_syntax(code, language, line_numbers=True)
            panel = _make_syntax_panel(syntax)
            panels.append(panel)
        else:
            console.log(
                f"[bold yellow]✘[/bold yellow] No matching file found: [bold yellow]{kwargs.get('id')}[/bold yellow]."
            )
            return
    elif isinstance(data, str):
        syntax = _make_syntax(data, "text", line_numbers=True)
        panel = _make_syntax_panel(syntax)
        panels.append(panel)
    else:
        for item in data:
            filename = item.filename
            repo = item.repo
            language = item.language
            lines_count = item.linescount
            lines = item.lines

            code_string = _extract_code_string_with_linenumbers(
                lines_dict=lines.__dict__
            )

            syntax = _make_syntax(
                code=code_string, language=language, word_wrap=False, indent_guides=True
            )

            header_text = (
                f"[bold]{filename}[/] ([blue]{repo}[/]) "
                f"{language} · [cyan]{lines_count}[/] lines"
            )

            panel = _make_syntax_panel(
                syntax=syntax, header_text=header_text, add_divider=True
            )

            panels.append(panel)

    console.print(*panels)
