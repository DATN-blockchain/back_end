import uuid
import cloudinary

from cloudinary.uploader import upload
from fastapi import UploadFile, File
from sqlalchemy.orm import Session
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler

from ..schemas import DetailDescriptionCreate, DetailDescriptionUpdate, DetailDescriptionCreateParams
from ..crud import crud_detail_description, crud_product


class DetailDescriptionService:
    def __init__(self, db: Session):
        self.db = db

    async def create_detail_description(self, detail_description_create: DetailDescriptionCreateParams,
                                        img: UploadFile = File(...)):
        current_product = crud_product.get_product_by_id(db=self.db, product_id=detail_description_create.product_id)
        if not current_product:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)
        image = cloudinary.uploader.upload(img.file, folder="image")
        image_url = image.get("secure_url")
        detail_description_create = DetailDescriptionCreate(
            id=str(uuid.uuid4()),
            product_id=detail_description_create.product_id,
            title=detail_description_create.title,
            description=detail_description_create.description,
            image=image_url)
        # breakpoint()

        result = crud_detail_description.create(db=self.db, obj_in=detail_description_create)
        return result

    async def update_detail_description(self, detail_description_id: str,
                                        detail_description_update: DetailDescriptionUpdate):
        current_detail_description = (crud_detail_description.
                                      get_detail_description_id(db=self.db,
                                                                detail_description_id=detail_description_id))
        if not current_detail_description:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_DETAIL_DESCRIPTION_NOT_FOUND)
        result = crud_detail_description.update(db=self.db,
                                                db_obj=current_detail_description,
                                                obj_in=detail_description_update)
        return result

    async def update_image(self, detail_description_id: str, image: UploadFile):
        current_detail_description = (crud_detail_description.
                                      get_detail_description_id(db=self.db,
                                                                detail_description_id=detail_description_id))
        if not current_detail_description:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_DETAIL_DESCRIPTION_NOT_FOUND)
        uploaded_banner = upload(image.file)
        image_url = uploaded_banner['secure_url']
        detail_description_update = dict(image=image_url)
        crud_detail_description.update(db=self.db, db_obj=current_detail_description, obj_in=detail_description_update)
        return AppStatus.SUCCESS

    async def delete_detail_description(self, detail_description_id: str):
        current_detail_description = (crud_detail_description.
                                      get_detail_description_id(db=self.db,
                                                                detail_description_id=detail_description_id))
        if not current_detail_description:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_DETAIL_DESCRIPTION_NOT_FOUND)

        result = crud_detail_description.remove(db=self.db, entry_id=detail_description_id)
        return result
