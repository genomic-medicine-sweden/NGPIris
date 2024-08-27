class VPNConnectionError(Exception):
    pass

class BucketNotFound(Exception):
    pass

class NoBucketMounted(Exception):
    pass

class ObjectAlreadyExist(Exception):
    pass

class DownloadLimitReached(Exception):
    pass

class NotADirectory(Exception):
    pass