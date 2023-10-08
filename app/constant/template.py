from enum import Enum


class NotificationTemplate(Enum):
    CRUD_PRODUCT_NOTIFICATION_MSG = lambda product_type, product_name, action, user_name: f"The {product_name} {product_type} has just been {action} by {user_name} <span style=\"background: linear-gradient(to right, #7AF4AE 0%, #3262DD 100%);-webkit-background-clip: text; background-clip: text; color: transparent; font-weight: bold;\"></span>"
