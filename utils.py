import hashlib

def hash_password(password: str) -> str:
    """Return SHA256 hash of a password"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its SHA256 hash"""
    return hash_password(password) == hashed
