
class NoBucketMounted(Exception):
    pass

class BucketNotFound(Exception):
    pass

class BucketForbidden(Exception):
    pass

class ObjectAlreadyExist(Exception):
    pass

class ObjectDoesNotExist(Exception):
    pass

class DownloadLimitReached(Exception):
    pass

class NotADirectory(Exception):
    pass

class NotAValidTenant(Exception):
    pass

class UnableToParseEndpoint(Exception):
    pass

class UnallowedCharacter(Exception):
    pass

class IsFolderObject(Exception):
    pass

class SubfolderException(Exception):
    pass