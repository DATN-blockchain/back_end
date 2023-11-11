from fastapi import APIRouter, UploadFile, File
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.depend import oauth2
from app.schemas import DetailDescriptionCreateParams
from app.utils.response import make_response_object

from app.schemas.detail_description import DetailDescriptionUpdate
from app.model import User
from app.services import DetailDescriptionService

router = APIRouter()


@router.post("/detail_description/create")
async def create_detail_description(title: str,
                                    description: str,
                                    product_id: str,
                                    img: UploadFile = File(...),
                                    user: User = Depends(oauth2.get_current_user),
                                    db: Session = Depends(get_db)):
    detail_description_service = DetailDescriptionService(db=db)

    detail_description_create = DetailDescriptionCreateParams(title=title,
                                                              description=description,
                                                              product_id=product_id)
    product_response = await (detail_description_service.
                              create_detail_description(detail_description_create=detail_description_create, img=img))
    return make_response_object(product_response)


@router.put("/detail_description/{detail_description_id}/update")
async def update_detail_description(detail_description_id: str,
                                    detail_description_update: DetailDescriptionUpdate,
                                    user: User = Depends(oauth2.get_current_user),
                                    db: Session = Depends(get_db)):
    detail_description_service = DetailDescriptionService(db=db)
    product_response = await (detail_description_service.
                              update_detail_description(detail_description_id=detail_description_id,
                                                        detail_description_update=detail_description_update))
    return make_response_object(product_response)


@router.put("/detail_description/{detail_description_id}/img")
async def update_avatar(detail_description_id: str,
                        image: UploadFile = File(None),
                        user: User = Depends(oauth2.get_current_user),
                        db: Session = Depends(get_db)):
    detail_description_service = DetailDescriptionService(db=db)
    product_response = await detail_description_service.update_image(detail_description_id=detail_description_id,
                                                                     image=image)
    return make_response_object(product_response)


@router.delete("/detail_description/{detail_description_id}/delete")
async def delete_product(detail_description_id: str,
                         user: User = Depends(oauth2.get_current_user),
                         db: Session = Depends(get_db)):
    detail_description_service = DetailDescriptionService(db=db)

    product_response = await (detail_description_service.
                              delete_detail_description(detail_description_id=detail_description_id))

    return make_response_object(product_response)
