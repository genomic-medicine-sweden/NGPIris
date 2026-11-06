# ruff: noqa: N801


class HCI_ResponseError(Exception):
    pass


class DataNotSuppliedToPOST(Exception):
    pass


class DataSuppliedToGET(Exception):
    pass


class IndexNotFound(Exception):
    pass
