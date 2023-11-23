from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    # Postgres
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None
    POSTGRES_PORT: Optional[str] = None
    POSTGRES_HOST: Optional[str] = None
    DEBUG: Optional[bool] = False

    # Email
    COURSE_EMAIl: Optional[str] = None
    COURSE_EMAIL_PASSWORD: Optional[str] = None

    # Jwt
    ACCESS_TOKEN_EXPIRES_IN_DAYS: int = 30
    REFRESH_TOKEN_EXPIRES_IN_DAYS: int = 30
    JWT_ALGORITHM: Optional[str] = None
    JWT_SECRET_KEY: Optional[str] = None

    # Pusher
    PUSHER_APP_ID: Optional[str] = None
    PUSHER_KEY: Optional[str] = None
    PUSHER_SECRET: Optional[str] = None
    PUSHER_CLUSTER: Optional[str] = None
    PUSHER_SSL: Optional[bool] = True

    # Channels
    GENERAL_CHANNEL: Optional[str] = "general-channel"
    ALL_CHANNEL: Optional[str] = "all-channel"

    # Cloud
    CLOUD_NAME: Optional[str] = None
    API_KEY: Optional[str] = None
    API_SECRET: Optional[str] = None

    # blockchain
    WEB3_PROVIDER: Optional[str] = None
    ADDRESS_CONTRACT_ACTOR_MANAGER: Optional[str] = None
    ADDRESS_CONTRACT_PRODUCT_MANAGER: Optional[str] = None
    ADDRESS_CONTRACT_SUPPLY_CHAIN: Optional[str] = None
    PRIVATE_KEY_SYSTEM: Optional[str] = None
    CHAIN_ID: Optional[str] = 421613
    HASH_KEY: Optional[str] = None

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
