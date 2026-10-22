from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


def __add_deprecation_in_doc_string[**P, R](
    function: Callable[P, R],
    deprecatation_message: str,
    deprecated_in: str,
) -> Callable[P, R]:
    deprecation_note = (
        "\n.. version-deprecated:: "
        + deprecated_in
        + "\n"
        + "   "
        + deprecatation_message
        + "\n"
    )
    doc_string = function.__doc__
    if doc_string:
        new_doc_string = deprecation_note + doc_string
        function.__doc__ = new_doc_string
    return function


def _add_deprecation_in_doc_string[**P, R](
    deprecatation_message: str,
    deprecated_in: str = "[Unknown]",
) -> Callable[..., Callable[P, R]]:
    """
    Decorator for adding deprecation message to API documentation.

    :param deprecatation_message: Deprecration message
    :param deprecated_in: Version where the object was deprecated
    """

    def decorator(function: Callable[P, R]) -> Callable[P, R]:
        return __add_deprecation_in_doc_string(
            function, deprecatation_message, deprecated_in
        )

    return decorator
