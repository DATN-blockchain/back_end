from fastapi import APIRouter

from app.api.endpoint import (user, product, marketplace, transaction_sf,
                              transaction_fm, comment, reply_comment, notification)

route = APIRouter()

route.include_router(user.router, tags=["users"])
route.include_router(product.router, tags=["products"])
route.include_router(marketplace.router, tags=["marketplaces"])
route.include_router(comment.router, tags=["comments"])
route.include_router(reply_comment.router, tags=["reply_comments"])
route.include_router(transaction_sf.router, tags=["transactions_sf"])
route.include_router(transaction_fm.router, tags=["transactions_fm"])
route.include_router(notification.router, tags=["notifications"])
