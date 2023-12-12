import uuid
import qrcode
import os

from fastapi import UploadFile, File
from sqlalchemy.orm import Session
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler
import cloudinary
from cloudinary.uploader import upload
from datetime import date

from ..blockchain_web3.supply_chain_provider import SupplyChainProvider
from ..model import User
from ..schemas import ProductType, ProductCreate, ProductUpdate, ProductResponse, TransactionSFCreate, \
    ProductFarmerCreate, TransactionFMCreate, ProductFarmerHistoryResponse, ProductManufacturerCreate, \
    ProductManufacturerHistoryResponse, GrowUpCreate, GrowUpUpdate, GrowUpResponse, LeaderboardUpdate, \
    LeaderboardCreate, ClassifyGoodsCreate, TransactionSFResponse, TransactionFMHistoryResponse, \
    TransactionSFHistoryResponse, TransactionFMResponse
from ..blockchain_web3.product_provider import ProductProvider
from ..crud import crud_product, crud_user, crud_transaction_sf, crud_transaction_fm, crud_product_farmer, \
    crud_product_manufacturer, crud_grow_up, crud_leaderboard, crud_cart, crud_classify_goods, crud_marketplace
from ..model.base import ProductStatus, UserSystemRole, ConfirmStatusProduct, ChooseProduct, ConfirmProduct
from ..utils.hash_lib import base64_encode


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

    async def get_product_trace_origin(self, product_id: str):
        current_product = crud_product.get_product_by_id(db=self.db, product_id=product_id)
        product = ProductResponse.from_orm(current_product)
        chain = await self.get_product_manufacturer_history(product_id=product_id)
        if "farmer" in chain:
            product_id = chain["farmer"]["product_id"]
            grow_up = await self.get_grow_up_trace_origin(product_id=product_id)
        else:
            grow_up = None
        result = dict(chain=chain, product=product, grow_up=grow_up)
        return result

    async def get_product_history_sale(self, current_user: User, skip: int, limit: int):
        if current_user.system_role == UserSystemRole.SEEDLING_COMPANY:
            total_transaction, list_transaction = crud_transaction_sf.get_history_sale(db=self.db,
                                                                                       user_id=current_user.id,
                                                                                       skip=skip, limit=limit)
            result = [TransactionSFHistoryResponse.from_orm(item) for item in list_transaction]
        elif current_user.system_role == UserSystemRole.FARMER:
            total_transaction, list_transaction = crud_transaction_fm.get_history_sale(db=self.db,
                                                                                       user_id=current_user.id,
                                                                                       skip=skip, limit=limit)
            result = [TransactionFMHistoryResponse.from_orm(item) for item in list_transaction]
        else:
            total_transaction = None
            result = None
        result_history = dict(total_transaction=total_transaction, list_transaction=result)
        return result_history

    async def get_product_order_by_user(self, current_user: User, skip: int, limit: int,
                                        status: ConfirmStatusProduct = None):
        if current_user.system_role == UserSystemRole.SEEDLING_COMPANY:
            total_transaction, list_transaction = (crud_transaction_sf.
                                                   get_product_order_by_user(db=self.db,
                                                                             user_id=current_user.id,
                                                                             skip=skip, limit=limit,
                                                                             status=status))
            list_transaction = [TransactionSFResponse.from_orm(item) for item in list_transaction]
        elif current_user.system_role == UserSystemRole.FARMER:
            total_transaction, list_transaction = (crud_transaction_fm.
                                                   get_product_order_by_user(db=self.db,
                                                                             user_id=current_user.id,
                                                                             skip=skip, limit=limit,
                                                                             status=status))
            list_transaction = [TransactionFMResponse.from_orm(item) for item in list_transaction]
        else:
            total_transaction = None
            list_transaction = None
        result = dict(total_transaction=total_transaction, list_transaction=list_transaction)
        return result

    async def get_product_manufacturer_history(self, product_id: str):
        current_product = crud_product.get_product_by_id(db=self.db, product_id=product_id)
        if current_product is None:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)

        if current_product.product_type == ProductType.SEEDLING_COMPANY:
            result = self.history_for_seedling_company(current_product=current_product)
        elif current_product.product_type == ProductType.FARMER:
            result, product_farmer = self.history_for_farmer(product_id=product_id)
        elif current_product.product_type == ProductType.MANUFACTURER:
            result = self.history_for_manufacturer(product_id=product_id)
        else:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)

        return result

    @staticmethod
    def history_for_seedling_company(current_product):
        seedling_company = ProductResponse.from_orm(current_product)
        seedling_company_dict = seedling_company.user.dict()
        seedling_company_dict["product_id"] = seedling_company.id
        result = dict(seedling_company=seedling_company_dict)

        return result

    def history_for_farmer(self, product_id):
        current_product_farmer = crud_product_farmer.get_product_farmer_by_product_id(db=self.db,
                                                                                      product_id=product_id)
        if not current_product_farmer:
            raise error_exception_handler(error=Exception(),
                                          app_status=AppStatus.ERROR_FARMER_PRODUCT_NOT_FOUND)
        farmer = ProductFarmerHistoryResponse.from_orm(current_product_farmer)
        farmer_dict = farmer.product.user.dict()
        farmer_dict["product_id"] = farmer.product.id

        seedling_company_dict = self.history_for_seedling_company(farmer.transactions_sf.product)
        result = dict(farmer=farmer_dict, seedling_company=seedling_company_dict["seedling_company"])
        return result, current_product_farmer

    def history_for_manufacturer(self, product_id):
        current_product_manufacturer = (crud_product_manufacturer.
                                        get_product_manufacturer_by_product_id(db=self.db, product_id=product_id))
        if not current_product_manufacturer:
            raise error_exception_handler(error=Exception(),
                                          app_status=AppStatus.ERROR_MANUFACTURER_PRODUCT_NOT_FOUND)
        manufacturer = ProductManufacturerHistoryResponse.from_orm(current_product_manufacturer)
        manufacturer_dict = manufacturer.product.user.dict()
        manufacturer_dict["product_id"] = manufacturer.product.id
        product = self.history_for_farmer(current_product_manufacturer.transactions_fm.product.id)
        result = dict(manufacturer=manufacturer_dict,
                      farmer=product[0]["farmer"],
                      seedling_company=product[0]["seedling_company"])
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
        result = [ProductResponse.from_orm(item) for item in list_product]
        for item in result:
            marketplace = crud_marketplace.get_marketplace_by_product_id(db=self.db, product_id=item.id)
            if marketplace:
                item.marketplace_id = marketplace.id
            else:
                item.marketplace_id = None
        result = dict(total_product=total_product, list_product=result)
        return result

    async def get_grow_up_trace_origin(self, product_id: str):
        current_product_farmer = crud_product_farmer.get_product_farmer_by_product_id(db=self.db, product_id=product_id)
        _, list_grow_up = (crud_grow_up.
                           get_grow_up_by_product_farmer_id(db=self.db,
                                                            product_farmer_id=current_product_farmer.id))
        return list_grow_up

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

    async def get_qr_code(self, product_id: str):
        current_product = crud_product.get_product_by_id(db=self.db, product_id=product_id)
        if current_product is None:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)
        root_folder = os.path.join(os.getcwd(), "img", "qr_code")
        image_path = os.path.join(root_folder, f"{product_id}.png")
        file_content = open(image_path, "rb")
        return file_content

    async def create_product(self, current_user: User,
                             product_create: ProductCreate,
                             banner: UploadFile = File(...)):
        banner = cloudinary.uploader.upload(banner.file, folder="banner")
        banner_url = banner.get("secure_url")
        obj_in = ProductCreate(
            id=str(uuid.uuid4()),
            name=product_create.name,
            description=product_create.description,
            banner=banner_url,
            product_type=current_user.system_role,
            price=product_create.price,
            quantity=product_create.quantity,
            product_status=ProductStatus.PRIVATE,
            created_by=current_user.id)

        result = crud_product.create(db=self.db, obj_in=obj_in)
        return result

    @staticmethod
    def permission_data(data: dict, quantity: int):
        quantity_value = 0
        for k, v in data.items():
            quantity_value += int(v["quantity"])
        if quantity_value != quantity:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_INVALID_QUANTITY)
        return quantity

    async def create_classify_goods(self, current_user: User, product_id: str,
                                    data: dict):
        current_product = crud_product.get_product_by_id(db=self.db, product_id=product_id)
        if not current_product:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)
        if current_user.system_role != UserSystemRole.FARMER:
            raise error_exception_handler(error=Exception(),
                                          app_status=AppStatus.ERROR_CLASSIFY_GOODS_METHOD_NOT_ALLOWED)
        current_classify_goods = (crud_classify_goods.
                                  get_classify_goods_by_product_id(db=self.db,
                                                                   product_id=product_id))
        if current_classify_goods:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CLASSIFY_GOODS_CONFLICT)
        self.permission_data(data=data, quantity=current_product.quantity)
        classify_goods = ClassifyGoodsCreate(
            id=str(uuid.uuid4()),
            product_id=product_id,
            data=data
        )
        crud_classify_goods.create(db=self.db, obj_in=classify_goods)
        return AppStatus.SUCCESS

    async def create_qr_code(self, product_id: str):
        current_product = crud_product.get_product_by_id(db=self.db, product_id=product_id)
        if current_product is None:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)
        qr_content = f'https://shopee.vn/product/{product_id}'
        qr = qrcode.make(qr_content)
        root_folder = os.path.join(os.getcwd(), "img", "qr_code")
        os.makedirs(root_folder, exist_ok=True)
        image_path = os.path.join(root_folder, f"{product_id}.png")
        qr.save(image_path)
        return AppStatus.SUCCESS

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
        grow_up_create = GrowUpCreate(
            id=str(uuid.uuid4()),
            product_farmer_id=current_product_farmer.id,
            description=description, image=entity_url, video=entity_url)

        result = crud_grow_up.create(db=self.db, obj_in=grow_up_create)
        product_provider = ProductProvider()
        tx_hash = product_provider.update_grow_up_product(product_id=product_id, url_image=entity_url)
        update_grow_up = dict(tx_hash=tx_hash)
        result = crud_grow_up.update(self.db, db_obj=result, obj_in=update_grow_up)
        return result

    async def update_grow_up(self, product_id: str, grow_up_update: GrowUpUpdate):
        current_product = crud_product.get_product_by_id(db=self.db, product_id=product_id)
        product_farmer = current_product.product_farmers
        current_grow_up = crud_grow_up.get_grow_up_by_id(db=self.db,
                                                         grow_up_id=product_farmer[0])

        result = crud_grow_up.update(db=self.db, db_obj=current_grow_up, obj_in=grow_up_update)
        return result

    async def update_confirm_order(self, current_user: User, transaction_id: str, status: ConfirmProduct):
        # For Seedling company

        if current_user.system_role == UserSystemRole.SEEDLING_COMPANY:
            current_transaction = crud_transaction_sf.get_transaction_sf_by_id(db=self.db,
                                                                               transaction_sf_id=transaction_id)
            if current_transaction.status != ConfirmStatusProduct.PENDING:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ORDER_IS_COMPLETED)
            if not current_transaction:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_TRANSACTION_SF_NOT_FOUND)

            buyer = crud_user.get_user_by_id(db=self.db, user_id=current_transaction.user_id)
            if status == ConfirmProduct.ACCEPT:
                current_balance_user = current_user.account_balance + current_transaction.price
                obj_in_user = dict(account_balance=current_balance_user)
                status_confirm = ConfirmStatusProduct.DONE
                crud_user.update(db=self.db, db_obj=current_user, obj_in=obj_in_user)
            else:
                current_balance_user = buyer.account_balance + current_transaction.price
                obj_in_user = dict(account_balance=current_balance_user)
                status_confirm = ConfirmStatusProduct.REJECT
                crud_user.update(db=self.db, db_obj=buyer, obj_in=obj_in_user)
            result = crud_transaction_sf.update_confirm_order(db=self.db, current_transaction=current_transaction,
                                                              status=status_confirm)
        # For Farmer
        elif current_user.system_role == UserSystemRole.FARMER:
            current_transaction = crud_transaction_fm.get_transaction_fm_by_id(db=self.db,
                                                                               transaction_fm_id=transaction_id)
            if current_transaction.status != ConfirmStatusProduct.PENDING:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ORDER_IS_COMPLETED)
            buyer = crud_user.get_user_by_id(db=self.db, user_id=current_transaction.user_id)
            if not current_transaction:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_TRANSACTION_FM_NOT_FOUND)
            if current_transaction.status == ConfirmStatusProduct.DONE:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ORDER_IS_COMPLETED)

            current_balance_user = current_user.account_balance + current_transaction.price
            if status == ConfirmProduct.ACCEPT:
                obj_in_user = dict(account_balance=current_balance_user)
                crud_user.update(db=self.db, db_obj=current_user, obj_in=obj_in_user)
                status_confirm = ConfirmStatusProduct.DONE
            else:
                current_balance_user = buyer.account_balance + current_transaction.price
                obj_in_user = dict(account_balance=current_balance_user)
                crud_user.update(db=self.db, db_obj=buyer, obj_in=obj_in_user)
                status_confirm = ConfirmStatusProduct.REJECT
            result = crud_transaction_fm.update_confirm_order(db=self.db, current_transaction=current_transaction,
                                                              status=status_confirm)

        else:
            result = None
            current_transaction = None
            buyer = None

        current_product = current_transaction.product
        return result, current_product, buyer

    async def create_product_entity(self, user_id: str, transaction_id: str,
                                    product_create: ProductCreate, banner: UploadFile = File(...)):
        current_user = crud_user.get_user_by_id(db=self.db, user_id=user_id)
        if current_user.system_role == UserSystemRole.MEMBER:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_METHOD_NOT_ALLOWED)
        product_provider = ProductProvider()
        tx_hash = None
        # Seedling company
        if current_user.system_role == UserSystemRole.SEEDLING_COMPANY:
            product_create = await self.create_product(current_user=current_user, product_create=product_create,
                                                       banner=banner)
            data_hash = dict(name=product_create.name, banner=product_create.banner)
            hash_info = base64_encode(data_hash)
            tx_hash = product_provider.create_product(product_id=product_create.id, product_type=1,
                                                      price=product_create.price, quantity=product_create.quantity,
                                                      status=1, owner=user_id, hash_info=hash_info, trans_id="")
        # Farmer
        elif current_user.system_role == UserSystemRole.FARMER:
            if transaction_id is None:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PLEASE_ADD_TRANSACTION_ID)

            current_transaction = crud_transaction_sf.get_transaction_sf_by_id(db=self.db,
                                                                               transaction_sf_id=transaction_id)

            if current_transaction is None:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_TRANSACTION_SF_NOT_FOUND)

            if current_transaction.user_id != user_id or current_transaction.status != ConfirmStatusProduct.DONE:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_METHOD_NOT_ALLOWED)

            product_create = await self.create_product(current_user=current_user,
                                                       product_create=product_create, banner=banner)
            product_farmer = ProductFarmerCreate(id=str(uuid.uuid4()),
                                                 product_id=product_create.id,
                                                 transaction_sf_id=transaction_id)
            crud_product_farmer.create(db=self.db, obj_in=product_farmer)
            data_hash = dict(name=product_create.name, banner=product_create.banner)
            hash_info = base64_encode(data_hash)
            tx_hash = product_provider.create_product(product_id=product_create.id, product_type=2,
                                                      price=product_create.price, quantity=product_create.quantity,
                                                      status=1, owner=user_id, hash_info=hash_info,
                                                      trans_id=transaction_id)

        # Manufacturer
        elif current_user.system_role == UserSystemRole.MANUFACTURER:
            if transaction_id is None:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PLEASE_ADD_TRANSACTION_ID)
            current_transaction = crud_transaction_fm.get_transaction_fm_by_id(db=self.db,
                                                                               transaction_fm_id=transaction_id)
            if current_transaction is None:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_TRANSACTION_FM_NOT_FOUND)

            if current_transaction.user_id != user_id or current_transaction.status != ConfirmStatusProduct.DONE:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_METHOD_NOT_ALLOWED)

            if current_transaction.is_choose == ChooseProduct.DONE:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_TRANSACTION_FM_CONFLICT)

            product_create = await self.create_product(current_user=current_user,
                                                       product_create=product_create, banner=banner)
            product_manufacturer = ProductManufacturerCreate(id=str(uuid.uuid4()),
                                                             product_id=product_create.id,
                                                             transaction_fm_id=transaction_id)
            update_status = dict(is_choose=ChooseProduct.DONE)
            crud_transaction_fm.update(db=self.db, db_obj=current_transaction, obj_in=update_status)
            crud_product_manufacturer.create(db=self.db, obj_in=product_manufacturer)
            data_hash = dict(name=product_create.name, banner=product_create.banner)
            hash_info = base64_encode(data_hash)
            tx_hash = product_provider.create_product(product_id=product_create.id, product_type=3,
                                                      price=product_create.price, quantity=product_create.quantity,
                                                      status=1, owner=user_id, hash_info=hash_info,
                                                      trans_id=transaction_id)
        if current_user.system_role in [UserSystemRole.MANUFACTURER, UserSystemRole.FARMER,
                                        UserSystemRole.SEEDLING_COMPANY]:
            crud_product.update(db=self.db, db_obj=product_create, obj_in=dict(tx_hash=tx_hash))
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
        if product_update.data:
            if current_product.product_type == ProductType.FARMER and (
                    product_update.quantity is not None or product_update.price is not None):
                classify_goods = crud_classify_goods.get_classify_goods_by_product_id(db=self.db, product_id=product_id)
                if product_update.quantity is not None:
                    self.permission_data(data=product_update.data, quantity=product_update.quantity)
                if product_update.price is not None and not product_update.quantity:
                    self.permission_data(data=product_update.data, quantity=current_product.quantity)
                if classify_goods:
                    if not product_update.data:
                        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PLEASE_ADD_DATA)
                    crud_classify_goods.update_data(db=self.db,
                                                    current_classify_goods=classify_goods,
                                                    data=product_update.data)
                else:
                    classify_goods = ClassifyGoodsCreate(
                        id=str(uuid.uuid4()),
                        product_id=product_id,
                        data=product_update.data
                    )
                    crud_classify_goods.create(db=self.db, obj_in=classify_goods)
                    crud_product.update(db=self.db, db_obj=current_product, obj_in=product_update)
        else:
            pass
        del product_update.data
        result = crud_product.update(db=self.db, db_obj=current_product, obj_in=product_update)
        product_provider = ProductProvider()
        data_hash = dict(name=result.name, banner=result.banner)
        hash_info = base64_encode(data_hash)
        product_provider.update_product(product_id=result.id, price=result.price, quantity=result.quantity,
                                        hash_info=hash_info)
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

        product_provider = ProductProvider()
        map_status = {"PRIVATE": 1, "PUBLISH": 2, "CLOSE": 3}
        product_provider.update_status_product(product_id=product_id, status=map_status[product_status])
        return result

    @staticmethod
    def update_quantity_product(product_quantity: int, purchase_quantity: int):
        result = product_quantity - purchase_quantity
        return result

    @staticmethod
    def check_positive_value(value, error_message):
        if value <= 0:
            raise error_exception_handler(error=Exception(), app_status=error_message)

    async def purchase_product(self, user_id: str, product_id: str,
                               buy_all: bool, price: int,
                               quantity: int, kg_type: int,
                               receiver: str, phone_number: str,
                               address: str, cart_id: str = None):
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

            if buy_all:
                quantity = current_product.quantity
                price = current_product.price * quantity
            self.check_positive_value(price, AppStatus.ERROR_INVALID_PRICE)
            self.check_positive_value(quantity, AppStatus.ERROR_INVALID_QUANTITY)

            create_transaction_sf = TransactionSFCreate(
                id=str(uuid.uuid4()),
                user_id=user_id,
                product_id=product_id,
                price=price,
                quantity=quantity,
                status=ConfirmStatusProduct.PENDING,
                receiver=receiver,
                phone_number=phone_number,
                address=address,
                order_by=current_product.created_by
            )
            # breakpoint()

            supply_chain_provider = SupplyChainProvider()
            tx_hash = supply_chain_provider.buy_product_in_market(product_id=product_id,
                                                                  id_trans=create_transaction_sf.id,
                                                                  quantity=quantity,
                                                                  type_product="",
                                                                  buyer=create_transaction_sf.user_id)
            create_transaction_sf.tx_hash = tx_hash
            result = crud_transaction_sf.create(db=self.db, obj_in=create_transaction_sf)
        # Purchase for Manufacturer
        elif current_user.system_role == UserSystemRole.MANUFACTURER:
            if current_product.product_type != ProductType.FARMER:
                raise error_exception_handler(error=Exception(),
                                              app_status=AppStatus.ERROR_PURCHASE_PRODUCT_TYPE_INVALID)
            self.check_positive_value(price, AppStatus.ERROR_INVALID_PRICE)
            self.check_positive_value(quantity, AppStatus.ERROR_INVALID_QUANTITY)
            if buy_all:
                quantity, price = self.total_price(current_product=current_product)
                self.update_data_by_product(current_product=current_product)
            else:
                if not kg_type:
                    raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PLEASE_ADD_KG_TYPE)
                self.update_classify_goods_by_kg(product_id=product_id, quantity=quantity, kg=kg_type)

            create_transaction_fm = TransactionFMCreate(
                id=str(uuid.uuid4()),
                user_id=user_id,
                product_id=product_id,
                price=price,
                quantity=quantity,
                status=ConfirmStatusProduct.PENDING,
                is_choose=ChooseProduct.NONE,
                receiver=receiver,
                phone_number=phone_number,
                address=address,
                order_by=current_product.created_by
            )

            supply_chain_provider = SupplyChainProvider()
            tx_hash = supply_chain_provider.buy_product_in_market(product_id=product_id,
                                                                  id_trans=create_transaction_fm.id,
                                                                  quantity=quantity,
                                                                  type_product="", buyer=create_transaction_fm.user_id)
            create_transaction_fm.tx_hash = tx_hash
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

    def total_price(self, current_product):
        current_classify_goods = crud_classify_goods.get_classify_goods_by_product_id(db=self.db,
                                                                                      product_id=current_product.id)
        data = current_classify_goods.data
        quantity = current_product.quantity
        price = 0
        for k, v in data.items():
            total_amount_tmp = (v["quantity"] * v["price"])
            price += total_amount_tmp
        return quantity, price

    def update_classify_goods_by_kg(self, product_id: str, quantity: int, kg: int):
        current_classify_goods = crud_classify_goods.get_classify_goods_by_product_id(db=self.db, product_id=product_id)
        data = current_classify_goods.data
        current_quantity = data[str(kg)]["quantity"]
        if int(current_quantity) < int(quantity):
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_INVALID_QUANTITY)
        data[str(kg)]["quantity"] = int(current_quantity) - int(quantity)
        crud_classify_goods.update_data(db=self.db, current_classify_goods=current_classify_goods, data=data)

    def update_data_by_product(self, current_product):
        current_classify_goods = crud_classify_goods.get_classify_goods_by_product_id(db=self.db,
                                                                                      product_id=current_product.id)
        data = current_classify_goods.data
        for key in data:
            data[key]["quantity"] = 0
        crud_classify_goods.update_data(db=self.db, current_classify_goods=current_classify_goods, data=data)
        return data

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
