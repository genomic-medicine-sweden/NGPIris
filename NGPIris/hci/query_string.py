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
    @abstractmethod
    def to_str(self) -> str:
        pass

    def __and__(self: QueryString, other: QueryString) -> QueryString:
        return Operator("AND", self, other)

    def __or__(self: QueryString, other: QueryString) -> QueryString:
        return Operator("OR", self, other)


@dataclass(frozen=True)
class Term(QueryString):
    field: str
    value: str | int

    def to_str(self) -> str:
        return self.field + ":" + '"' + str(self.value) + '"'


@dataclass(frozen=True)
class Operator(QueryString):
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

