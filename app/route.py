from fastapi import APIRouter

from app.api.endpoint import user, product, marketplace

route = APIRouter()

route.include_router(user.router, tags=["users"])
route.include_router(product.router, tags=["products"])
route.include_router(marketplace.router, tags=["marketplaces"])
