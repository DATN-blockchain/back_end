import json
import logging
from web3.auto import w3

from app.blockchain_web3.provider import Web3Provider
from app.core.settings import settings

logger = logging.getLogger(__name__)


class SupplyChainRouterProvider(Web3Provider):

    def __init__(self):
        with open('./app/abi/supply_chain.txt', 'r', encoding='utf-8') as f:
            abi = f.read()

        factory_abi = json.loads(abi)
        super().__init__(settings.WEB3_PROVIDER)
        self.contract = self.conn.eth.contract(address=settings.WEB3_FACTORY_ADDRESS, abi=factory_abi)

    def create_actor(self, id, address, type, private_key):
        nonce = self.conn.eth.getTransactionCount(address)
        gas = 3000000
        gas_price = self.conn.toWei('3000', 'gwei')

        function = self.contract.functions.create_actor(id, address, type)
        tx_data = function.buildTransaction({'chainId': 97, 'gas': gas, 'gasPrice': gas_price, 'nonce': nonce})

        # Tạo một đối tượng giao dịch
        transaction = {
            'to': settings.WEB3_FACTORY_ADDRESS,
            'value': 0,  # Số Ether bạn muốn chuyển đi (0 trong trường hợp này)
            'gas': gas,
            'gasPrice': gas_price,
            'nonce': nonce,
            'data': tx_data['data']
        }

        signed_transaction = self.conn.eth.account.signTransaction(transaction, private_key)

        tx_hash = self.conn.eth.sendRawTransaction(signed_transaction.rawTransaction)

        return tx_hash

    def create_product(self, product_id, product_type, price, quantity, transaction_id, status, owner, private_key):
        account = w3.eth.account.privateKeyToAccount(private_key)
        nonce = self.conn.eth.getTransactionCount(account.address)
        gas = 3000000
        gas_price = self.conn.eth.gasPrice

        function = self.contract.functions.create_product(product_id, product_type, price, quantity, transaction_id,
                                                          status, owner)

        tx_data = function.buildTransaction({'chainId': 97, 'gas': gas, 'gasPrice': gas_price, 'nonce': nonce})

        # Tạo một đối tượng giao dịch
        transaction = {
            'to': settings.WEB3_FACTORY_ADDRESS,
            'value': 0,  # Số Ether bạn muốn chuyển đi (0 trong trường hợp này)
            'gas': gas,
            'gasPrice': gas_price,
            'nonce': nonce,
            'data': tx_data['data']
        }

        signed_transaction = self.conn.eth.account.signTransaction(transaction, private_key)

        tx_hash = self.conn.eth.sendRawTransaction(signed_transaction.rawTransaction)

        return tx_hash

    def get_list_actor(self, type):
        result = self.contract.functions.get_list_actor(type).call()
        return result

    def get_address(self, type):
        result = self.contract.functions.map_address(type).call()
        return result

    def get_info_product(self, product_id):
        return self.contract.functions.seek_an_origin(product_id).call()

    def push_product_to_marketplace(self, id, product_id, owner, status, private_key):
        account = w3.eth.account.privateKeyToAccount(private_key)
        nonce = self.conn.eth.getTransactionCount(account.address)
        gas = 3000000
        gas_price = self.conn.eth.gasPrice

        function = self.contract.functions.listing_product(id, product_id, owner, status)

        tx_data = function.buildTransaction({'chainId': 97, 'gas': gas, 'gasPrice': gas_price, 'nonce': nonce})

        # Tạo một đối tượng giao dịch
        transaction = {
            'to': settings.WEB3_FACTORY_ADDRESS,
            'value': 0,  # Số Ether bạn muốn chuyển đi (0 trong trường hợp này)
            'gas': gas,
            'gasPrice': gas_price,
            'nonce': nonce,
            'data': tx_data['data']
        }

        signed_transaction = self.conn.eth.account.signTransaction(transaction, private_key)

        tx_hash = self.conn.eth.sendRawTransaction(signed_transaction.rawTransaction)

        return tx_hash

    def buy_product_in_market(self, id, quantity, buyer, id_trans, private_key):
        account = w3.eth.account.privateKeyToAccount(private_key)
        nonce = self.conn.eth.getTransactionCount(account.address)
        gas = 3000000
        gas_price = self.conn.eth.gasPrice

        function = self.contract.functions.buy_product_in_market(id, quantity, buyer, id_trans)

        tx_data = function.buildTransaction({'chainId': 97, 'gas': gas, 'gasPrice': gas_price, 'nonce': nonce})

        # Tạo một đối tượng giao dịch
        transaction = {
            'to': settings.WEB3_FACTORY_ADDRESS,
            'value': 0,  # Số Ether bạn muốn chuyển đi (0 trong trường hợp này)
            'gas': gas,
            'gasPrice': gas_price,
            'nonce': nonce,
            'data': tx_data['data']
        }

        signed_transaction = self.conn.eth.account.signTransaction(transaction, private_key)

        tx_hash = self.conn.eth.sendRawTransaction(signed_transaction.rawTransaction)

        return tx_hash

    def update_grow_up_detail_product(self, id: str, url: str, private_key):
        account = w3.eth.account.privateKeyToAccount(private_key)
        nonce = self.conn.eth.getTransactionCount(account.address)
        gas = 3000000
        gas_price = self.conn.eth.gasPrice

        function = self.contract.functions.update_grow_up_detail_product(id, url)

        tx_data = function.buildTransaction({'chainId': 97, 'gas': gas, 'gasPrice': gas_price, 'nonce': nonce})

        # Tạo một đối tượng giao dịch
        transaction = {
            'to': settings.WEB3_FACTORY_ADDRESS,
            'value': 0,  # Số Ether bạn muốn chuyển đi (0 trong trường hợp này)
            'gas': gas,
            'gasPrice': gas_price,
            'nonce': nonce,
            'data': tx_data['data']
        }

        signed_transaction = self.conn.eth.account.signTransaction(transaction, private_key)

        tx_hash = self.conn.eth.sendRawTransaction(signed_transaction.rawTransaction)

        return tx_hash

    def get_grow_up_product(self, id):
        return self.contract.functions.get_grow_up_product(id).call()
