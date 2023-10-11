import re
from web3 import Web3
from web3.middleware import geth_poa_middleware


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
