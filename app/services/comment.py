import uuid

from sqlalchemy.orm import Session
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler

from ..schemas import CommentCreate, CommentCreateParams, CommentUpdateParams, CommentResponse
from ..crud import crud_comment, crud_marketplace


class CommentService:

    def __init__(self, db: Session):
        self.db = db

    async def get_comment_by_id(self, comment_id):
        current_comment = crud_comment.get_comment_by_id(db=self.db, comment_id=comment_id)
        if current_comment is None:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_COMMENT_NOT_FOUND)

        return current_comment

    async def list_comment(self, marketplace_id: str, skip: int, limit: int):
        current_marketplace = crud_marketplace.get_marketplace_by_id(db=self.db, marketplace_id=marketplace_id)
        if current_marketplace is None:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_MARKETPLACE_NOT_FOUND)

        total_comment, list_comment = crud_comment.list_comment(db=self.db, marketplace_id=current_marketplace.id,
                                                                skip=skip, limit=limit)
        list_comment = [CommentResponse.from_orm(item) for item in list_comment]
        result = dict(total_comment=total_comment, list_comment=list_comment)
        return result

    async def has_comment_permission(self, user_id: str, comment_id: str):
        current_comment = crud_comment.get_comment_by_id(db=self.db, comment_id=comment_id)
        if current_comment is None:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_COMMENT_NOT_FOUND)

        current_comment_by_user = crud_comment.get_comment_by_user(db=self.db, user_id=user_id, comment_id=comment_id)
        if current_comment_by_user is None:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_COMMENT_METHOD_NOT_ALLOWED)
        return current_comment_by_user

    async def create_comment_to_post(self, user_id: str, comment: CommentCreateParams):
        current_marketplace = crud_marketplace.get_marketplace_by_id(db=self.db, marketplace_id=comment.marketplace_id)
        if current_marketplace is None:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_MARKETPLACE_NOT_FOUND)

        obj_in = CommentCreate(id=str(uuid.uuid4()), content=comment.content, user_id=user_id,
                               marketplace_id=comment.marketplace_id)

        result = crud_comment.create(db=self.db, obj_in=obj_in)
        return current_marketplace, result

    async def update_comment(self, comment_id: str, comment: CommentUpdateParams):
        current_comment = crud_comment.get_comment_by_id(db=self.db, comment_id=comment_id)
        result = crud_comment.update(db=self.db, obj_in=comment, db_obj=current_comment)
        return result

    async def delete_comment(self, comment_id: str):
        result = crud_comment.remove(db=self.db, entry_id=comment_id)
        return result
