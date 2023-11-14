import json

from app.blockchain_web3.provider import Web3Provider
from app.core.settings import settings


class ProductProvider(Web3Provider):

    def __init__(self):
        with open('./app/abi/actor.txt', 'r', encoding='utf-8') as f:
            abi = f.read()

        factory_abi = json.loads(abi)
        super().__init__(settings.WEB3_PROVIDER)
        self.chain_id = settings.CHAIN_ID
        self.contract = self.conn.eth.contract(address=settings.ADDRESS_CONTRACT_PRODUCT_MANAGER, abi=factory_abi)

    def create_product(self, product_id, product_type, price, quantity, trans_id, status, owner, hash_info):
        function = self.contract.functions.create(product_id, product_type, price, quantity, trans_id, status, owner,
                                                  hash_info)
        tx_hash = self.sign_and_send_transaction(self.conn, function)
        self.wait_for_transaction_confirmation(self.conn, tx_hash)
        return tx_hash

    def update_product(self, product_id, product_type, price, quantity, hash_info):
        function = self.contract.functions.update(product_id, product_type, price, quantity, hash_info)
        tx_hash = self.sign_and_send_transaction(self.conn, function)
        self.wait_for_transaction_confirmation(self.conn, tx_hash)
        return tx_hash

    def get_product_by_id(self, product_id):
        return self.contract.functions.readOneProduct(product_id).call()

    def update_grow_up_product(self, product_id, url_image):
        function = self.contract.functions.updateGrowUpProduct(product_id, url_image)
        tx_hash = self.sign_and_send_transaction(self.conn, function)
        self.wait_for_transaction_confirmation(self.conn, tx_hash)
        return tx_hash
