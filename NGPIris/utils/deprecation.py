from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


def __add_deprecation_in_doc_string[**P, R](
    function: Callable[P, R],
    deprecation_message: str,
    deprecated_in: str,
) -> Callable[P, R]:
    deprecation_note = (
        "\n.. deprecated:: "
        + deprecated_in
        + "\n"
        + "   "
        + deprecation_message
        + "\n"
    )
    doc_string = function.__doc__
    if doc_string:
        new_doc_string = deprecation_note + doc_string
        function.__doc__ = new_doc_string
    return function


def _add_deprecation_in_doc_string[**P, R](
    deprecation_message: str,
    deprecated_in: str = "[Unknown]",
) -> Callable[..., Callable[P, R]]:
    """
    Decorator for adding deprecation message to API documentation.

    :param deprecation_message: Deprecation message
    :param deprecated_in: Version where the object was deprecated
    """

    def decorator(function: Callable[P, R]) -> Callable[P, R]:
        return __add_deprecation_in_doc_string(
            function, deprecation_message, deprecated_in
        )

    return decorator
