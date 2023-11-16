import json

from app.blockchain_web3.provider import Web3Provider
from app.core.settings import settings


class ActorProvider(Web3Provider):

    def __init__(self):
        with open('./app/abi/actor.txt', 'r', encoding='utf-8') as f:
            abi = f.read()

        factory_abi = json.loads(abi)
        super().__init__(settings.WEB3_PROVIDER, settings.ADDRESS_CONTRACT_ACTOR_MANAGER)
        self.chain_id = settings.CHAIN_ID
        self.contract = self.w3.eth.contract(address=settings.ADDRESS_CONTRACT_ACTOR_MANAGER, abi=factory_abi)

    def create_actor(self, user_id: str, address, role):
        function = self.contract.functions.create(user_id, address, role)

        tx_hash = self.sign_and_send_transaction(function)
        return tx_hash

    def get_actor_by_id(self, user_id):
        return self.contract.functions.get_Actor_by_id(user_id).call()

    def get_ids_by_role(self, role):
        return self.contract.functions.get_ids_by_role(role).call()
