from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_, and_, distinct

from . import crud_user
from .base import CRUDBase
from ..model import Messenger, User

from ..schemas import MessengerCreate, MessengerUpdate


class CRUDMessenger(CRUDBase[Messenger, MessengerCreate, MessengerUpdate]):

    @staticmethod
    def get_messenger_by_id(db: Session, messenger_id: str) -> Optional[Messenger]:
        current_messenger = db.query(Messenger).get(messenger_id)
        return current_messenger

    @staticmethod
    def list_messenger_detail(db: Session, sender_id: str, receiver_id: str):
        db_query = db.query(Messenger).filter(or_(
            and_(Messenger.sender_id == sender_id, Messenger.receiver_id == receiver_id),
            and_(Messenger.sender_id == receiver_id, Messenger.receiver_id == sender_id),
        ))
        # list_messenger = db_query.order_by(desc(Messenger.create_at))
        return db_query.all()

    @staticmethod
    def last_message(db: Session, sender_id: str, receiver_id: str):
        db_query = db.query(Messenger).filter(or_(
            and_(Messenger.sender_id == sender_id, Messenger.receiver_id == receiver_id),
            and_(Messenger.sender_id == receiver_id, Messenger.receiver_id == sender_id),
        ))
        list_messenger = db_query.order_by(desc(Messenger.create_at))
        last_message = list_messenger.first()
        return last_message

    @staticmethod
    def list_messenger_contacts(db: Session, user_id: str):
        sender_contacts = db.query(Messenger.receiver_id).filter(Messenger.sender_id == user_id).all()
        receiver_contacts = db.query(Messenger.sender_id).filter(Messenger.receiver_id == user_id).all()

        all_contact_ids = list(
            set(contact[0] for contact in sender_contacts) | set(contact[0] for contact in receiver_contacts))
        return all_contact_ids


crud_messenger = CRUDMessenger(Messenger)
