from passlib.context import CryptContext
# Import CryptContext to handle password hashing
# NOTE: Used to securely store passwords instead of plain text

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Create a CryptContext configured to use bcrypt
# NOTE: bcrypt is slow by design → protects against brute-force attacks
# NOTE: deprecated="auto" automatically upgrades old hashes if needed

def hash_password(password: str) -> str:
    # Function to hash a plain-text password
    # NOTE: Always hash passwords before saving them to the database

    return pwd_context.hash(password)
    # Hash the password and return the hashed value
    # NOTE: The output is safe to store in the database

def verify(plain_password, hashed_password):
    # Function to verify a plain password against a hashed one
    # NOTE: Used during login to check user credentials

    return pwd_context.verify(plain_password, hashed_password)
    # Compares plain password with stored hash
    # NOTE: Returns True if match, False otherwise


# NOTE: Never store passwords in plain text
# NOTE: Never compare passwords using == 
# NOTE: Always use verify() for login authentication
# NOTE: bcrypt hashes include salt automatically
