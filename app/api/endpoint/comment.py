from fastapi import APIRouter
from fastapi import Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.depend import oauth2
from app.utils.response import make_response_object
from ...constant.template import CommentTemplate
from ...model.base import NotificationType

from ...schemas import CommentCreateParams, CommentUpdateParams

from ...model import User
from ...services import CommentService, NotificationService
from ...utils.background_tasks import send_notification

router = APIRouter()


@router.get("/comments/list")
async def list_comment(marketplace_id: str,
                       user: User = Depends(oauth2.get_current_user),
                       db: Session = Depends(get_db),
                       skip=0,
                       limit=10):
    comment_service = CommentService(db=db)
    comment_response = await comment_service.list_comment(marketplace_id=marketplace_id, skip=skip, limit=limit)
    return make_response_object(comment_response)


@router.post("/comments/")
async def create_comment(comment: CommentCreateParams,
                         background_tasks: BackgroundTasks,
                         db: Session = Depends(get_db),
                         user: User = Depends(oauth2.get_current_user)):
    comment_service = CommentService(db=db)
    notification_service = NotificationService(db=db)

    marketplace, comment_response = await comment_service.create_comment_to_post(user_id=user.id, comment=comment)

    message_template = CommentTemplate.Comment_MSG
    background_tasks.add_task(
        send_notification, notification_service, entity=marketplace,
        notification_type=NotificationType.COMMENT_NOTIFICATION,
        message_template=message_template, action='commented',
        current_user=user, owner=marketplace.product.user
    )
    return make_response_object(comment_response)


@router.put("/comments/")
async def update_comment(comment_id: str,
                         comment: CommentUpdateParams,
                         db: Session = Depends(get_db),
                         user: User = Depends(oauth2.get_current_user)):
    comment_service = CommentService(db=db)
    await comment_service.has_comment_permission(user_id=user.id, comment_id=comment_id)
    comment_response = await comment_service.update_comment(comment_id=comment_id, comment=comment)
    return make_response_object(comment_response)


@router.delete("/comments/")
async def delete_comment(comment_id: str,
                         db: Session = Depends(get_db),
                         user: User = Depends(oauth2.get_current_user)):
    comment_service = CommentService(db=db)
    await comment_service.has_comment_permission(user_id=user.id, comment_id=comment_id)
    comment_response = await comment_service.delete_comment(comment_id=comment_id)
    return make_response_object(comment_response)
