import json

from app.blockchain_web3.provider import Web3Provider
from app.core.settings import settings


class ProductProvider(Web3Provider):

    def __init__(self):
        with open('./app/abi/product.txt', 'r', encoding='utf-8') as f:
            abi = f.read()

        factory_abi = json.loads(abi)
        super().__init__(settings.WEB3_PROVIDER, settings.ADDRESS_CONTRACT_PRODUCT_MANAGER)
        self.chain_id = settings.CHAIN_ID
        self.contract = self.w3.eth.contract(address=settings.ADDRESS_CONTRACT_PRODUCT_MANAGER, abi=factory_abi)

    def create_product(self, product_id, product_type, price, quantity, status, owner, hash_info, trans_id=None):
        function = self.contract.functions.create(product_id, product_type, price, quantity, trans_id, status, owner,
                                                  hash_info)
        tx_hash = self.sign_and_send_transaction(function)
        return tx_hash

    def update_product(self, product_id, price, quantity, hash_info):
        function = self.contract.functions.update(product_id, price, quantity, hash_info)
        tx_hash = self.sign_and_send_transaction(function)
        return tx_hash

    def get_product_by_id(self, product_id):
        return self.contract.functions.readOneProduct(product_id).call()

    def update_grow_up_product(self, product_id, url_image):
        function = self.contract.functions.updateGrowUpProduct(product_id, url_image)
        tx_hash = self.sign_and_send_transaction(function)
        return tx_hash

    def create_price_detail_for_product(self, product_id: str, type_products: list, list_quantity: list):
        function = self.contract.functions.create_price_detail_of_type(product_id, type_products, list_quantity)
        tx_hash = self.sign_and_send_transaction(function)
        return tx_hash

    def update_status_product(self, product_id: str, status: int):
        function = self.contract.functions.update_status_product(product_id, status)
        tx_hash = self.sign_and_send_transaction(function)
        return tx_hash

    def update_price_detail_for_product(self, product_id: str, type_product: str, price: int, quantity: int):
        function = self.contract.functions.update_price_and_type_of_type(product_id, type_product, price, quantity)
        tx_hash = self.sign_and_send_transaction(function)
        return tx_hash

    def get_price_detail_of_product(self, product_id, type_product: str):
        return self.contract.functions.get_price_detail_of_product(product_id, type_product).call()

    def get_list_type_product(self, product_id: str):
        return self.contract.functions.get_list_type_product(product_id).call()
