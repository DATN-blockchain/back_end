from app.blockchain_web3.router import SupplyChainRouterProvider


class BlockchainService:

    @staticmethod
    def create_product(product_id, product_type, price, quantity, transaction_id, status, owner, private_key):
        route = SupplyChainRouterProvider()
        try:
            route.create_product(product_id, product_type, price, quantity, transaction_id, status, owner, private_key)
        except Exception as err:
            pass