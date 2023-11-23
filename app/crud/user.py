import logging

from typing import Optional
from sqlalchemy.orm import Session
from .base import CRUDBase
from ..model import User
from app.utils import hash_lib

from app.utils.hash_lib import hash_verify_code
from app.schemas.user import UserCreate, UserUpdate
from ..model.base import ConfirmStatusUser, UserSystemRole

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
    def list_users(db: Session, system_role: UserSystemRole = None, email: str = None, username: str = None,
                   skip: int = None, limit: int = None):
        db_query = db.query(User)
        if system_role is not None:
            db_query = db_query.filter(User.system_role == system_role)
        if email:
            db_query = db_query.filter(User.email.ilike(f'%{email}%'))
        if username:
            db_query = db_query.filter(User.email.ilike(f'%{username}%'))
        if skip and limit is None:
            list_users = db_query.all()
        else:
            list_users = db_query.offset(skip).limit(limit).all()

        total_users = db_query.count()
        result = dict(total_users=total_users, list_users=list_users)
        return result

    @staticmethod
    def list_users_request(db: Session, email: str = None, username: str = None, skip: int = None, limit: int = None):
        db_query = db.query(User).filter(User.confirm_status == ConfirmStatusUser.PENDING)
        if email is not None:
            db_query = db_query.filter(User.email.ilike(f'%{email}%'))
        if username is not None:
            db_query = db_query.filter(User.email.ilike(f'%{username}%'))
        if skip and limit is None:
            list_users = db_query.all()
        else:
            list_users = db_query.offset(skip).limit(limit).all()
        total_users = db_query.count()

        result = dict(total_users=total_users, list_users=list_users)
        return result

    @staticmethod
    def get_statistical_user(db: Session):
        db_query = db.query(User)
        member_count = db_query.filter(User.system_role == UserSystemRole.MEMBER).count()
        seedling_count = db_query.filter(User.system_role == UserSystemRole.SEEDLING_COMPANY).count()
        farmer_count = db_query.filter(User.system_role == UserSystemRole.FARMER).count()
        manufacturer_count = db_query.filter(User.system_role == UserSystemRole.MANUFACTURER).count()
        total_user = db_query.count()
        result = dict(total_user=total_user, member_count=member_count,
                      seedling_count=seedling_count, farmer_count=farmer_count,
                      manufacturer_count=manufacturer_count)
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
    def update_user_role(db: Session, current_user: User, user_role: str, tx_hash: str = None):
        logger.info("CRUD_user: update_user_role called")
        current_user.system_role = user_role
        if tx_hash:
            current_user.tx_hash = tx_hash
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

    @staticmethod
    def get_survey_by_user(db: Session, user_id: str):
        logger.info("CRUD_user: get_survey_by_user called.")
        db_query = db.query(User).filter(User.id == user_id).first()
        user_survey = db_query.survey_data
        logger.info("CRUD_user: get_survey_by_user called successfully.")
        return user_survey

    @staticmethod
    def update_account_balance(db: Session, current_user: dict, product_price: int):
        logger.info("CRUD_user: change_password called.")
        account_balance = current_user.account_balance - product_price
        current_user.account_balance = account_balance
        db.commit()
        db.refresh(current_user)
        logger.info("CRUD_user: change_password called successfully.")
        return current_user


crud_user = CRUDUser(User)
