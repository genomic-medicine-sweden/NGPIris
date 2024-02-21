
import base64
import hashlib

def base64_hashing(string : str) -> str:
    return (base64.b64encode(string.encode('ascii'))).decode('UTF-8')

def md5_hashing(string : str) -> str:
    return hashlib.md5(string.encode('ascii')).hexdigest()