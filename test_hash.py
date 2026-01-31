"""Test bcrypt with passlib"""
from passlib.context import CryptContext
import hashlib
import base64

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt with SHA256 pre-hashing."""
    # Pre-hash with SHA256 and encode as base64 (44 bytes)
    password_hash = hashlib.sha256(password.encode('utf-8')).digest()
    password_b64 = base64.b64encode(password_hash).decode('utf-8')
    print(f"Password length after encoding: {len(password_b64)} bytes")
    print(f"Encoded password: {password_b64}")
    return pwd_context.hash(password_b64)

# Test
try:
    password = "MyPassword123"
    print(f"Original password: {password}")
    hashed = hash_password(password)
    print(f"✅ Password hashed successfully!")
    print(f"Hash: {hashed[:60]}...")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
