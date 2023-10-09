import logging

from typing import Optional
from sqlalchemy.orm import Session
from .base import CRUDBase
from ..model import User
from app.utils import hash_lib

from app.utils.hash_lib import hash_verify_code
from app.schemas.user import UserCreate, UserUpdate
from ..model.base import ConfirmStatusUser

logger = logging.getLogger(__name__)


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        current_email = db.query(User).filter(User.email == email).first()
        return current_email

    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
        current_user = db.query(User).filter(User.id == user_id).first()
        return current_user

    @staticmethod
    def list_users(db: Session, skip: int = None, limit: int = None):
        total_users = db.query(User).count()
        if skip and limit is None:
            list_users = db.query(User).all()
        else:
            list_users = db.query(User).offset(skip).limit(limit).all()
        result = dict(total_users=total_users, list_users=list_users)
        return result

    @staticmethod
    def list_users_request(db: Session, skip: int = None, limit: int = None):
        db_query = db.query(User).filter(User.confirm_status == ConfirmStatusUser.PENDING)
        if skip and limit is None:
            list_users = db_query.all()
        else:
            list_users = db_query.offset(skip).limit(limit).all()
        total_users = db_query.count()

        result = dict(total_users=total_users, list_users=list_users)
        return result

    @staticmethod
    def create_user(db: Session, create_user: UserCreate):
        current_user = User(**create_user.dict())
        db.add(current_user)
        db.commit()
        db.refresh(current_user)
        return current_user

    @staticmethod
    def update_verification_code(db: Session, current_user: dict, verify_code: str):
        current_user.verify_code = hash_verify_code(str(verify_code))
        db.commit()
        db.refresh(current_user)
        return current_user

    @staticmethod
    def update_user(db: Session, current_user: str, update_user: UserUpdate):
        result = super().update(db, obj_in=update_user, db_obj=current_user)
        return result

    @staticmethod
    def update_user_role(db: Session, current_user: str, user_role: str):
        logger.info("CRUD_user: update_user_role called")
        current_user.system_role = user_role
        db.commit()
        db.refresh(current_user)
        logger.info("CRUD_user: update_user_role called successfully")
        return current_user

    @staticmethod
    def verify_code(db: Session, current_user: dict, new_password: str):
        current_user.hashed_password = hash_lib.hash_verify_code(str(new_password))
        current_user.is_active = True
        db.commit()
        db.refresh(current_user)
        return current_user

    @staticmethod
    def change_password(db: Session, current_user: dict, new_password: str):
        logger.info("CRUD_user: change_password called.")
        current_user.hashed_password = new_password
        db.commit()
        db.refresh(current_user)
        logger.info("CRUD_user: change_password called successfully.")
        return current_user


crud_user = CRUDUser(User)
