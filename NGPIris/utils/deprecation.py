from ast import Call
from functools import partial, reduce, wraps
from textwrap import wrap
from typing import TYPE_CHECKING, Any, LiteralString
from warnings import deprecated as deprecated_base

if TYPE_CHECKING:
    from collections.abc import Callable


def add_deprecation_in_doc_string[**P, R](
    function: Callable[P, R],
    deprecatation_message: str,
    deprecated_in: str,
    removed_in: str,
) -> Callable[P, R]:
    deprecation_note = """
    .. version-deprecated:: {deprecated_in}

        {deprecatation_message}
    """
    doc_string = function.__doc__
    if doc_string:
        doc_string += deprecation_note
    function.__doc__ = doc_string
    return function


def deprecated(
    deprecatation_message: str,
    deprecated_in: str = "",
    removed_in: str = "",
):
    def decorator(function: Callable):
        return add_deprecation_in_doc_string(
            function, deprecatation_message, deprecated_in, removed_in
        )

    return decorator
