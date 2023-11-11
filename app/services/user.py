import uuid
import smtplib
import logging
import string
import secrets
import random

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.constant.app_status import AppStatus
from app.utils import hash_lib
from app.core.exceptions import error_exception_handler
from app.core.settings import settings
from ..crud import crud_product, crud_transaction_sf, crud_transaction_fm
from ..model import User
from ..model.base import ConfirmStatusUser, ConfirmUser, UserSystemRole
import cloudinary
from cloudinary.uploader import upload

from ..schemas import UserCreate, UserCreateParams, UserUpdateParams, LoginUser, UserResponse, ChangePassword, UserBase, \
    SurveyCreateParam
from ..crud.user import crud_user

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, db: Session):
        self.db = db

    async def get_user_by_id(self, user_id: str):
        current_user = crud_user.get_user_by_id(db=self.db, user_id=user_id)
        if not current_user:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_USER_NOT_FOUND)
        return UserResponse.from_orm(current_user)

    async def list_users(self, system_role: UserSystemRole, email: str, username: str, skip: int, limit: int):
        result = crud_user.list_users(db=self.db, system_role=system_role, email=email, username=username, skip=skip,
                                      limit=limit)
        return result

    async def list_users_request(self, email: str, username: str,  skip: int, limit: int):
        result = crud_user.list_users_request(db=self.db, email=email, username=username, skip=skip, limit=limit)
        return result

    async def get_statistical(self):
        statistical_user = crud_user.get_statistical_user(db=self.db)
        statistical_product = crud_product.get_statistical_product(db=self.db)
        statistical_transaction_sf = crud_transaction_sf.get_statistical_transaction_sf(db=self.db)
        statistical_transaction_fm = crud_transaction_fm.get_statistical_transaction_fm(db=self.db)
        result = dict(statistical_user=statistical_user, statistical_product=statistical_product,
                      statistical_transaction_sf=statistical_transaction_sf,
                      statistical_transaction_fm=statistical_transaction_fm)
        return result

    async def create_user(self, create_user: UserCreateParams):

        email_lower = create_user.email.lower()
        username_lower = create_user.username.lower()
        current_email = crud_user.get_by_email(db=self.db, email=email_lower)
        if current_email:
            if current_email.hashed_password is None:
                update_user = UserBase(email=email_lower, username=username_lower)
                result = crud_user.update(db=self.db, db_obj=current_email, obj_in=update_user)
            else:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_EMAIL_ALREADY_EXIST)

        else:
            result = crud_user.create_user(db=self.db, create_user=UserCreate(
                id=str(uuid.uuid4()),
                username=username_lower,
                email=email_lower))
        await self.get_verification_code(email=email_lower, action="is_active")
        return UserResponse.from_orm(result)

    async def update_survey(self, user_id: str, survey_param: SurveyCreateParam):
        current_user = crud_user.get_user_by_id(db=self.db, user_id=user_id)
        user_update = dict(survey_data=survey_param.survey_data, confirm_status=ConfirmStatusUser.PENDING)
        result = crud_user.update(db=self.db, db_obj=current_user, obj_in=user_update)

        return result.survey_data

    async def get_verification_code(self, email: str, action: str):
        email_lower = email.lower()
        current_email = crud_user.get_by_email(db=self.db, email=email_lower)

        if not current_email:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_EMAIL_NOT_FOUND)

        email_from = settings.COURSE_EMAIl
        email_password = settings.COURSE_EMAIL_PASSWORD
        characters = string.ascii_letters + string.digits
        verify_code = ''.join(secrets.choice(characters) for _ in range(8))
        receiver_email = email

        if action == "forget_password":
            subject = "[FULL STACK] Verification code to change your password"
        elif action == "is_active":
            subject = "[FULL STACK] Verification code to user authentication"

        title = subject.replace("[FULL STACK]", "")
        html = """
        <html>
            <body>
                <h1>{}</h1>
                <p>Your verification code is <strong>{}</strong>. Please do not share it with anyone.</p>
            </body>
        </html>
        """.format(title, verify_code)

        try:
            msg = MIMEMultipart()
            msg['From'] = email_from
            msg['To'] = receiver_email
            msg['Subject'] = subject

            msg.attach(MIMEText(html, 'html'))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_from, email_password)
            server.send_message(msg)
            server.quit()

            crud_user.update_verification_code(self.db, current_user=current_email, verify_code=verify_code)
        except Exception:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_EMAIL_NOT_FOUND)

        return dict(message_code=AppStatus.SUCCESS.message)

    async def login(self, login_request: LoginUser):
        email_lower = login_request.email.lower()
        current_user = crud_user.get_by_email(db=self.db, email=email_lower)

        if not current_user:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_USER_NOT_FOUND)

        if current_user.is_active == False:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_INACTIVE_USER)

        if not hash_lib.verify_password(login_request.password, current_user.hashed_password):
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PASSWORD_INVALID)

        return UserResponse.from_orm(current_user)

    async def update_profile(self, user_id: str, update_user: UserUpdateParams):
        current_user = crud_user.get_user_by_id(db=self.db, user_id=user_id)
        if not current_user:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_USER_NOT_FOUND)
        result = crud_user.update(db=self.db, db_obj=current_user, obj_in=update_user)
        return UserResponse.from_orm(result)

    async def update_avatar(self, user_id: str, avatar: UploadFile):
        current_user = crud_user.get_user_by_id(db=self.db, user_id=user_id)
        uploaded_banner = upload(avatar.file)
        avatar_url = uploaded_banner['secure_url']
        user_update = dict(avatar=avatar_url)
        crud_user.update(db=self.db, db_obj=current_user, obj_in=user_update)
        return avatar_url

    async def update_qr_code(self, user_id: str, qr_code: UploadFile):
        current_user = crud_user.get_user_by_id(db=self.db, user_id=user_id)
        uploaded_qr_code = upload(qr_code.file)
        qr_code_url = uploaded_qr_code['secure_url']
        user_update = dict(qr_code=qr_code_url)
        crud_user.update(db=self.db, db_obj=current_user, obj_in=user_update)
        return qr_code_url

    async def confirm_user(self, user_id: str, confirm: ConfirmUser):
        current_user = crud_user.get_user_by_id(db=self.db, user_id=user_id)
        if not current_user:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_USER_NOT_FOUND)
        if confirm == ConfirmUser.ACCEPT:
            system_role = current_user.survey_data["user_role"]
        else:
            system_role = current_user.system_role
        user_update = dict(system_role=system_role, confirm_status=ConfirmStatusUser.DONE)
        result = crud_user.update(db=self.db, db_obj=current_user, obj_in=user_update)
        return UserResponse.from_orm(result)

    async def update_user_role(self, user_id: str, user_role: str):
        current_user = crud_user.get_user_by_id(db=self.db, user_id=user_id)
        if not current_user:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_USER_NOT_FOUND)

        result = crud_user.update_user_role(self.db, current_user=current_user, user_role=user_role)
        return UserResponse.from_orm(result)

    async def change_password(self, current_user: User, obj_in: ChangePassword):
        logger.info("UserService: change_password called.")

        if not hash_lib.verify_password(obj_in.old_password, current_user.hashed_password):
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PASSWORD_INCORRECT)

        if obj_in.new_password != obj_in.new_password_confirm:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PASSWORD_CONFIRM_WRONG)

        hashed_password = hash_lib.hash_password(obj_in.new_password)

        result = crud_user.change_password(db=self.db, id_user=current_user.id, new_password=hashed_password)
        logger.info("UserService: change_password called successfully.")

    async def verify_code(self, email: str,
                          verify_code: str,
                          new_password: str,
                          password_confirm: str):
        email_lower = email.lower()
        current_user = crud_user.get_by_email(db=self.db, email=email_lower)

        if not current_user:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_EMAIL_NOT_FOUND)

        if not hash_lib.verify_code(verify_code, current_user.verify_code):
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_INVALID_VERIFY_CODE)

        if len(new_password) < 6:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_INVALID_PASSWORD_LENGTH)
        elif new_password != password_confirm:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CONFIRM_PASSWORD_DOES_NOT_MATCH)

        result = crud_user.verify_code(self.db, current_user=current_user, new_password=new_password)
        return UserResponse.from_orm(result)

    async def change_password(self, current_user: dict, obj_in: ChangePassword):
        logger.info("Service_user: change_password called")

        if not hash_lib.verify_password(obj_in.old_password, current_user.hashed_password):
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PASSWORD_INCORRECT)

        if len(obj_in.new_password) < 6:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_INVALID_PASSWORD_LENGTH)

        if obj_in.new_password != obj_in.new_password_confirm:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PASSWORD_CONFIRM_WRONG)

        hashed_password = hash_lib.hash_password(obj_in.new_password)

        result = crud_user.change_password(db=self.db, current_user=current_user, new_password=hashed_password)
        logger.info("Service_user: change_password called successfully")
        return UserResponse.from_orm(result)
