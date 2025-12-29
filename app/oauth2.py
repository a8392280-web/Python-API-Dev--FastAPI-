from jose import JWTError, jwt
# Import JWTError and jwt for encoding/decoding JSON Web Tokens
# NOTE: python-jose is commonly used with FastAPI for JWT auth

from datetime import datetime, timedelta, timezone
# Import datetime utilities for token expiration handling
# NOTE: timezone.utc avoids timezone-related bugs

from . import schemas, models, sqlalchemy_setup
# Import internal schemas, models, and database setup
# NOTE: schemas is used for TokenData
# NOTE: models is used to query User table

from fastapi import Depends, HTTPException, status
# Depends → dependency injection
# HTTPException → raise auth-related errors
# status → HTTP status codes

from fastapi.security.oauth2 import OAuth2PasswordBearer
# OAuth2PasswordBearer extracts token from Authorization header
# NOTE: Expects header: Authorization: Bearer <token>

from sqlalchemy.orm import Session
# Import Session type for database session typing

from .confic import settings
# Import settings from config file

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# Define OAuth2 scheme with token URL
# NOTE: tokenUrl must match your login endpoint path

SECRET_KEY = settings.secret_key
# Secret key used to sign JWTs
# NOTE: Keep this secret and never commit it to public repos

ALGORITHM = settings.algorithm
# Algorithm used for JWT encoding/decoding
# NOTE: HS256 is symmetric (same key for encode/decode)

ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
# Token expiration time in minutes
# NOTE: Shorter expiry improves security

def create_access_token(data: dict):
    # Function to create a JWT access token
    # NOTE: data usually contains user_id

    to_encode = data.copy()
    # Copy data to avoid mutating original dict
    # NOTE: Prevents side effects

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Calculate expiration time
    # NOTE: Stored in UTC for consistency

    to_encode.update({"exp": expire})
    # Add expiration time to token payload
    # NOTE: JWT automatically checks this during decoding

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # Encode payload into JWT string
    # NOTE: Signed using SECRET_KEY

    return encoded_jwt
    # Return encoded JWT token

def verify_access_token(token: str, credentials_exception):
    # Function to verify and decode JWT token
    # NOTE: credentials_exception is raised on failure

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Decode JWT using secret key and algorithm
        # NOTE: Automatically validates expiration

        id: str = payload.get("user_id")
        # Extract user_id from token payload
        # NOTE: This should match the ID stored during login

        if id is None:
            raise credentials_exception
            # Raise error if token payload is invalid
            # NOTE: Prevents malformed tokens

        token_data = schemas.TokenData(id=id)
        # Create TokenData schema instance
        # NOTE: Used for type safety and validation

    except JWTError:
        raise credentials_exception
        # Catch any JWT decoding errors
        # NOTE: Includes expired or tampered tokens
    
    return token_data
    # Return validated token data

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(sqlalchemy_setup.get_db)
):
    # Dependency to get the currently authenticated user
    # NOTE: Used to protect routes

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # Predefined exception for auth failures
    # NOTE: Required header for OAuth2 standard

    token_data = verify_access_token(token, credentials_exception)
    # Verify token and extract user data
    # NOTE: Raises exception if token is invalid

    user = db.query(models.User).filter(
        models.User.id == token_data.id
    ).first()
    # Query database for user with ID from token
    # NOTE: If user was deleted, this returns None

    return user
    # Return authenticated user
    # NOTE: Can be injected into protected routes


# NOTE: JWT stores user_id, not sensitive data
# NOTE: Tokens expire automatically based on "exp"
# NOTE: OAuth2PasswordBearer reads token from Authorization header
# NOTE: get_current_user is used to protect routes
# NOTE: Always raise the same auth error for security
