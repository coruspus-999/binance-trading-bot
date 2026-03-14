import logging
from binance.exceptions import BinanceAPIException

class OrderManager:
    """
    Handles the execution of futures orders on the Binance Testnet.
    Separates API logic from the CLI layer for reusability.
    """
    def __init__(self, client):
        self.client = client
        self.logger = logging.getLogger("OrderManager")

    def execute_order(self, symbol, side, order_type, quantity, price=None):
        try:
            # Construct base parameters
            params = {
                "symbol": symbol.upper(),
                "side": side.upper(),
                "type": order_type.upper(),
                "quantity": quantity,
            }

            # Add limit-specific parameters
            if order_type.upper() == "LIMIT":
                params["price"] = str(price)
                params["timeInForce"] = "GTC"  # Good Till Cancelled

            self.logger.info(f"Sending Order Request: {params}")

            # Execute via python-binance client
            response = self.client.futures_create_order(**params)
            
            self.logger.info(f"Received Order Response: {response}")
            return response

        except BinanceAPIException as e:
            error_msg = f"Binance API Error: Code {e.code} - {e.message}"
            self.logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Unexpected Error during order execution: {str(e)}"
            self.logger.error(error_msg)
            raise Exception(error_msg)