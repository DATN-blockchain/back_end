import datetime
import uuid
import smtplib
import logging
import string
import secrets

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from fastapi import UploadFile
from eth_account import Account
from sqlalchemy.orm import Session

from app.constant.app_status import AppStatus
from app.utils import hash_lib
from app.core.exceptions import error_exception_handler
from app.core.settings import settings
from ..crud import crud_product, crud_transaction_sf, crud_transaction_fm, crud_financial_transaction
from ..blockchain_web3.actor_provider import ActorProvider
from ..model import User
from ..model.base import ConfirmStatusUser, ConfirmUser, UserSystemRole, BankCode, LanguageEnum, TypeTransaction, \
    FinancialStatus
from cloudinary.uploader import upload

from ..schemas import UserCreate, UserCreateParams, UserUpdateParams, LoginUser, UserResponse, ChangePassword, UserBase, \
    SurveyCreateParam, FinancialTransactionCreate
from ..blockchain_web3.hash_code import hash_code_private_key
from ..crud.user import crud_user
from app.constant.mapping_enum import USER_TYPE
from ..utils.hash_lib import base64_encode
from ..utils.payment import payment, payment_return

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

    async def list_users_request(self, email: str, username: str, skip: int, limit: int):
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

    async def get_statistical_me(self, user_id: str):
        statistical_product = crud_product.get_statistical_product_me(db=self.db, user_id=user_id)
        result = dict(statistical_product=statistical_product)
        return result

    async def get_survey_by_user(self, user_id: str):
        user_survey = crud_user.get_survey_by_user(db=self.db, user_id=user_id)
        return user_survey

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
                full_name=username_lower,
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
            subject = "[SupplyChainDurian] Please reset password"
            title = "Verification code to change your password"
        elif action == "is_active":
            subject = "Welcome to Supply Chain Durian"
            title_tmp = "Welcome to Supply Chain Durian"
            address_img = "https://icon-library.com/images/celebration-icon-png/celebration-icon-png-7.jpg"
            title = f'<img src="{address_img}" alt="celebration icon" style="width:30px;height:30px;"> {title_tmp}'
        else:
            title = None
            subject = None

        html = """
        <html>
            <body>
                <h1>{}</h1>
                <p>Thank you for joining Supply Chain Durian! We are grateful to have you as a part of our community.</p>
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

        if not current_user.is_active:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_YOUR_ACCOUNT_LOCKED)

        if not hash_lib.verify_password(login_request.password, current_user.hashed_password):
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PASSWORD_INVALID)

        return UserResponse.from_orm(current_user)

    async def update_profile(self, user_id: str, update_user: UserUpdateParams):
        current_user = crud_user.get_user_by_id(db=self.db, user_id=user_id)
        if not current_user:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_USER_NOT_FOUND)
        result = crud_user.update(db=self.db, db_obj=current_user, obj_in=update_user)
        data_hash = dict(name=result.full_name, phone=result.phone)
        hash_info = base64_encode(data_hash)
        actor_provider = ActorProvider()
        actor_provider.update_actor(result.id, hash_info=hash_info)
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
            actor_provider = ActorProvider()
            role = USER_TYPE[system_role]
            data_hash = dict(name=current_user.full_name, phone=current_user.phone)
            hash_info = base64_encode(data_hash)
            tx_hash = actor_provider.create_actor(user_id=user_id,
                                                  address=current_user.address_wallet,
                                                  role=role, hash_info=hash_info)
        else:
            system_role = current_user.system_role
            tx_hash = None
        user_update = dict(system_role=system_role, confirm_status=ConfirmStatusUser.DONE,
                           tx_hash=f'{settings.BLOCK_EXPLORER}{tx_hash}')
        result = crud_user.update(db=self.db, db_obj=current_user, obj_in=user_update)
        return UserResponse.from_orm(result)

    async def update_user_status(self, user_id: str, is_active: bool):
        current_user = crud_user.get_user_by_id(db=self.db, user_id=user_id)
        if not current_user:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_USER_NOT_FOUND)
        obj_in = dict(is_active=is_active)
        result = crud_user.update(self.db, db_obj=current_user, obj_in=obj_in)
        return result

    async def update_user_role(self, user_id: str, user_role: str):
        current_user = crud_user.get_user_by_id(db=self.db, user_id=user_id)
        tx_hash = None
        if not current_user:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_USER_NOT_FOUND)
        if user_role in ["FARMER", 'SEEDLING_COMPANY', 'MANUFACTURER']:
            actor_provider = ActorProvider()
            map_role = {"SEEDLING_COMPANY": 0, "FARMER": 1, "MANUFACTURER": 2}
            data_hash = dict(name=current_user.full_name, phone=current_user.phone)
            hash_info = base64_encode(data_hash)
            tx_hash = actor_provider.create_actor(user_id=user_id, address=current_user.address_wallet,
                                                  role=map_role[user_role], hash_info=hash_info)

        result = crud_user.update_user_role(self.db, current_user=current_user, user_role=user_role,
                                            tx_hash=f'{settings.BLOCK_EXPLORER}{tx_hash}')
        return UserResponse.from_orm(result)

    async def change_password(self, current_user: User, obj_in: ChangePassword):
        logger.info("UserService: change_password called.")

        if not hash_lib.verify_password(obj_in.old_password, current_user.hashed_password):
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PASSWORD_INCORRECT)

        if obj_in.new_password != obj_in.new_password_confirm:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PASSWORD_CONFIRM_WRONG)

        hashed_password = hash_lib.hash_password(obj_in.new_password)

        result = crud_user.change_password_user(db=self.db, id_user=current_user.id, new_password=hashed_password)
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

        # Generate a new account
        account = Account.create()
        private_key = account.key.hex()
        address = account.address

        private_key = hash_code_private_key(str(private_key))
        data_update = dict(hashed_password=hash_lib.hash_password(new_password), is_active=True, address_wallet=address,
                           private_key=private_key)
        result = crud_user.update(db=self.db, db_obj=current_user, obj_in=data_update)
        return UserResponse.from_orm(result)

    async def change_password_user(self, current_user: any, obj_in: ChangePassword):
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

    async def payment_return_in_user(self, request):
        result = payment_return(request=request)
        amount = result["amount"]
        current_user = crud_user.get(db=self.db, entry_id=result.get("order_desc"))
        tx_hash = ActorProvider().deposited(user_id=current_user.id,
                                            amount=int(int(amount) / 1000))
        crud_user.update(db=self.db, db_obj=current_user,
                         obj_in=dict(
                             account_balance=current_user.account_balance + int(
                                 int(amount) / 1000)))
        financial_transaction_create = FinancialTransactionCreate(
            id=str(uuid.uuid4()),
            user_id=result["order_desc"],
            status=FinancialStatus.DONE,
            type_transaction=TypeTransaction.DEPOSIT,
            amount=result["amount"],
            tx_hash=f'{settings.BLOCK_EXPLORER}{tx_hash}')
        result_transaction = crud_financial_transaction.create(db=self.db, obj_in=financial_transaction_create)
        current_admin = crud_user.get_admin(db=self.db)
        current_user = crud_user.get_user_by_id(db=self.db, user_id=result["order_desc"])
        return result_transaction, current_user, current_admin, amount

    async def payment(self, request, amount: int, user_id: str, bank_code: BankCode,
                      language: LanguageEnum = LanguageEnum.VIETNAMESE,
                      order_type: str = "billpayment"):
        current_user = crud_user.get(db=self.db, entry_id=user_id)
        if not current_user:
            raise error_exception_handler(error=Exception, app_status=AppStatus.ERROR_USER_NOT_FOUND)
        order_id = int(datetime.datetime.now().timestamp())

        return payment(request=request, order_id=order_id, order_type=order_type, amount=amount,
                       language=language.value,
                       order_desc=user_id, bank_code=bank_code.value)
