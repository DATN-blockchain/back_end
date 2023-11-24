import json
import logging
import os
import uuid

from app.blockchain_web3.provider import Web3Provider
from app.core.settings import settings

logger = logging.getLogger(__name__)


class SupplyChainProvider(Web3Provider):

    def __init__(self):
        path_abi = os.path.join(os.getcwd(), "app/abi/supply_chain.txt")
        with open(path_abi, 'r', encoding='utf-8') as f:
            abi = f.read()

        factory_abi = json.loads(abi)
        super().__init__(settings.WEB3_PROVIDER, settings.ADDRESS_CONTRACT_SUPPLY_CHAIN)
        self.chain_id = settings.CHAIN_ID
        self.contract = self.w3.eth.contract(address=settings.ADDRESS_CONTRACT_SUPPLY_CHAIN, abi=factory_abi)

    def get_info_product(self, product_id):
        return self.contract.functions.seek_an_origin(product_id).call()

    def listing_product_to_marketplace(self, item_id, product_id, owner):
        function = self.contract.functions.listing_product(item_id, product_id, owner)
        tx_hash = self.sign_and_send_transaction(function)
        return tx_hash

    def buy_product_in_market(self, product_id, id_trans, buyer, quantity, type_product):
        function = self.contract.functions.buy_item_on_marketplace(product_id, buyer, id_trans, quantity, type_product)
        tx_hash = self.sign_and_send_transaction(function)
        return tx_hash

    def update_status_item_on_marketplace(self, item_id, status):
        function = self.contract.functions.update_item_on_marketplance(item_id, status)
        tx_hash = self.sign_and_send_transaction(function)
        return tx_hash

    def get_transaction_by_id(self, trans_id):
        return self.contract.functions.get_transaction_by_id(trans_id).call()

if __name__ == "__main__":
    provider = SupplyChainProvider()
    product = provider.get_info_product(product_id="3b9fc13a-4bd6-4ed8-a761-67e404d53dcd")
    print(product)
    tx_hash = provider.listing_product_to_marketplace(uuid.uuid4().__str__(), "3b9fc13a-4bd6-4ed8-a761-67e404d53dcd", "a98c4ce8-2fee-4ad4-9652-8848f3afe50d")
    print(tx_hash)