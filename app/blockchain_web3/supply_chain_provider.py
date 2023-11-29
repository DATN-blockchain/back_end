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
        return self.sign_and_send_transaction(function)

    def buy_product_in_market(self, product_id, id_trans, buyer, quantity, type_product):
        function = self.contract.functions.buy_item_on_marketplace(product_id, id_trans, buyer, quantity, type_product)
        return self.sign_and_send_transaction(function)

    def update_transaction_status(self, item_id, status):
        function = self.contract.functions.update_status_transaction(item_id, status)
        return self.sign_and_send_transaction(function)

    def get_transaction_by_id(self, trans_id):
        return self.contract.functions.get_transaction_by_id(trans_id).call()


if __name__ == "__main__":
    provider = SupplyChainProvider()
    product = provider.get_info_product(product_id="1dbc3a9c-e7b8-4b7c-9b02-56861e28f0d7")
    print(product)
    tx_hash = provider.buy_product_in_market(product_id="1dbc3a9c-e7b8-4b7c-9b02-56861e28f0d7",
                                             id_trans=uuid.uuid4().__str__(),
                                             buyer="a98c4ce8-2fee-4ad4-9652-8848f3afe50d", quantity=10, type_product="")
    print(tx_hash)
