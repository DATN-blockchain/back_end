import uuid
from fastapi import UploadFile, File

from sqlalchemy.orm import Session
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler
import cloudinary
from cloudinary.uploader import upload

from ..schemas import ProductType, ProductCreate, ProductUpdate, ProductResponse
from ..crud import crud_product, crud_user
from ..model.base import ProductRole, ProductStatus, UserSystemRole


class ProductService:
    def __init__(self, db: Session):
        self.db = db

    async def get_product_by_id(self, product_id: str):
        current_product = crud_product.get_product_by_id(db=self.db, product_id=product_id)
        if not current_product:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)

        return current_product

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

    async def create_product(self, user_id: str,
                             product_create: ProductCreate, banner: UploadFile = File(...)):

        current_user = crud_user.get_user_by_id(db=self.db, user_id=user_id)
        if current_user.system_role == UserSystemRole.MEMBER:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_METHOD_NOT_ALLOWED)

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
            created_by=user_id)

        result = crud_product.create(db=self.db, obj_in=product_create)
        return result

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

    async def delete_product(self, product_id: str):
        current_product = crud_product.get_product_by_id(db=self.db, product_id=product_id)
        if not current_product:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)

        result = crud_product.remove(db=self.db, entry_id=product_id)
        return result
