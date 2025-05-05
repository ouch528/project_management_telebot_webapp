import hashlib

def hash_chat_title(title: str) -> str:
    return hashlib.sha256(title.encode('utf-8')).hexdigest()