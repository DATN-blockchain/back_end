import re
from time import sleep

from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account
from app.core.settings import settings


class Web3Provider(object):

    def __init__(self, provider=None, contract_address=None):
        if re.match(r'^https*:', provider):
            self.w3 = Web3(Web3.HTTPProvider(provider, request_kwargs={"timeout": 60}))
        elif re.match(r'^ws*:', provider):
            self.w3 = Web3(Web3.WebsocketProvider(provider))
        elif re.match(r'^/', provider):
            self.w3 = Web3(Web3.IPCProvider(provider))
        else:
            raise RuntimeError("Unknown provider type " + provider)
        self.contract_address = contract_address
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        if not self.w3.is_connected():
            raise RuntimeError("Unable to connect to provider at " + provider)

    def check_connection(self):
        return self.w3.is_connected()

    def get_transaction_count(self, address):
        return self.w3.eth.get_transaction_count(address)

    def sign_and_send_transaction(self, func):
        account = Account.from_key(settings.PRIVATE_KEY_SYSTEM)
        nonce = self.get_transaction_count(account.address)
        gas = 500000
        gas_price = self.w3.eth.gas_price

        tx_data = func.build_transaction({'chainId': int(settings.CHAIN_ID), 'gas': gas, 'gasPrice': gas_price})

        transaction = {
            'to': self.contract_address,
            'value': 0,
            'gas': gas,
            'gasPrice': gas_price,
            'nonce': nonce,
            'data': tx_data['data'],
            'chainId': int(settings.CHAIN_ID)
        }

        signed_transaction = self.w3.eth.account.sign_transaction(transaction, settings.PRIVATE_KEY_SYSTEM)
        tx_hash = self.w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

        while True:
            try:
                receipt = self.w3.eth.get_transaction_receipt(tx_hash)
                if receipt is not None:
                    print("Transaction confirmed in block", receipt['blockNumber'])
                    break
            except Exception as e:
                print("Error checking transaction receipt:", e)

            sleep(0.1)

        return tx_hash.hex()
