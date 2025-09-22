import hashlib

def hash_password(password):
    """Return SHA256 hash of the password"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hashed):
    """Verify if the password matches the hashed value"""
    return hash_password(password) == hashed
