
# -------------- Parsing exceptions --------------

class NotAValidTenant(Exception):
    """
    The given tenant name is not valid.
    """


class UnableToParseEndpoint(Exception):
    """
    The given endpoint URL was not correctly parsed.
    """


# -------------- Bucket exceptions --------------
class NoBucketMounted(Exception):
    """
    No bucket has been mounted before using a method that require it.
    """


class BucketNotFound(Exception):
    """
    The bucket could not be found.
    """


class BucketForbidden(Exception):
    """
    The credentials used do not have permission to reach this bucket.
    """


# -------------- Bucket object exceptions --------------

class ObjectAlreadyExist(Exception):
    """
    The object already exist on the mounted bucket.
    """


class ObjectDoesNotExist(Exception):
    """
    The object does not exist on the mounted bucket.
    """


class IsFolderObject(Exception):
    """
    The object on the mounted bucket is a folder.
    """


class SubfolderException(Exception):
    """
    There is at least one subfolder in the given path on the mounted bucket.
    """


class DownloadLimitReached(Exception):
    """
    Download limit was reached while downloading file objects from the
    mounted bucket.
    """


# -------------- File system exceptions --------------

class NotADirectory(Exception):
    """
    The given file system path is not a directory
    """


class UnallowedCharacter(Exception):
    """
    A character that is not allowed was used.
    """

