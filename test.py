import json
import re
import logging
import uuid

from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.auto import w3
# from eth_account import messages, Account

contract_address = '0x415B78B5Ba2bB2488bFd42C127a1D9A372968347'
provider_url = 'https://ethereum-sepolia.blockpi.network/v1/rpc/public'
private_key = "24045d471ee28f805d1058b6a68307d2faa71fa7b9ff5f9441c1d67259d151c4"
logger = logging.getLogger(__name__)
account = w3.eth.account.privateKeyToAccount(private_key)
my_address = account.address


# w3.middleware_onion.inject(geth_poa_middleware, layer=0)
class Web3Provider(object):

    def __init__(self, provider=None):

        self.provider = provider
        if re.match(r'^https*:', self.provider):
            provider = Web3.HTTPProvider(self.provider, request_kwargs={"timeout": 60})
        elif re.match(r'^ws*:', self.provider):
            provider = Web3.WebsocketProvider(self.provider)
        elif re.match(r'^/', self.provider):
            provider = Web3.IPCProvider(self.provider)
        else:
            raise RuntimeError("Unknown provider type " + self.provider)

        self.conn = Web3(provider)
        self.conn.middleware_onion.inject(geth_poa_middleware, layer=0)

        if not self.conn.isConnected():
            raise RuntimeError("Unable to connect to provider at " + self.provider)


class RouterFactoryContract(Web3Provider):

    def __init__(self):
        with open('./app/abi/supply_chain.txt', 'r', encoding='utf-8') as f:
            abi = f.read()

        factory_abi = json.loads(abi)
        super().__init__(provider_url)
        self.contract = self.conn.eth.contract(address=contract_address, abi=factory_abi)

    def create_actor(self, id, address, type):
        nonce = self.conn.eth.getTransactionCount(address)
        gas = 500000
        gas_price = self.conn.eth.gas_price

        function = self.contract.functions.create_actor(id, address, type)
        tx_data = function.buildTransaction({'chainId': 11155111, 'gas': gas, 'gasPrice': gas_price, 'nonce': nonce})

        # Tạo một đối tượng giao dịch
        transaction = {
            'to': contract_address,
            'value': 0,  # Số Ether bạn muốn chuyển đi (0 trong trường hợp này)
            'gas': gas,
            'gasPrice': gas_price,
            'nonce': nonce,
            'data': tx_data['data'],
            'chainId': 11155111
        }

        signed_transaction = self.conn.eth.account.signTransaction(transaction, private_key)

        tx_hash = self.conn.eth.sendRawTransaction(signed_transaction.rawTransaction)

        return tx_hash

    def create_product(self, product_id, product_type, price, quantity, transaction_id, status, owner):
        nonce = self.conn.eth.getTransactionCount(account.address)
        gas = 250000
        # gas_price = self.conn.toWei('35', 'gwei')
        gas_price = self.conn.eth.gas_price

        function = self.contract.functions.create_product(product_id, product_type, price, quantity, transaction_id,
                                                          status, owner)

        tx_data = function.buildTransaction({'chainId': 97, 'gas': gas, 'gasPrice': gas_price, 'nonce': nonce})

        # Tạo một đối tượng giao dịch
        transaction = {
            'to': contract_address,
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


class FarmerProvider(Web3Provider):

    def __init__(self):
        with open('./app/abi/actor.txt', 'r', encoding='utf-8') as f:
            abi = f.read()

        factory_abi = json.loads(abi)
        super().__init__(provider_url)
        service = RouterFactoryContract()
        self.contract = self.conn.eth.contract(address=service.get_address("seedCompany"), abi=factory_abi)

    def get_actor_by_id(self, id):
        return self.contract.functions.get_Actor_by_id(id).call()


service = RouterFactoryContract()
# result = service.create_actor(str(uuid.uuid4()), my_address, 0)
# # # # # # # # print (service.create_product("p1", 1, 200, 200, "", 0, "a1"))
# print(result.hex())

print(service.get_list_actor(0))
# print(service.get_address("farmer"))
# # result = service.create_product("p1", 1, 200, 100, "", 0, "a1")
# # print(result.hex())
#
# print(service.get_info_product("p1"))
#
#
# service_SC = FarmerProvider()
# print(service_SC.get_actor_by_id("a1"))

#
# from web3 import Web3
#
# from eth_account import Account
#
# # Connect to the BNB testnet
# w3 = Web3(Web3.HTTPProvider('https://data-seed-prebsc-1-s1.binance.org:8545'))
#
# # Generate a new account
# # account = Account.create()
# # private_key = account.privateKey
# # address = account.address
#
# # Get the account balance
# balance = w3.eth.getBalance("0x179004f7bd51C2B1b63ADf9F340E273a8EBa77E0")
# # print(f"Address: {address}")
# print(f"Balance: {balance}")
#
# # Create the account wallet file
# # with open(f"{address}_private_key.txt", "w") as f:
# #     f.write(private_key.hex())
#
# print("BNB testnet account wallet created!")