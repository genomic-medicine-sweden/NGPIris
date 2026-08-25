from ast import Call
from functools import partial, reduce, wraps
from textwrap import wrap
from typing import TYPE_CHECKING, Any, LiteralString
from warnings import deprecated as deprecated_base

if TYPE_CHECKING:
    from collections.abc import Callable

"""
def compose[**P, R](decorators: list[Callable[P, R]]) -> Callable[P, R]:
    def decorator(f) -> R:
        for decorator_ in reversed(decorators):
            f = decorator_(f)
        return f

    return decorator

def deprecated[**P, R](function: Callable[P, R]) -> Callable[P, R]:
    @wraps(function)
    @wraps(deprecated_base)
    def decorator(*args: P.args, **kwargs: P.kwargs) -> R:
        print("hahaha")
        return function(*args, **kwargs)

    return decorator
"""

"""
def deprecated[**P, R](
    deprecatation_message,
    deprecated_in: str = "",
    removed_in: str = "",
) -> Callable[..., Callable[P, R]]:  # -> Callable[P, Callable[P, R]]:
    # f = deprecated_base(deprecatation_message)(function)
    # decorator = partial(f)
    # return decorator

    def decorator(function: Callable[P, R]) -> Callable[P, R]:
        # @wraps(function)
        @wraps(deprecated_base(deprecatation_message))
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            return function(*args, **kwargs)

        return wrapper

    return decorator
"""

"""
def compose[**P, R](functions: list[Callable[P, R]]) -> Callable[P, R]:
    def inner(args):
        for function in reversed(functions):
            args = function(args)
        return args

    return inner
    # return reduce(lambda x, y: x, functions)


def compose[R](*functions: Callable[..., R]) -> Callable[..., R]:
    def inner(args):
        for f in reversed(functions):
            args = f(args)
        return args

    return inner
"""


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
