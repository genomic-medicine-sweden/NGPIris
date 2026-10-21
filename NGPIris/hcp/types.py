from typing import TypedDict

# ruff: noqa: N801


class MQE_ResultSet(TypedDict):
    changeTimeMilliseconds: str
    changeTimeString: str
    objectPath: str
    operation: str
    size: int


class MQE_Query(TypedDict):
    expression: str


class MQE_Status(TypedDict):
    code: str
    message: str
    results: int
    totalResults: int


class MQE_QueryResult(TypedDict):
    """
    Typed dictionary for MQE query results. It uses recursive typing in order to
    keeping the structure of the dictionary general.
    """

    query: MQE_Query
    resultSet: list[MQE_ResultSet]
    status: MQE_Status
