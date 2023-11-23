import json
import os.path
import uuid

from app.blockchain_web3.provider import Web3Provider
from app.core.settings import settings


class ActorProvider(Web3Provider):

    def __init__(self):
        path_abi = os.path.join(os.getcwd(), "app/abi/actor.txt")
        with open("../abi/actor.txt", 'r', encoding='utf-8') as f:
            abi = f.read()

        factory_abi = json.loads(abi)
        super().__init__(settings.WEB3_PROVIDER, settings.ADDRESS_CONTRACT_ACTOR_MANAGER)
        self.chain_id = settings.CHAIN_ID
        self.contract = self.w3.eth.contract(address=settings.ADDRESS_CONTRACT_ACTOR_MANAGER, abi=factory_abi)

    def create_actor(self, user_id: str, address, role, hash_info):
        # breakpoint()
        function = self.contract.functions.create(user_id, address, role, hash_info)
        return self.sign_and_send_transaction(function)

    def update_actor(self, user_id: str, hash_info: str):
        function = self.contract.functions.update_actor_hash_info(user_id, hash_info)

        return self.sign_and_send_transaction(function)

    def get_actor_by_id(self, user_id):
        return self.contract.functions.get_Actor_by_id(user_id).call()

    def get_ids_by_role(self, role):
        return self.contract.functions.get_ids_by_role(role).call()


if __name__ == "__main__":
    actor_provider = ActorProvider()
    tx_hash = actor_provider.create_actor(user_id=uuid.uuid4().__str__(),
                                          address='0xe75DB3f37A05858507D469f896A4A982F7E1C302', role=0,
                                          hash_info="eyduYW1lJzogTm9uZSwgJ2F2YXRhcic6IE5vbmUsICdwaG9uZSc6IE5vbmUsICdhZGRyZXNzX3JlYWwnOiBOb25lfQ")
