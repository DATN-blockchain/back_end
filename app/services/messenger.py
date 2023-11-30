import uuid
from datetime import datetime

from sqlalchemy.orm import Session
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler
from ..core.pusher.pusher_client import PusherClient
from ..core.settings import settings
from ..model.base import NotificationType

from ..schemas import MessengerCreate, MessengerResponse, MessengerCreateParam
from ..crud import crud_messenger, crud_user


class MessengerService:
    def __init__(self, db: Session):
        self.db = db

    async def get_messenger_by_id(self, messenger_id: str):
        current_messenger = crud_messenger.get_messenger_by_id(db=self.db,
                                                               messenger_id=messenger_id)
        if not current_messenger:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CART_NOT_FOUND)

        return current_messenger

    async def list_messenger(self, sender_id: str, receiver_id: str):
        current_receiver = crud_user.get_user_by_id(db=self.db, user_id=receiver_id)
        if not current_receiver:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_USER_NOT_FOUND)
        list_messenger, is_read = crud_messenger.list_messenger(db=self.db,
                                                                sender_id=sender_id,
                                                                receiver_id=receiver_id)
        list_messenger = [MessengerResponse.from_orm(item) for item in list_messenger]
        if is_read:
            is_read = 0
        else:
            is_read = 1
        result = dict(is_read=is_read, list_messenger=list_messenger)
        return result

    async def create_messenger(self, user_id: str, messenger_create: MessengerCreateParam):
        current_receiver = crud_user.get_user_by_id(db=self.db, user_id=messenger_create.receiver_id)
        if not current_receiver:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_USER_NOT_FOUND)
        messenger_create = MessengerCreate(
            id=str(uuid.uuid4()),
            sender_id=user_id,
            receiver_id=current_receiver.id,
            content=messenger_create.content)
        result = crud_messenger.create(db=self.db, obj_in=messenger_create)
        data = dict(sender_id=messenger_create.sender_id,
                    content=messenger_create.content,
                    receiver=current_receiver.username,
                    type=NotificationType.MESSENGER)
        self.push_data_for_pusher(user_id=current_receiver.id, data=data)

        return result

    @staticmethod
    def push_data_for_pusher(user_id, data):
        client = PusherClient()
        client.push_notification(channel=settings.GENERAL_CHANNEL, event=user_id, data_push=data)

    async def delete_messenger(self, messenger_id: str):
        current_messenger = crud_messenger.get_messenger_by_id(db=self.db, messenger_id=messenger_id)
        if not current_messenger:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CART_NOT_FOUND)

        result = crud_messenger.remove(db=self.db, entry_id=messenger_id)
        return result
