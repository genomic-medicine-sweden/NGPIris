class UnattachedBucketError(Exception):
    """Raise on trying to perform actions on bucket without first attaching."""


class LocalFileExistsError(Exception):
    """Raise on trying to overwrite existing local file."""


class UnknownSourceTypeError(Exception):
    """Raise on trying to get size of unknown object type."""


class MismatchChecksumError(Exception):
    """Raise on local and remote checksums differing."""
