from passlib.context import CryptContext
import bcrypt

print(f"Bcrypt version: {getattr(bcrypt, '__version__', 'unknown')}")
try:
    print(f"Bcrypt __about__: {getattr(bcrypt, '__about__', 'missing')}")
except Exception as e:
    print(f"Error accessing bcrypt.__about__: {e}")

try:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed = pwd_context.hash("testpassword")
    print(f"Hashed: {hashed}")
except Exception as e:
    import traceback
    traceback.print_exc()
