import uuid
from fastapi import UploadFile, File

from sqlalchemy.orm import Session
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler
import cloudinary
from cloudinary.uploader import upload
from datetime import date

from ..blockchain_web3.product_provider import ProductProvider
from ..model import User
from ..schemas import ProductType, ProductCreate, ProductUpdate, ProductResponse, TransactionSFCreate, \
    ProductFarmerCreate, TransactionFMCreate, ProductFarmerHistoryResponse, ProductManufacturerCreate, \
    ProductManufacturerHistoryResponse, GrowUpCreate, GrowUpUpdate, GrowUpResponse, LeaderboardUpdate, \
    LeaderboardCreate
from ..blockchain_web3.product_provider import ProductProvider
from ..crud import crud_product, crud_user, crud_transaction_sf, crud_transaction_fm, crud_product_farmer, \
    crud_product_manufacturer, crud_grow_up, crud_leaderboard, crud_cart
from ..model.base import ProductStatus, UserSystemRole
from app.utils.encode_decode_json import encode_json
from app.constant.mapping_enum import PRODUCT_TYPE


class ProductService:
    def __init__(self, db: Session):
        self.db = db

    async def get_product_by_id(self, product_id: str):
        current_product = crud_product.get_product_by_id(db=self.db, product_id=product_id)
        if not current_product:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)
        crud_product.update_product_view(db=self.db, current_product=current_product)
        result = ProductResponse.from_orm(current_product)
        return result

    async def get_product_top_selling(self, product_type: str):
        top_selling = crud_product.get_product_top_selling(db=self.db, product_type=product_type)
        return top_selling

    async def get_product_chart(self, product_id: str):
        current_product = crud_product.get(db=self.db, entry_id=product_id)
        if current_product is None:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)
        data_chart = crud_product.get_chart_product(db=self.db, product_id=product_id)
        return data_chart

    async def get_product_seedling_company_history(self, product_id: str):
        current_product = crud_product.get_product_by_id(db=self.db, product_id=product_id)
        if not (current_product and current_product.product_type == ProductType.SEEDLING_COMPANY):
            raise error_exception_handler(error=Exception(),
                                          app_status=AppStatus.ERROR_SEEDLING_COMPANY_PRODUCT_NOT_FOUND)
        result = ProductResponse.from_orm(current_product)

        return result

    async def get_product_farmer_history(self, product_id: str):
        current_product_farmer = crud_product_farmer.get_product_farmer_by_product_id(db=self.db, product_id=product_id)
        if not current_product_farmer:
            raise error_exception_handler(error=Exception(),
                                          app_status=AppStatus.ERROR_FARMER_PRODUCT_NOT_FOUND)
        result = ProductFarmerHistoryResponse.from_orm(current_product_farmer)

        return result

    async def get_product_history(self, product_id: str):
        current_product = crud_product.get_product_by_id(db=self.db, product_id=product_id)
        if current_product is None:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)
        if current_product.product_type == ProductType.SEEDLING_COMPANY:
            result = ProductResponse.from_orm(current_product)
        elif current_product.product_type == ProductType.FARMER:
            current_product_farmer = crud_product_farmer.get_product_farmer_by_product_id(db=self.db,
                                                                                          product_id=product_id)
            if not current_product_farmer:
                raise error_exception_handler(error=Exception(),
                                              app_status=AppStatus.ERROR_FARMER_PRODUCT_NOT_FOUND)
            result = ProductFarmerHistoryResponse.from_orm(current_product_farmer)
        elif current_product.product_type == ProductType.MANUFACTURER:
            current_product_manufacturer = (crud_product_manufacturer.
                                            get_product_manufacturer_by_product_id(db=self.db, product_id=product_id))
            if not current_product_manufacturer:
                raise error_exception_handler(error=Exception(),
                                              app_status=AppStatus.ERROR_MANUFACTURER_PRODUCT_NOT_FOUND)
            result = ProductManufacturerHistoryResponse.from_orm(current_product_manufacturer)
        else:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)
        return result

    async def get_product_by_me(self, user_id: str, name: str, skip: int, limit: int):
        current_product = crud_product.get_product_by_me(db=self.db, user_id=user_id, name=name,
                                                         skip=skip, limit=limit)
        if not current_product:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)

        return current_product

    async def list_product(self, name: str, user_id: str, skip: int, limit: int):
        total_product, list_product = crud_product.list_product(db=self.db, name=name, user_id=user_id,
                                                                skip=skip, limit=limit)
        list_product = [ProductResponse.from_orm(item) for item in list_product]
        result = dict(total_product=total_product, list_product=list_product)
        return result

    async def get_product_grow_up(self, product_id: str, from_date: date, to_date: date, skip: int, limit: int):
        current_product_farmer = crud_product_farmer.get_product_farmer_by_product_id(db=self.db, product_id=product_id)
        if current_product_farmer is None:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_FARMER_NOT_FOUND)
        total_grow_up, list_grow_up = (crud_grow_up.
                                       get_grow_up_by_product_farmer_id(db=self.db,
                                                                        product_farmer_id=current_product_farmer.id,
                                                                        from_date=from_date,
                                                                        to_date=to_date,
                                                                        skip=skip,
                                                                        limit=limit))
        list_grow_up = [GrowUpResponse.from_orm(item) for item in list_grow_up]
        result = dict(total_grow_up=total_grow_up, list_grow_up=list_grow_up)
        return result

    async def create_product(self, current_user: User, product_create: ProductCreate, banner: UploadFile = File(...)):
        banner = cloudinary.uploader.upload(banner.file, folder="banner")
        banner_url = banner.get("secure_url")
        product_provider = ProductProvider()
        product_create = ProductCreate(
            id=str(uuid.uuid4()),
            name=product_create.name,
            description=product_create.description,
            banner=banner_url,
            product_type=current_user.system_role,
            price=product_create.price,
            quantity=product_create.quantity,
            product_status=ProductStatus.PRIVATE,
            created_by=current_user.id)
        # info = dict(name=product_create.name,
        #             description=product_create.description,
        #             banner=product_create.banner)
        # hash_info = encode_json(data=info)
        #
        # tx_hash = product_provider.create_product(product_id=product_create.id,
        #                                           product_type=PRODUCT_TYPE[product_create.product_type],
        #                                           price=product_create.price,
        #                                           quantity=product_create.quantity,
        #                                           status=product_create.product_status,
        #                                           owner=product_create.created_by,
        #                                           hash_info=hash_info)
        # product_create.tx_hash = tx_hash
        result = crud_product.create(db=self.db, obj_in=product_create)
        return result

    async def create_grow_up(self, product_id: str, description: str, image: UploadFile = File(...),
                             video: UploadFile = File(...)):

        if not image and not video or (image and video):
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_INVALID_INPUT)

        current_product_farmer = crud_product_farmer.get_product_farmer_by_product_id(db=self.db, product_id=product_id)
        if current_product_farmer is None:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_FARMER_NOT_FOUND)

        if image:
            image = cloudinary.uploader.upload(image.file, folder="image_grow_up")
            entity_url = image.get("secure_url")
        else:
            try:
                upload_result = cloudinary.uploader.upload(video.file, resource_type='video', folder="video_grow_up")
                entity_url = upload_result['url']
            except Exception as error:
                raise error_exception_handler(error=error, app_status=AppStatus.ERROR_BAD_REQUEST)
        product_provider = ProductProvider()
        grow_up_create = GrowUpCreate(
            id=str(uuid.uuid4()),
            product_farmer_id=current_product_farmer.id,
            description=description, image=entity_url, video=entity_url)
        # tx_hash = product_provider.update_grow_up_product(product_id=grow_up_create.product_farmer_id,
        #                                                   url_image=entity_url)
        # grow_up_create.tx_hash = tx_hash

        result = crud_grow_up.create(db=self.db, obj_in=grow_up_create)
        return result

    async def update_grow_up(self, product_id: str, grow_up_update: GrowUpUpdate):
        current_product = crud_product.get_product_by_id(db=self.db, product_id=product_id)
        product_farmer = current_product.product_farmers
        current_grow_up = crud_grow_up.get_grow_up_by_id(db=self.db,
                                                         grow_up_id=product_farmer[0])

        result = crud_grow_up.update(db=self.db, db_obj=current_grow_up, obj_in=grow_up_update)
        return result

    async def create_product_entity(self, user_id: str, transaction_id: str,
                                    product_create: ProductCreate, banner: UploadFile = File(...)):

        current_user = crud_user.get_user_by_id(db=self.db, user_id=user_id)
        if current_user.system_role == UserSystemRole.MEMBER:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_METHOD_NOT_ALLOWED)

        # Seedling company
        if current_user.system_role == UserSystemRole.SEEDLING_COMPANY:
            product_create = await self.create_product(current_user=current_user, product_create=product_create,
                                                       banner=banner)

        # Farmer
        elif current_user.system_role == UserSystemRole.FARMER:
            if transaction_id is None:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PLEASE_ADD_TRANSACTION_ID)

            current_transaction = crud_transaction_sf.get_transaction_sf_by_id(db=self.db,
                                                                               transaction_sf_id=transaction_id)

            if current_transaction is None:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_TRANSACTION_SF_NOT_FOUND)

            if current_transaction.user_id != user_id:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_METHOD_NOT_ALLOWED)

            product_create = await self.create_product(current_user=current_user,
                                                       product_create=product_create, banner=banner)
            product_farmer = ProductFarmerCreate(id=str(uuid.uuid4()),
                                                 product_id=product_create.id,
                                                 transaction_sf_id=transaction_id)
            crud_product_farmer.create(db=self.db, obj_in=product_farmer)

        # Manufacturer
        elif current_user.system_role == UserSystemRole.MANUFACTURER:
            if transaction_id is None:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PLEASE_ADD_TRANSACTION_ID)
            current_transaction = crud_transaction_fm.get_transaction_fm_by_id(db=self.db,
                                                                               transaction_fm_id=transaction_id)
            if current_transaction is None:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_TRANSACTION_FM_NOT_FOUND)

            if current_transaction.user_id != user_id:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_METHOD_NOT_ALLOWED)

            if current_transaction.status == False:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_TRANSACTION_FM_CONFLICT)

            product_create = await self.create_product(current_user=current_user,
                                                       product_create=product_create, banner=banner)
            product_manufacturer = ProductManufacturerCreate(id=str(uuid.uuid4()),
                                                             product_id=product_create.id,
                                                             transaction_fm_id=transaction_id)
            update_status = dict(status=False)
            crud_transaction_fm.update(db=self.db, db_obj=current_transaction, obj_in=update_status)
            crud_product_manufacturer.create(db=self.db, obj_in=product_manufacturer)

        self.db.refresh(product_create)
        return product_create

    async def has_product_permissions(self, user_id: str, product_id: str):
        current_product = crud_product.get_product_by_id(db=self.db, product_id=product_id)
        if not current_product:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)
        if current_product.created_by != user_id:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_METHOD_NOT_ALLOWED)
        return current_product

    async def update_product(self, product_id: str, product_update: ProductUpdate):
        current_product = crud_product.get_product_by_id(db=self.db, product_id=product_id)
        result = crud_product.update(db=self.db, db_obj=current_product, obj_in=product_update)
        return result

    async def update_banner(self, product_id: str, banner: UploadFile):
        current_product = crud_product.get_product_by_id(db=self.db, product_id=product_id)
        uploaded_banner = upload(banner.file)
        banner_url = uploaded_banner['secure_url']
        product_update = dict(banner=banner_url)
        crud_user.update(db=self.db, db_obj=current_product, obj_in=product_update)
        return AppStatus.SUCCESS

    async def update_product_status(self, product_id: str, product_status: ProductStatus):
        current_product = crud_product.get_product_by_id(db=self.db, product_id=product_id)

        result = crud_product.update_product_status(db=self.db, current_product=current_product,
                                                    product_status=product_status)
        return result

    @staticmethod
    def update_quantity_product(product_quantity: int, purchase_quantity: int):
        result = product_quantity - purchase_quantity
        return result

    @staticmethod
    def check_positive_value(value, error_message):
        if value <= 0:
            raise error_exception_handler(error=Exception(), app_status=error_message)

    async def purchase_product(self, user_id: str, product_id: str, price: int, quantity: int, cart_id: str = None):
        current_product = crud_product.get_product_by_id(db=self.db, product_id=product_id)
        current_user = crud_user.get_user_by_id(db=self.db, user_id=user_id)

        if current_product is None:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)
        if current_product.created_by == user_id:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_METHOD_NOT_ALLOWED)
        if current_product.quantity < quantity:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_INVALID_QUANTITY)
        if current_user.account_balance < price:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_YOU_BALANCE_IS_INSUFFICIENT)
        if cart_id:
            current_cart = crud_cart.get_cart_by_id(db=self.db, cart_id=cart_id)
            if not current_cart:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CART_NOT_FOUND)
        else:
            current_cart = None

        # Purchase for Farmer
        if current_user.system_role == UserSystemRole.FARMER:
            if current_product.product_type != ProductType.SEEDLING_COMPANY:
                raise error_exception_handler(error=Exception(),
                                              app_status=AppStatus.ERROR_PURCHASE_PRODUCT_TYPE_INVALID)
            self.check_positive_value(price, AppStatus.ERROR_INVALID_PRICE)
            self.check_positive_value(quantity, AppStatus.ERROR_INVALID_QUANTITY)

            create_transaction_sf = TransactionSFCreate(
                id=str(uuid.uuid4()),
                user_id=user_id,
                product_id=product_id,
                price=price,
                quantity=quantity
            )
            result = crud_transaction_sf.create(db=self.db, obj_in=create_transaction_sf)

        # Purchase for Manufacturer
        elif current_user.system_role == UserSystemRole.MANUFACTURER:
            if current_product.product_type != ProductType.FARMER:
                raise error_exception_handler(error=Exception(),
                                              app_status=AppStatus.ERROR_PURCHASE_PRODUCT_TYPE_INVALID)
            self.check_positive_value(price, AppStatus.ERROR_INVALID_PRICE)
            self.check_positive_value(quantity, AppStatus.ERROR_INVALID_QUANTITY)
            create_transaction_fm = TransactionFMCreate(
                id=str(uuid.uuid4()),
                user_id=user_id,
                product_id=product_id,
                price=price,
                quantity=quantity
            )
            result = crud_transaction_fm.create(db=self.db, obj_in=create_transaction_fm)
        else:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_YOU_ARE_NOT_ALLOWED)

        update_quantity = self.update_quantity_product(product_quantity=current_product.quantity,
                                                       purchase_quantity=quantity)

        current_number_of_sales = current_product.number_of_sales + 1
        obj_in = dict(quantity=update_quantity, number_of_sales=current_number_of_sales)
        crud_product.update(db=self.db, db_obj=current_product, obj_in=obj_in)
        self.create_leader_board(user_id=current_product.created_by, quantity_sales=quantity)

        crud_user.update_account_balance(db=self.db, current_user=current_user, product_price=price)
        if current_cart:
            crud_cart.remove(db=self.db, entry_id=cart_id)

        self.db.refresh(result)
        return result, current_product

    def create_leader_board(self, user_id, quantity_sales):
        current_leaderboard = crud_leaderboard.get_leaderboard_by_user_id(db=self.db, user_id=user_id)
        if current_leaderboard:
            new_number_of_sales = current_leaderboard.number_of_sales + 1
            new_quantity_sales = current_leaderboard.number_of_sales + quantity_sales
            obj_in = LeaderboardUpdate(number_of_sales=new_number_of_sales, quantity_sales=new_quantity_sales)
            leaderboard = crud_leaderboard.update(db=self.db, db_obj=current_leaderboard, obj_in=obj_in)
        else:
            obj_in = LeaderboardCreate(
                id=str(uuid.uuid4()),
                user_id=user_id,
                number_of_sales=1,
                quantity_sales=quantity_sales
            )
            leaderboard = crud_leaderboard.create(db=self.db, obj_in=obj_in)
        return leaderboard

    async def delete_product(self, product_id: str):
        current_product = crud_product.get_product_by_id(db=self.db, product_id=product_id)
        if not current_product:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)

        result = crud_product.soft_remove(db=self.db, entry_id=product_id)
        return result
