import json

from web3.auto import w3

from app.blockchain_web3.provider import Web3Provider
from app.core.settings import settings


class ActorProvider(Web3Provider):

    def __init__(self):
        with open('./app/abi/actor.txt', 'r', encoding='utf-8') as f:
            abi = f.read()

        factory_abi = json.loads(abi)
        super().__init__(settings.WEB3_PROVIDER)
        self.chain_id = settings.CHAIN_ID
        self.contract = self.conn.eth.contract(address=settings.ADDRESS_CONTRACT_ACTOR_MANAGER, abi=factory_abi)

    def create_actor(self, user_id: str, address, role):
        account = w3.eth.account.privateKeyToAccount(settings.PRIVATE_KEY_SYSTEM)
        nonce = self.conn.eth.getTransactionCount(account.address)
        gas = 3000000
        gas_price = self.conn.eth.gasPrice

        function = self.contract.functions.create(user_id, address, role)

        tx_data = function.buildTransaction(
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

    def get_actor_by_id(self, user_id):
        return self.contract.functions.get_Actor_by_id(user_id).call()

    def get_ids_by_role(self, role):
        return self.contract.functions.get_ids_by_role(role).call()
