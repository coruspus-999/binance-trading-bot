import argparse
import os
from dotenv import load_dotenv
from bot.logging_cfg import setup_logging
from bot.client import BinanceTestnetClient
from bot.orders import OrderManager
from bot.validators import OrderValidator

# Load environment variables from .env file
load_dotenv()

def main():
    setup_logging()
    
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Bot")
    parser.add_argument("--symbol", required=True, help="e.g. BTCUSDT")
    parser.add_argument("--side", choices=["BUY", "SELL"], required=True)
    parser.add_argument("--type", choices=["MARKET", "LIMIT"], required=True)
    parser.add_argument("--qty", type=float, required=True)
    parser.add_argument("--price", type=float, help="Required for LIMIT")

    args = parser.parse_args()

    validator = OrderValidator()
    is_valid, error_msg = validator.validate(args.symbol, args.side, args.type, args.qty, args.price)
    
    if not is_valid:
        print(f"\n Validation Error: {error_msg}")
        return

    
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    # Double check keys were actually loaded
    if not api_key or not api_secret:
        print("\n Configuration Error: API Keys not found in .env file.")
        return

    try:
        print(f"\n Sending {args.type} {args.side} order for {args.symbol}...")
        
        client_wrapper = BinanceTestnetClient(api_key, api_secret)
        manager = OrderManager(client_wrapper.get_client())

        res = manager.execute_order(args.symbol, args.side, args.type, args.qty, args.price)
        
        print("\nORDER PLACED SUCCESSFULLY")
        print("-" * 40)
        print(f"Order ID      : {res.get('orderId')}")
        print(f"Symbol        : {res.get('symbol')}")
        print(f"Status        : {res.get('status')}")
        print(f"Side          : {res.get('side')}")
        print(f"Type          : {res.get('type')}")
        print(f"Original Qty  : {res.get('origQty')}")
        print(f"Executed Qty  : {res.get('executedQty')}")
        
        avg_price = res.get('avgPrice', '0')
        if float(avg_price) > 0:
            print(f"Average Price : {avg_price}")
        else:
            print(f"Limit Price   : {res.get('price', 'N/A')}")
        print("-" * 40)
    except Exception as e:
        print(f"\n API/Execution Failure: {e}")

if __name__ == "__main__":
    main()