from fastapi import APIRouter

from app.api.endpoint import user, product, marketplace, transaction_sf, transaction_fm

route = APIRouter()

route.include_router(user.router, tags=["users"])
route.include_router(product.router, tags=["products"])
route.include_router(transaction_sf.router, tags=["transactions_sf"])
route.include_router(transaction_fm.router, tags=["transactions_fm"])
route.include_router(marketplace.router, tags=["marketplaces"])
