import os
import subprocess
import typing as t
from types import SimpleNamespace


def namespace_to_dict(
    obj: t.Union[SimpleNamespace, t.List[SimpleNamespace]],
) -> t.Union[t.Dict, t.List[t.Dict], SimpleNamespace, t.List[SimpleNamespace]]:
    """
    Recursively convert a SimpleNamespace object and any nested namespaces into a dictionary.

    :param obj: The object to convert. It can be a SimpleNamespace, list, dictionary, or any other type.
    :type obj: Union[SimpleNamespace, List[SimpleNamespace]]
    :return: A dictionary (or list, or primitive type) suitable for JSON serialization.
    :rtype: Union[Dict, List[Dict], SimpleNamespace, List[SimpleNamespace]]
    """
    if isinstance(obj, SimpleNamespace):
        return {key: namespace_to_dict(value) for key, value in vars(obj).items()}
    elif isinstance(obj, list):
        return [namespace_to_dict(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: namespace_to_dict(value) for key, value in obj.items()}
    else:
        return obj


def dict_to_namespace(
    obj: t.Union[t.List[t.Dict], t.Dict],
) -> t.Union[t.List[SimpleNamespace], SimpleNamespace, t.List[t.Dict], t.Dict]:
    """
    Recursively converts the API response into a SimpleNamespace object(s).

    :param obj: The object to convert, either a dictionary or a list of dictionaries.
    :type obj: Union[List[Dict], Dict]
    :return: A SimpleNamespace object or list of SimpleNamespace objects.
    :rtype: Union[List[SimpleNamespace], SimpleNamespace, List[Dict], Dict]
    """

    if isinstance(obj, t.Dict):
        return SimpleNamespace(
            **{key: dict_to_namespace(obj=value) for key, value in obj.items()}
        )
    elif isinstance(obj, t.List):
        return [dict_to_namespace(obj=item) for item in obj]
    else:
        return obj


def update_window_title(text: str):
    """
    Update the current window title with the specified text.

    :param text: Text to update the window with.
    """
    from . import __pkg__, __version__
    from ._cli.panels import console

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
