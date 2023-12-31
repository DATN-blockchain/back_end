import json
import os.path
import uuid

from app.blockchain_web3.provider import Web3Provider
from app.core.settings import settings


class ActorProvider(Web3Provider):

    def __init__(self):
        path_abi = os.path.join(os.getcwd(), "app/abi/actor.txt")
        with open(path_abi, 'r', encoding='utf-8') as f:
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

    def deposited(self, user_id: str, amount: int):
        function = self.contract.functions.deposited(user_id, amount)
        return self.sign_and_send_transaction(function)

    def withdraw(self, user_id: str, amount: int):
        function = self.contract.functions.withdraw_balance(user_id, amount)
        return self.sign_and_send_transaction(function)


if __name__ == "__main__":
    # actor_provider = ActorProvider().get_actor_by_id("e1bd3c7b-07b6-407b-afa3-041edf3bfe91")
    # print(actor_provider)
    # ActorProvider().deposited(user_id="68e144e4-9667-4187-98d3-2738c8a2927e", amount=100000)
    actor_provider = ActorProvider().get_actor_by_id("60b96988-dcb0-4afc-8f6d-a65f99a06995")
    # actor_provider = ActorProvider()
    print(actor_provider)
    # id = uuid.uuid4().__str__()
    # tx_hash = actor_provider.create_actor(user_id=id,
    #                                       address='0xe75DB3f37A05858507D469f896A4A982F7E1C302', role=0,
    #                                       hash_info="eyduYW1lJzogTm9uZSwgJ2F2YXRhcic6IE5vbmUsICdwaG9uZSc6IE5vbmUsICdhZGRyZXNzX3JlYWwnOiBOb25lfQ")
    # actor_provider = ActorProvider().get_actor_by_id(id)
    # print(actor_provider)
