"""
QueryString := Term | Operator
Term := Field : Value
Operator := QueryString AND QueryString | QueryString OR QueryString
.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal


class QueryString(ABC):
    """
    An abstract class representing a query string.

    For more information: https://lucene.apache.org/core/2_9_4/queryparsersyntax.html
    """

    @abstractmethod
    def to_str(self) -> str:
        """
        Method for turning a :py:class:`QueryString` into a string.
        """

    def __and__(self: QueryString, other: QueryString) -> QueryString:
        """
        Definition of the :py:meth:`&` operator as on instance of
        :py:obj:`Operator("AND", self, other)`.
        """
        return Operator("AND", self, other)

    def __or__(self: QueryString, other: QueryString) -> QueryString:
        """
        Definition of the :py:meth:`|` operator as on instance of
        :py:obj:`Operator("OR", self, other)`.
        """
        return Operator("OR", self, other)


@dataclass(frozen=True)
class Field(QueryString):
    """
    Class representing a field query.
    For example, if the index has a field "Chromosome"
    and we wish to make a query for all entries where "Chromosome" is "X",
    we write of query string as ``Chromosome:"X"`` which is equivalent to
    :py:obj:`Field("Chromosome", "X").to_str()`.

    For more information: https://lucene.apache.org/core/2_9_4/queryparsersyntax.html
    """

    field_name: str
    value: str | int

    def to_str(self) -> str:
        """
        Method for turning a :py:class:`Field` into a string.
        """
        return self.field_name + ":" + '"' + str(self.value) + '"'


@dataclass(frozen=True)
class Operator(QueryString):
    """
    Class representing an operator in the query string. Valid operators are
    :py:obj:`"AND"` and :py:obj:`"OR"`.

    Using :py:meth:`&` and :py:meth:`|` is preferable to using the class
    constructor itself for readability.

    Example:
    ::
        Field("Chromosome", "X") & Field("REF", "A") ==
        Operator(
            operator="AND",
            left=Field(
                field_name="Chromosome",
                value="X"
            ),
            right=Field(
                field_name="REF",
                value="A"
            )
        )

    For more information: https://lucene.apache.org/core/2_9_4/queryparsersyntax.html

    """

    operator: Literal["AND", "OR"]
    left: QueryString
    right: QueryString

    def to_str(self) -> str:
        return (
            "("
            + self.left.to_str()
            + " "
            + self.operator
            + " "
            + self.right.to_str()
            + ")"
        )

