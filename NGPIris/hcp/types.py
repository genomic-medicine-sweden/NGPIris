from typing import TypedDict


class MQE_QueryResult(TypedDict, extra_items=str):  # noqa: N801
    """
    Typed dictionary for MQE query results. It uses recursive typing in order to
    keeping the structure of the dictionary general.
    """

    resultSet: list[MQE_QueryResult]
    status: MQE_QueryResult
