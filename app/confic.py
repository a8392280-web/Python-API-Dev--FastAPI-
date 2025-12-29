from pydantic_settings import BaseSettings
# Import BaseSettings to read environment variables automatically
# NOTE: BaseSettings lets you load values from environment variables or .env files

from pydantic import ConfigDict
# Import ConfigDict to configure Pydantic behavior
# NOTE:Used to configure how Settings behaves (instead of old class Config)


# Define application settings class
class Settings(BaseSettings):
    
    model_config = ConfigDict(env_file=".env")
    # Configure Settings to read from ".env" file
    # NOTE:This tells Pydantic: load variables from a .env file automatically

    
    database_hostname: str
    # Database host (e.g. localhost)

    
    database_port: int
    # Database port (e.g. 5432)

    
    database_username: str
    # Database username

    
    database_password: str
    # Database password

    
    database_name: str
    # Database name

    secret_key: str
    # Secret key used for JWT signing

    # NOTE: NEVER hardcode this in real projects

    
    algorithm: str
    # JWT algorithm (usually HS256)
    
    access_token_expire_minutes: int
    # Token expiration time in minutes
    # NOTE: Controls how long a user stays logged in



settings = Settings()
# Create a single settings instance

