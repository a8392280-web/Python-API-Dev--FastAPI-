import token
# Import token module (Python standard library)
# NOTE: This import is not used here and can be safely removed

from fastapi import APIRouter, Depends, status, HTTPException, Response
# APIRouter → create modular route groups
# Depends → dependency injection
# status → HTTP status codes
# HTTPException → raise HTTP errors
# Response → customize HTTP responses
# NOTE: Response is not used in this file and can be removed

from fastapi.security.oauth2 import OAuth2PasswordRequestForm
# Import OAuth2 form for username/password login
# NOTE: Expects form-data, not JSON

from sqlalchemy.orm import Session
# Import Session type for database session typing

from .. import sqlalchemy_setup, schemas, models, utiles, oauth2
# Import internal application modules
# NOTE: utiles likely contains password hashing utilities
# NOTE: oauth2 handles JWT token creation/verification

router = APIRouter(tags=["Authentication"])
# Create router for authentication-related endpoints
# NOTE: tags group endpoints in Swagger UI

@router.post("/login", response_model=schemas.Token)
# POST endpoint for user login
# NOTE: response_model ensures only token data is returned

def login(
    user_credetials: OAuth2PasswordRequestForm = Depends(),
    # Extract login data from form fields (username & password)
    # NOTE: username field is used instead of email by OAuth2 spec

    db: Session = Depends(sqlalchemy_setup.get_db)
    # Inject database session
    # NOTE: Session is automatically closed after request
):
    user = db.query(models.User).filter(
        models.User.email == user_credetials.username
    ).first()
    # Query database for user with matching email
    # NOTE: OAuth2PasswordRequestForm uses "username" field

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
        # Raise error if user does not exist
        # NOTE: Same error message prevents user enumeration

    if not utiles.verify(user_credetials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
        # Verify plain password against hashed password
        # NOTE: Never compare passwords using ==

    # create token:-
    # NOTE: Token will be used for authenticated requests

    access_token = oauth2.create_access_token(
        data={"user_id": user.id}
    )
    # Generate JWT access token
    # NOTE: user_id is stored inside token payload

    # return token:
    # NOTE: Client must store this token and send it in headers

    return {
        "token": access_token,
        "token_type": "bearer"
    }
    # Return token response
    # NOTE: "bearer" is required for Authorization header


# NOTE: OAuth2PasswordRequestForm expects form-data, not JSON
# NOTE: username field is used even if you authenticate by email
# NOTE: Always return the same error for invalid credentials
# NOTE: JWT token contains user_id, not sensitive data
# NOTE: Client must send token as: Authorization: Bearer <token>
