from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.depend import oauth2
from app.schemas import MessengerCreateParam
from app.utils.response import make_response_object

from app.model import User
from app.services import MessengerService

router = APIRouter()


@router.get("/messenger/list_messenger")
async def list_messenger(
        user_id: str,
        user: User = Depends(oauth2.get_current_user),
        db: Session = Depends(get_db)):
    messenger_service = MessengerService(db=db)

    messenger_response = await messenger_service.list_messenger(sender_id=user.id, receiver_id=user_id)
    return make_response_object(messenger_response)


@router.post("/messenger/create")
async def create_messenger(messenger_create: MessengerCreateParam,
                           user: User = Depends(oauth2.get_current_user),
                           db: Session = Depends(get_db)):
    messenger_service = MessengerService(db=db)
    product_response = await messenger_service.create_messenger(user_id=user.id, messenger_create=messenger_create)
    return make_response_object(product_response)


@router.delete("/messenger/{messenger_id}/delete")
async def delete_product(messenger_id: str,
                         user: User = Depends(oauth2.get_current_user),
                         db: Session = Depends(get_db)):
    messenger_service = MessengerService(db=db)

    product_response = await messenger_service.delete_messenger(messenger_id=messenger_id)

    return make_response_object(product_response)
