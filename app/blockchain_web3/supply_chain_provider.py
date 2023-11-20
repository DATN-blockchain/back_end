import json
import logging

from app.blockchain_web3.provider import Web3Provider
from app.core.settings import settings

logger = logging.getLogger(__name__)


class SupplyChainProvider(Web3Provider):

    def __init__(self):
        with open('./app/abi/supply_chain.txt', 'r', encoding='utf-8') as f:
            abi = f.read()

        factory_abi = json.loads(abi)
        super().__init__(settings.WEB3_PROVIDER, settings.ADDRESS_CONTRACT_SUPPLY_CHAIN)
        self.chain_id = settings.CHAIN_ID
        self.contract = self.w3.eth.contract(address=settings.ADDRESS_CONTRACT_SUPPLY_CHAIN, abi=factory_abi)

    def get_info_product(self, product_id):
        return self.contract.functions.seek_an_origin(product_id).call()

    def listing_product_to_marketplace(self, item_id, product_id, owner, status):
        function = self.contract.functions.listing_product(item_id, product_id, owner, status)
        tx_hash = self.sign_and_send_transaction(function)
        return tx_hash

    def buy_product_in_market(self, product_id, id_trans, buyer, quantity, type_product):
        function = self.contract.functions.buy_product_in_market(product_id, quantity, buyer, id_trans, type_product)
        tx_hash = self.sign_and_send_transaction(function)
        return tx_hash

    def update_status_item_on_marketplace(self, item_id, status):
        function = self.contract.functions.update_item_on_marketplance(item_id, status)
        tx_hash = self.sign_and_send_transaction(function)
        return tx_hash

    def get_transaction_by_id(self, trans_id):
        return self.contract.functions.get_transaction_by_id(trans_id).call()
