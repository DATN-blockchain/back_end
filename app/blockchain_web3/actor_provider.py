import json

from app.blockchain_web3.provider import Web3Provider
from app.blockchain_web3.router import SupplyChainRouterProvider
from app.core.settings import settings


class ActorProvider(Web3Provider):

    def __init__(self, type_actor):
        with open('./app/abi/actor.txt', 'r', encoding='utf-8') as f:
            abi = f.read()

        factory_abi = json.loads(abi)
        super().__init__(settings.WEB3_PROVIDER)
        service = SupplyChainRouterProvider()
        self.contract = self.conn.eth.contract(address=service.get_address(type_actor), abi=factory_abi)

    def get_actor_by_id(self, id):
        return self.contract.functions.get_Actor_by_id(id).call()

    def get_list_actor(self):
        return self.contract.functions.get_list_Actor().call()
