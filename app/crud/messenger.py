from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_, and_
from .base import CRUDBase
from ..model import Messenger

from ..schemas import MessengerCreate, MessengerUpdate


class CRUDMessenger(CRUDBase[Messenger, MessengerCreate, MessengerUpdate]):

    @staticmethod
    def get_messenger_by_id(db: Session, messenger_id: str) -> Optional[Messenger]:
        current_messenger = db.query(Messenger).get(messenger_id)
        return current_messenger

    @staticmethod
    def list_messenger(db: Session, sender_id: str, receiver_id: str):
        db_query = db.query(Messenger).filter(or_(
                and_(Messenger.sender_id == sender_id, Messenger.receiver_id == receiver_id),
                and_(Messenger.sender_id == receiver_id, Messenger.receiver_id == sender_id),
            ))
        list_messenger = db_query.order_by(desc(Messenger.create_at))
        last_message = list_messenger.first()

        if last_message:
            return list_messenger.all(), last_message.is_read
        return list_messenger.all(), None


crud_messenger = CRUDMessenger(Messenger)
