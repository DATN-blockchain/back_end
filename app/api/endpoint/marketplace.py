from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.depend import oauth2
from app.model.base import ProductStatus, ProductType
from app.utils.response import make_response_object

from app.schemas.marketplace import MarketplaceUpdate
from app.model import User
from app.services import MarketplaceService

router = APIRouter()


@router.post("/marketplace/create")
async def create_marketplace(product_id: str,
                             user: User = Depends(oauth2.get_current_user),
                             db: Session = Depends(get_db)):
    marketplace_service = MarketplaceService(db=db)

    product_response = await marketplace_service.create_marketplace(user_id=user.id, product_id=product_id)
    db.refresh(product_response)
    return make_response_object(product_response)


@router.get("/marketplace/list")
async def list_marketplace(
        product_id: str = None,
        order_type: ProductType = None,
        name_product: str = None,
        user: User = Depends(oauth2.get_current_user),
        db: Session = Depends(get_db),
        skip=0,
        limit=10):
    marketplace_service = MarketplaceService(db=db)

    marketplace_response = await marketplace_service.list_marketplace(product_id=product_id, order_type=order_type,
                                                                      name_product=name_product,
                                                                      skip=skip, limit=limit)
    return make_response_object(marketplace_response)


@router.get("/marketplace/{marketplace_id}")
async def get_marketplace_by_id(marketplace_id: str,
                                user: User = Depends(oauth2.get_current_user),
                                db: Session = Depends(get_db)):
    marketplace_service = MarketplaceService(db=db)

    marketplace_response = await marketplace_service.get_marketplace_by_id(marketplace_id=marketplace_id)
    return make_response_object(marketplace_response)


@router.put("/marketplace/update/{marketplace_id}")
async def update_marketplace(marketplace_id: str,
                             hashed_data: str = None,
                             user: User = Depends(oauth2.get_current_user),
                             db: Session = Depends(get_db)):
    marketplace_service = MarketplaceService(db=db)

    # authorization
    await marketplace_service.has_marketplace_permissions(user_id=user.id, marketplace_id=marketplace_id)
    marketplace_update = MarketplaceUpdate(hashed_data=hashed_data)

    marketplace_response = await marketplace_service.update_marketplace(marketplace_id=marketplace_id,
                                                                        marketplace_update=marketplace_update)

    return make_response_object(marketplace_response)

# @router.delete("/marketplace/{marketplace_id}/delete")
# async def delete_marketplace(marketplace_id: str,
#                              user: User = Depends(oauth2.get_current_user),
#                              db: Session = Depends(get_db)):
#     marketplace_service = MarketplaceService(db=db)
#
#     # authorization
#     await marketplace_service.has_marketplace_permissions(user_id=user.id, marketplace_id=marketplace_id)
#
#     marketplace_response = await marketplace_service.delete_marketplace(marketplace_id=marketplace_id)
#     return make_response_object(marketplace_response)
