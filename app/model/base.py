from enum import Enum
from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class UserSystemRole(str, Enum):
    SUPPER_ADMIN = "SUPPER_ADMIN"
    ADMIN = "ADMIN"
    FARMER = "FARMER"
    SEEDLING_COMPANY = "SEEDLING_COMPANY"
    MANUFACTURER = "MANUFACTURER"
    MEMBER = "MEMBER"


class ProductStatus(str, Enum):
    PUBLISH = "PUBLISH"
    PRIVATE = "PRIVATE"
    CLOSE = "CLOSE"


class ProductType(str, Enum):
    FARMER = "FARMER"
    SEEDLING_COMPANY = "SEEDLING_COMPANY"
    MANUFACTURER = "MANUFACTURER"


class ProductRole(str, Enum):
    OWNER = "OWNER"
    MEMBER = "MEMBER"


class NotificationType(str, Enum):
    SYSTEM_NOTIFICATION = "SYSTEM_NOTIFICATION"
    COURSE_NOTIFICATION = "COURSE_NOTIFICATION"
    POST_NOTIFICATION = "POST_NOTIFICATION"
    COMMENT_NOTIFICATION = "COMMENT_NOTIFICATION"
