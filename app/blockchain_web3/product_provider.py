import json

from web3.auto import w3

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
        return self.sign_and_send_transaction(function)

    def update_product(self, product_id, product_type, price, quantity, hash_info):

        function = self.contract.functions.update(product_id, product_type, price, quantity, hash_info)
        return self.sign_and_send_transaction(function)

    def get_product_by_id(self, product_id):
        return self.contract.functions.readOneProduct(product_id).call()

    def update_grow_up_product(self, product_id, url_image):
        function = self.contract.functions.updateGrowUpProduct(product_id, url_image)
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
