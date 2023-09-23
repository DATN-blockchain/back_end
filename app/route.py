from fastapi import APIRouter

from app.api.endpoint import user, product

route = APIRouter()

route.include_router(user.router, tags=["users"])
route.include_router(product.router, tags=["products"])
