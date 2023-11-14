import re
from time import sleep

from web3 import Web3
from web3.auto import w3
from web3.middleware import geth_poa_middleware

from app.core.settings import settings


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

    @staticmethod
    def wait_for_transaction_confirmation(conn, tx_hash):
        while True:
            try:
                receipt = conn.eth.getTransactionReceipt(tx_hash)
                if receipt is not None:
                    print("Transaction confirmed in block", receipt['blockNumber'])
                    break
            except Exception as e:
                print("Error checking transaction receipt:", e)

            sleep(1)

    @staticmethod
    def sign_and_send_transaction(conn, func):
        account = w3.eth.account.privateKeyToAccount(settings.PRIVATE_KEY_SYSTEM)
        nonce = conn.eth.getTransactionCount(account.address)
        gas = 3000000
        gas_price = conn.eth.gasPrice

        tx_data = func.buildTransaction(
            {'chainId': settings.CHAIN_ID, 'gas': gas, 'gasPrice': gas_price, 'nonce': nonce})

        # Tạo một đối tượng giao dịch
        transaction = {
            'to': settings.WEB3_FACTORY_ADDRESS,
            'value': 0,  # Số Ether bạn muốn chuyển đi (0 trong trường hợp này)
            'gas': gas,
            'gasPrice': gas_price,
            'nonce': nonce,
            'data': tx_data['data']
        }

        signed_transaction = conn.eth.account.signTransaction(transaction, settings.PRIVATE_KEY_SYSTEM)

        tx_hash = conn.eth.sendRawTransaction(signed_transaction.rawTransaction)

        return tx_hash
