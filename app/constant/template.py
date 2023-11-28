from enum import Enum


class NotificationTemplate(Enum):
    CRUD_PRODUCT_NOTIFICATION_MSG = (lambda product_type, product_name, action, user_name:
                                     f"The {product_name} {product_type} has just been {action} by {user_name}")
    ERROR_TRANSACTION_OF_BLOCKCHAIN_NOTIFICATION_MSG = "Transaction failed with blockchain."


class ActivityTemplate(Enum):
    Activity_MSG = (lambda username, action, entity, entity_name, children_name:
                    f"{username} has {action} the {entity} {children_name} - {entity_name}")

    Activity_Purchase_MSG = (lambda action, entity, entity_name, owner:
                             f"You {action}d the {entity} from {owner} - {entity_name}")


class CommentTemplate(Enum):
    Comment_MSG = (lambda username, action, entity_name: f"{username} {action} on your post - {entity_name}")


class PurchaseProduct(Enum):
    Purchase_MSG = (lambda username, action, product_name, price:
                    f"{username} {action}d product {product_name} with a total order value of ${price}")


class ConfirmOrder(Enum):
    OrderComplete_MSG = (lambda product_name:
                         f"Your order {product_name} has just been completed. You can now create your product.")

    OrderReject_MSG = (lambda product_name:
                       f"Your order {product_name} has just been cancelled. Please contact the owner.")


class FinancialTransactionTemplate(Enum):
    Deposit_MSG = (lambda username, action, price:
                   f"{username} successfully {action}ed funds into the system, in the amount of {price}")

    Withdraw_MSG = (lambda username, action, price:
                    f"{username} requests to {action} money from the system, in the amount of {price}")
