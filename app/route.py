from fastapi import APIRouter

from app.api.endpoint import (user, product, marketplace, transaction_sf,
                              transaction_fm, comment, reply_comment,
                              notification, activity, financial_transaction,
                              leaderboard, cart)

route = APIRouter()

route.include_router(user.router, tags=["users"])
route.include_router(product.router, tags=["products"])
route.include_router(marketplace.router, tags=["marketplaces"])
route.include_router(comment.router, tags=["comments"])
route.include_router(reply_comment.router, tags=["reply_comments"])
route.include_router(cart.router, tags=["carts"])
route.include_router(transaction_sf.router, tags=["transactions_sf"])
route.include_router(transaction_fm.router, tags=["transactions_fm"])
route.include_router(financial_transaction.router, tags=["financial_transactions"])
route.include_router(notification.router, tags=["notifications"])
route.include_router(activity.router, tags=["activities"])
route.include_router(leaderboard.router, tags=["leaderboards"])
