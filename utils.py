import hashlib

def hash_password(password: str) -> str:
    """Return SHA256 hash of a password"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its SHA256 hash"""
    return hash_password(password) == hashed

# Test function to verify hashing works correctly
def test_password_hashing():
    """Test function to verify password hashing"""
    test_password = "admin123"
    hashed = hash_password(test_password)
    verified = verify_password(test_password, hashed)
    
    print(f"Test password: {test_password}")
    print(f"Hashed: {hashed}")
    print(f"Verification: {verified}")
    
    return verified

if __name__ == "__main__":
    # Run test when executed directly
    test_password_hashing()