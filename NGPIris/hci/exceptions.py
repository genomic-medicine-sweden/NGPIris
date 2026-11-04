# ruff: noqa: N801


class HCI_ResponseError(Exception):
    """
    General Response Error from the HCI.
    """


class DataNotSuppliedToPOSTError(Exception):
    """
    Data was not supplied to a POST request.
    """


class DataSuppliedToGETError(Exception):
    """
    Data was supplied to a GET request.
    """


class IndexNotFoundError(Exception):
    """
    The HCI index could not be found.
    """
