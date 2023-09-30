import uuid
from fastapi import UploadFile, File

from sqlalchemy.orm import Session
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler
import cloudinary
from cloudinary.uploader import upload

from ..crud.product_farmer import crud_product_farmer
from ..model import User
from ..schemas import ProductType, ProductCreate, ProductUpdate, ProductResponse, TransactionSFCreate, \
    ProductFarmerCreate, TransactionFMCreate, ProductFarmerHistoryResponse
from ..crud import crud_product, crud_user, crud_transaction_sf, crud_transaction_fm, crud_product_farmer
from ..model.base import ProductRole, ProductStatus, UserSystemRole


class ProductService:
    def __init__(self, db: Session):
        self.db = db

    async def get_product_by_id(self, product_id: str):
        current_product = crud_product.get_product_by_id(db=self.db, product_id=product_id)
        if not current_product:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)

        return current_product

    async def get_product_seedling_company_history(self, product_id: str):
        current_product = crud_product.get_product_by_id(db=self.db, product_id=product_id)
        if not (current_product and current_product.product_type == ProductType.SEEDLING_COMPANY):
            raise error_exception_handler(error=Exception(),
                                          app_status=AppStatus.ERROR_SEEDLING_COMPANY_PRODUCT_NOT_FOUND)
        result = ProductResponse.from_orm(current_product)

        return result

    async def get_product_farmer_history(self, product_id: str):
        current_product_farmer = crud_product_farmer.get_product_farmer_by_product_id(db=self.db, product_id=product_id)
        if not current_product_farmer:
            raise error_exception_handler(error=Exception(),
                                          app_status=AppStatus.ERROR_FARMER_PRODUCT_NOT_FOUND)
        result = ProductFarmerHistoryResponse.from_orm(current_product_farmer)

        return result

    async def get_product_history(self, product_id: str):
        current_product = crud_product.get_product_by_id(db=self.db, product_id=product_id)
        if current_product is None:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)
        if current_product.product_type == ProductType.SEEDLING_COMPANY:
            result = ProductResponse.from_orm(current_product)
        elif current_product.product_type == ProductType.FARMER:
            current_product_farmer = crud_product_farmer.get_product_farmer_by_product_id(db=self.db,
                                                                                          product_id=product_id)
            if not current_product_farmer:
                raise error_exception_handler(error=Exception(),
                                              app_status=AppStatus.ERROR_FARMER_PRODUCT_NOT_FOUND)
            result = ProductFarmerHistoryResponse.from_orm(current_product_farmer)
        else:
            result = None
        return result

    async def get_product_by_me(self, user_id: str, skip: int, limit: int):
        current_product = crud_product.get_product_by_me(db=self.db, user_id=user_id, skip=skip, limit=limit)
        if not current_product:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)

        return current_product

    async def list_product(self, skip: int, limit: int):
        total_product, list_product = crud_product.list_product(db=self.db, skip=skip, limit=limit)
        list_product = [ProductResponse.from_orm(item) for item in list_product]
        result = dict(total_product=total_product, list_product=list_product)
        return result

    async def create_product(self, current_user: User, product_create: ProductCreate, banner: UploadFile = File(...)):
        banner = cloudinary.uploader.upload(banner.file, folder="banner")
        banner_url = banner.get("secure_url")
        product_create = ProductCreate(
            id=str(uuid.uuid4()),
            name=product_create.name,
            description=product_create.description,
            banner=banner_url,
            product_type=current_user.system_role,
            price=product_create.price,
            quantity=product_create.quantity,
            product_status=ProductStatus.PRIVATE,
            created_by=current_user.id)
        result = crud_product.create(db=self.db, obj_in=product_create)
        return result

    async def create_product_entity(self, user_id: str, transaction_id: str,
                                    product_create: ProductCreate, banner: UploadFile = File(...)):

        current_user = crud_user.get_user_by_id(db=self.db, user_id=user_id)
        if current_user.system_role == UserSystemRole.MEMBER:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_METHOD_NOT_ALLOWED)

        if current_user.system_role == UserSystemRole.SEEDLING_COMPANY:
            product_create = await self.create_product(current_user=current_user, product_create=product_create,
                                                       banner=banner)

        if current_user.system_role == UserSystemRole.FARMER:
            if transaction_id is None:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PLEASE_ADD_TRANSACTION_ID)

            current_transaction = crud_transaction_sf.get_transaction_sf_by_id(db=self.db,
                                                                               transaction_sf_id=transaction_id)

            if current_transaction is None:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_TRANSACTION_NOT_FOUND)

            if current_transaction.user_id != user_id:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_METHOD_NOT_ALLOWED)

            project_me = crud_product.get_transaction_in_product(db=self.db, user_id=user_id,
                                                                 transaction_id=transaction_id)
            if project_me:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_TRANSACTION_CONFLICT)

            product_create = await self.create_product(current_user=current_user,
                                                       product_create=product_create, banner=banner)
            product_farmer = ProductFarmerCreate(id=str(uuid.uuid4()),
                                                 product_id=product_create.id,
                                                 transaction_sf_id=transaction_id)
            crud_product_farmer.create(db=self.db, obj_in=product_farmer)
        self.db.refresh(product_create)
        return product_create

    async def has_product_permissions(self, user_id: str, product_id: str):
        current_product = crud_product.get_product_by_id(db=self.db, product_id=product_id)
        if not current_product:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)
        if current_product.created_by != user_id:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_METHOD_NOT_ALLOWED)
        return current_product

    async def update_product(self, product_id: str, product_update: ProductUpdate,
                             banner: UploadFile):
        current_product = crud_product.get_product_by_id(db=self.db, product_id=product_id)
        if banner:
            uploaded_banner = upload(banner.file)
            banner_url = uploaded_banner['secure_url']
            product_update.banner = banner_url

        result = crud_product.update(db=self.db, db_obj=current_product, obj_in=product_update)
        return result

    async def update_product_status(self, product_id: str, product_status: ProductStatus):
        current_product = crud_product.get_product_by_id(db=self.db, product_id=product_id)

        result = crud_product.update_product_status(db=self.db, current_product=current_product,
                                                    product_status=product_status)
        return result

    @staticmethod
    def update_quantity_product(product_quantity: int, purchase_quantity: int):
        result = product_quantity - purchase_quantity
        return result

    @staticmethod
    def check_positive_value(value, error_message):
        if value <= 0:
            raise error_exception_handler(error=Exception(), app_status=error_message)

    async def purchase_product(self, user_id: str, product_id: str, price: int, quantity: int):
        current_product = crud_product.get_product_by_id(db=self.db, product_id=product_id)
        current_user = crud_user.get_user_by_id(db=self.db, user_id=user_id)

        if current_product is None:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)
        if current_product.created_by == user_id:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_METHOD_NOT_ALLOWED)
        if current_product.quantity < quantity:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_INVALID_QUANTITY)

        # Purchase for Farmer
        if current_user.system_role == UserSystemRole.FARMER:
            if current_product.product_type != ProductType.SEEDLING_COMPANY:
                raise error_exception_handler(error=Exception(),
                                              app_status=AppStatus.ERROR_PURCHASE_PRODUCT_TYPE_INVALID)
            self.check_positive_value(price, AppStatus.ERROR_INVALID_PRICE)
            self.check_positive_value(quantity, AppStatus.ERROR_INVALID_QUANTITY)

            create_transaction_sf = TransactionSFCreate(
                id=str(uuid.uuid4()),
                user_id=user_id,
                product_id=product_id,
                price=price,
                quantity=quantity
            )
            result = crud_transaction_sf.create(db=self.db, obj_in=create_transaction_sf)

        # Purchase for Manufacturer
        elif current_user.system_role == UserSystemRole.MANUFACTURER:
            if current_product.product_type != ProductType.FARMER:
                raise error_exception_handler(error=Exception(),
                                              app_status=AppStatus.ERROR_PURCHASE_PRODUCT_TYPE_INVALID)
            self.check_positive_value(price, AppStatus.ERROR_INVALID_PRICE)
            self.check_positive_value(quantity, AppStatus.ERROR_INVALID_QUANTITY)
            create_transaction_fm = TransactionFMCreate(
                id=str(uuid.uuid4()),
                user_id=user_id,
                product_id=product_id,
                price=price,
                quantity=quantity
            )
            result = crud_transaction_fm.create(db=self.db, obj_in=create_transaction_fm)
        else:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_YOU_ARE_NOT_ALLOWED)

        update_quantity = self.update_quantity_product(product_quantity=current_product.quantity,
                                                       purchase_quantity=quantity)
        obj_in = dict(quantity=update_quantity)
        crud_product.update(db=self.db, db_obj=current_product, obj_in=obj_in)

        self.db.refresh(result)
        return result

    async def delete_product(self, product_id: str):
        current_product = crud_product.get_product_by_id(db=self.db, product_id=product_id)
        if not current_product:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)

        result = crud_product.remove(db=self.db, entry_id=product_id)
        return result
