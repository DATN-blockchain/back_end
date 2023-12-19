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
    BLOCK_EXPLORER: Optional[str] = None
    CHAIN_ID: Optional[str] = 421613
    HASH_KEY: Optional[str] = None
    # WEB3_PROVIDER = "https://goerli-rollup.arbitrum.io/rpc"
    # ADDRESS_CONTRACT_ACTOR_MANAGER ="0xADC3E1AAb3660cEf413822950101e4680d2E52C9"
    # ADDRESS_CONTRACT_PRODUCT_MANAGER = "0x17C486dc7AeCFe07acE15BD142e2bBE22892f5A2"
    # ADDRESS_CONTRACT_SUPPLY_CHAIN = "0xdA86b46a57Da7D9017Cd76B5B8fAC2Eb3f8DaA1b"
    # CHAIN_ID = 421613
    # PRIVATE_KEY_SYSTEM = "2bd81d7cace245abc1a7e981075332251823b56a136c0154187cd8a0746ed84a"

    # VNPAY CONFIG
    VNPAY_RETURN_URL: Optional[str] = None  # get from config
    VNPAY_PAYMENT_URL: Optional[str] = None  # get from config
    VNPAY_API_URL: Optional[str] = None
    VNPAY_TMN_CODE: Optional[str] = None  # Website ID in VNPAY System, get from config
    VNPAY_HASH_SECRET_KEY: Optional[str] = None  # Secret key for create checksum,get from config
    FE_REDIRECT: Optional[str] = None

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
