from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal, TypedDict, TypeIs

if TYPE_CHECKING:
    from collections.abc import Callable

# ruff: noqa: N801

# MQE types -------------------------------------------------


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


class POSTRequestData(TypedDict):
    pass


class HardQuotaString(TypedDict):
    size: int
    unit: Literal["GB", "TB"]


class ModifyBucketOptions(POSTRequestData, total=False):
    description: str
    fullyQualifiedName: str
    hardQuota: HardQuotaString
    name: str
    owner: str
    replicationEnabled: bool
    searchEnabled: bool
    softQuota: int  # Must be between 10 and 95, inclusive.
    id: str


class ModifyBucketOptionsTHQ(POSTRequestData, total=False):
    """
    THQ = Transformed Hard Quota
    """

    description: str
    fullyQualifiedName: str
    hardQuota: str
    name: str
    owner: str
    replicationEnabled: bool
    searchEnabled: bool
    softQuota: int  # Must be between 10 and 95, inclusive.
    id: str


NonStandardType = HardQuotaString
StandardType = str | int | bool
StandardTypeDict = dict[str, StandardType]


def is_type[T](_: Any, t1: type[T], t2: type[T]) -> TypeIs[T]:  # noqa: ANN401
    return t1 == t2


def value_is_StandardType(value: Any) -> TypeIs[StandardType]:  # noqa: ANN401
    """
    Type narrowing function for :py:type:`StandardType`.
    """
    return isinstance(value, StandardType)


def from_POSTRequestData_to_dict(
    options: POSTRequestData,
    transformation_functions: dict[
        str, Callable[[NonStandardType], StandardType]
    ],
) -> StandardTypeDict:
    """
    Helper function for turning a :py:class:`POSTRequestData` object or
    subclassed objects into a :py:type:`dict`. It achieves this by a somewhat
    *unorthodox* approach.
    """
    d: StandardTypeDict = {}
    for key, value in options.items():  # pyright: ignore[reportAssignmentType]
        value: NonStandardType | StandardType
        if value_is_StandardType(value):
            d[key] = value
        elif key in transformation_functions:
            transformation_function = transformation_functions[key]

            d[key] = transformation_function(value)

    return d


def from_ModifyBucketOptions_to_dict(
    options: ModifyBucketOptions,
) -> StandardTypeDict:
    """
    Helper function for turning a :py:class:`ModifyBucketOptions` into a
    :py:type:`dict`. It achieves this by a somewhat
    *unorthodox* approach.
    """
    return from_POSTRequestData_to_dict(
        options,
        {"hardQuota": lambda value: str(value["size"]) + " " + value["unit"]},
    )


def from_ModifyBucketOptionsTHQ_to_dict(
    options: ModifyBucketOptionsTHQ,
) -> StandardTypeDict:
    """
    Helper function for turning a :py:class:`ModifyBucketOptionsTHQ` into a
    :py:type:`dict`. It achieves this by a somewhat
    *unorthodox* approach.
    """
    return from_POSTRequestData_to_dict(options, {})


def to_ModifyBucketOptionsTHQ(
    options: ModifyBucketOptions,
) -> ModifyBucketOptionsTHQ:
    """
    Helper function for turning a :py:class:`ModifyBucketOptions` into a
    :py:class:`ModifyBucketOptionsTHQ`. It achieves this by a somewhat
    *unorthodox* approach.
    """
    return ModifyBucketOptionsTHQ(from_ModifyBucketOptions_to_dict(options))  # pyright: ignore[reportArgumentType]


# -------------------------------------------------
