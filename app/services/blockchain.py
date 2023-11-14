from app.blockchain_web3.supply_chain_provider import SupplyChainRouterProvider


class BlockchainService:

    @staticmethod
    async def create_product(product_id, product_type, price, quantity, transaction_id, status, owner, private_key):
        route = SupplyChainRouterProvider()
        try:
            result = route.create_product(product_id, product_type, price, quantity, transaction_id, status, owner,
                                          private_key)
            return True
        except Exception as err:
            return False
