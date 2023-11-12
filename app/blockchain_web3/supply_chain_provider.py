import json
import logging

from web3.auto import w3

from app.blockchain_web3.provider import Web3Provider
from app.core.settings import settings

logger = logging.getLogger(__name__)


class SupplyChainProvider(Web3Provider):

    def __init__(self):
        with open('./app/abi/supply_chain.txt', 'r', encoding='utf-8') as f:
            abi = f.read()

        factory_abi = json.loads(abi)
        super().__init__(settings.WEB3_PROVIDER)
        self.chain_id = settings.CHAIN_ID
        self.contract = self.conn.eth.contract(address=settings.ADDRESS_CONTRACT_SUPPLY_CHAIN, abi=factory_abi)

    def get_info_product(self, product_id):
        return self.contract.functions.seek_an_origin(product_id).call()

    def listing_product_to_marketplace(self, item_id, product_id, owner, status):
        function = self.contract.functions.listing_product(item_id, product_id, owner, status)

        return self.sign_and_send_transaction(function)

    def buy_product_in_market(self, item_id, id_trans, buyer, quantity):
        function = self.contract.functions.buy_product_in_market(item_id, quantity, buyer, id_trans)
        return self.sign_and_send_transaction(function)

    def update_status_item_on_marketplace(self, item_id, status):
        function = self.contract.functions.update_item_on_marketplance(item_id, status)
        return self.sign_and_send_transaction(function)

    def sign_and_send_transaction(self, func):
        account = w3.eth.account.privateKeyToAccount(settings.PRIVATE_KEY_SYSTEM)
        nonce = self.conn.eth.getTransactionCount(account.address)
        gas = 3000000
        gas_price = self.conn.eth.gasPrice

        tx_data = func.buildTransaction(
            {'chainId': self.chain_id, 'gas': gas, 'gasPrice': gas_price, 'nonce': nonce})

        # Tạo một đối tượng giao dịch
        transaction = {
            'to': settings.WEB3_FACTORY_ADDRESS,
            'value': 0,  # Số Ether bạn muốn chuyển đi (0 trong trường hợp này)
            'gas': gas,
            'gasPrice': gas_price,
            'nonce': nonce,
            'data': tx_data['data']
        }

        signed_transaction = self.conn.eth.account.signTransaction(transaction, settings.PRIVATE_KEY_SYSTEM)

        tx_hash = self.conn.eth.sendRawTransaction(signed_transaction.rawTransaction)

        return tx_hash

    def get_transaction_by_id(self, trans_id):
        return self.contract.functions.get_transaction_by_id(trans_id).call()
