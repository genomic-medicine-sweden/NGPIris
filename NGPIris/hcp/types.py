from typing import TypedDict

# ruff: noqa: N801


class MQE_ResultSet(TypedDict):
    """
    Typed dictionary for the `ResultSet` dictionaries inside of
    `MQE_QueryResult`.
    """

    changeTimeMilliseconds: str
    changeTimeString: str
    objectPath: str
    operation: str
    size: int


class MQE_Query(TypedDict):
    """
    Typed dictionary for the `Query` dictionary of `MQE_QueryResult`.
    """

    expression: str


class MQE_Status(TypedDict):
    """
    Typed dictionary for the `Status` dictionary of `MQE_QueryResult`.
    """

    code: str
    message: str
    results: int
    totalResults: int


class MQE_QueryResult(TypedDict):
    """
    Typed dictionary for MQE query results.
    """

    query: MQE_Query
    resultSet: list[MQE_ResultSet]
    status: MQE_Status
