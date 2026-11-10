from dataclasses import dataclass
from typing import Literal

from icecream import ic
from parse import Result, compile, parse


@dataclass(frozen=True)
class QueryString:
    """
    An abstract class representing a query string.

    For more information: https://lucene.apache.org/core/2_9_4/queryparsersyntax.html
    """

    def to_str(self) -> str:
        """
        Method for turning a :py:class:`QueryString` into a string.
        """
        return ""

    def __and__(self: QueryString, other: QueryString) -> QueryString:
        """
        Definition of the :py:obj:`&` operator as on instance of
        :py:obj:`Operator("AND", self, other)`.
        """
        return Operator("AND", self, other)

    def __or__(self: QueryString, other: QueryString) -> QueryString:
        """
        Definition of the :py:obj:`|` operator as on instance of
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
        Method for turning a :py:class:`~NGPIris.hci.query_string.Field` into a
        string.
        """
        return self.field_name + ":" + '"' + str(self.value) + '"'


@dataclass(frozen=True)
class Operator(QueryString):
    """
    Class representing an operator in the query string. Valid operators are
    :py:obj:`"AND"` and :py:obj:`"OR"`.

    Using :py:obj:`&` and :py:obj:`|` is preferable to using the class
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
        """
        Method for turning a :py:class:`Operator` into a string.
        """
        return (
            "("
            + self.left.to_str()
            + " "
            + self.operator
            + " "
            + self.right.to_str()
            + ")"
        )


_Field_parse_format = "Field({},{})"
_Operator_parse_format = "Operator({},{},{})"
_AND_parse_format = "{} & {}"
_OR_parse_format = "{} | {}"

_parse_formats = [
    _Field_parse_format,
    _Operator_parse_format,
    _AND_parse_format,
    _OR_parse_format,
]

_compiled_parse_formats = [
    compile(parse_format) for parse_format in _parse_formats
]


def str_to_QueryString(s: str) -> QueryString:
    fields_and_operators = s.split(" ")

    qs = QueryString()
    for field_or_operator in fields_and_operators:
        ic(field_or_operator)
        for compiled_parse_format in _compiled_parse_formats:
            result = compiled_parse_format.parse(field_or_operator)
            if type(result) is Result:
                ic(result, compiled_parse_format)

    return qs
