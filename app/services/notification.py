import uuid

from sqlalchemy.orm import Session

from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler
from app.core.pusher.pusher_client import PusherClient
from app.core.settings import settings
from ..constant.template import PurchaseProduct

from ..crud import crud_notification, crud_user
from ..model.base import NotificationType
from ..schemas import NotificationCreate, NotificationResponse
from app.utils.pagination import calc_skip_record_query, make_response_pagination


class NotificationService:
    def __init__(self, db: Session):
        self.db = db

    async def list_notifications(self, user_id: str, unread: bool, page: int = None, limit: int = None):
        skip_record, limit_record = calc_skip_record_query(page=page, limit=limit)
        total_notifications, list_notifications = crud_notification.list_notifications(db=self.db, user_id=user_id,
                                                                                       unread=unread,
                                                                                       skip=skip_record,
                                                                                       limit=limit_record)
        data = [NotificationResponse.from_orm(item) for item in list_notifications]
        notification_unread_total, _ = crud_notification.list_notifications_unread(db=self.db, user_id=user_id)
        meta = dict(unread_total=notification_unread_total)
        result = make_response_pagination(items=data, page=page, limit=limit, total=total_notifications, meta=meta)
        return result

    async def detail_notification(self, notification_id: str):
        current_notification = crud_notification.detail_notification(db=self.db, notifications_id=notification_id)
        if current_notification is None:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_NOTIFICATION_NOT_FOUND)
        notification = crud_notification.mark_notification_as_read(db=self.db,
                                                                   current_notification=current_notification,
                                                                   unread=False)
        return notification.data

    async def notify_entity_status(self, entity, notification_type,
                                   message_template, action, current_user=None, owner=None, price=None):
        data_push = self.create_data_notification(action, message_template,
                                                  notification_type, entity,
                                                  current_user, price=price)
        if notification_type == NotificationType.COMMENT_NOTIFICATION:
            user_id = owner.id
        elif message_template == PurchaseProduct.Purchase_MSG:
            user_id = owner
        elif notification_type == NotificationType.TRANSACTION_NOTIFICATION:
            user_id = current_user.id
        else:
            user_id = current_user.id

        request_data = NotificationCreate(id=str(uuid.uuid4()), data=data_push, user_id=user_id,
                                          notification_type=notification_type)
        await self.create_notification(request_data=request_data)

    async def multi_notify_entity_status(self, entity, notification_type, message_template, action, current_user=None):
        data_push = self.create_data_notification(action, message_template, notification_type, entity, current_user)
        list_user = crud_user.list_users(db=self.db)

        list_request_data = []
        for user in list_user["list_users"]:
            request_data = NotificationCreate(id=str(uuid.uuid4()), data=data_push, user_id=user.id,
                                              notification_type=notification_type)
            list_request_data.append(request_data)

        await self.create_multi_notification(list_request_data=list_request_data, data_push=data_push)

    @staticmethod
    def crete_data_push(message, notification_type, entity, action):
        data_push = {
            "message": message,
            "params": {
                notification_type[:-13].lower() + '_id': f'{entity.id}',
                notification_type[:-13].lower() + '_name': f'{entity.name}',
                "notification_type": notification_type,
                "action": action
            },
            "data": {
            }
        }
        return data_push

    @staticmethod
    def crete_data_push_comment(message, notification_type, entity, action):
        data_push = {
            "message": message,
            "params": {
                'marketplace_id': f'{entity.id}',
                "notification_type": notification_type,
                "action": action
            },
            "data": {
            }
        }
        return data_push

    @staticmethod
    def crete_data_push_confirm_order(message, notification_type, entity, action):
        data_push = {
            "message": message,
            "params": {
                'product_id': f'{entity.id}',
                'product_type': f'{entity.product_type}',
                "notification_type": notification_type,
                "action": action
            },
            "data": {
            }
        }
        return data_push

    @staticmethod
    def crete_data_push_financial_transaction(message, notification_type, entity, action):
        data_push = {
            "message": message,
            "params": {
                'financial_transaction_id': f'{entity.id}',
                "notification_type": notification_type,
                "action": action
            },
            "data": {
            }
        }
        return data_push

    def create_data_notification(self, action, message_template, notification_type, entity, current_user, price=None):
        if action in ['created', 'updated', 'deleted']:
            message = message_template(product_type=notification_type[:-13].lower(),
                                       product_name=entity.name,
                                       action=action,
                                       user_name=current_user.username)
            data_push = self.crete_data_push(message=message, notification_type=notification_type,
                                             entity=entity, action=action)
        elif action in ['commented']:
            message = message_template(username=current_user.username,
                                       action=action,
                                       entity_name=entity.product.name)
            data_push = self.crete_data_push_comment(message=message, notification_type=notification_type,
                                                     entity=entity, action=action)
        elif action in ["purchase"]:
            message = message_template(username=current_user.username, action=action,
                                       product_name=entity.name, price=price)
            data_push = self.crete_data_push(message=message, notification_type=notification_type,
                                             entity=entity, action=action)
        elif action in ["confirm_order"]:
            message = message_template(product_name=entity.name)
            data_push = self.crete_data_push_confirm_order(message=message, notification_type=notification_type,
                                                           entity=entity, action=action)
        elif action in ["deposit", "withdraw"]:
            message = message_template(username=current_user.username, action=action, price=price)
            data_push = self.crete_data_push_financial_transaction(message=message, notification_type=notification_type,
                                                                   entity=entity, action=action)
        else:
            data_push = []
        return data_push

    async def create_multi_notification(self, list_request_data: list, data_push: dict):
        client = PusherClient()
        notification_db = crud_notification.create_multi_notification(db=self.db, list_request_data=list_request_data)
        client.push_notification(settings.ALL_CHANNEL, f"[{settings.ALL_CHANNEL}]", data_push=data_push)
        return notification_db

    async def create_notification(self, request_data: NotificationCreate):
        client = PusherClient()
        notification_db = crud_notification.create(db=self.db, obj_in=request_data)
        data_push = crud_notification.mark_notification_as_read(db=self.db, current_notification=notification_db,
                                                                unread=notification_db.unread)

        if request_data.user_id is not None:
            client.push_notification(settings.GENERAL_CHANNEL, request_data.user_id, data_push=data_push.data)
        else:
            client.push_notification(settings.ALL_CHANNEL, f"[{settings.ALL_CHANNEL}]", data_push=data_push.data)

    async def delete_notification(self, notification_id: str):
        current_notification = crud_notification.detail_notification(db=self.db, notifications_id=notification_id)
        if current_notification is None:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_NOTIFICATION_NOT_FOUND)
        result = crud_notification.remove(db=self.db, entry_id=notification_id)
        return result
