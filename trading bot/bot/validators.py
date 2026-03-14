import logging
import math

class OrderValidator:
    def __init__(self):
        self.logger = logging.getLogger("Validator")

    def round_step(self, value, step):
        """Rounds a value down to the nearest multiple of 'step'."""
        if not step:
            return value
        # Using Decimal-safe math to avoid floating point issues
        precision = int(round(-math.log10(step), 0))
        return round(math.floor(value / step) * step, precision)

    def clean_order_data(self, quantity, price, rules):
        """Automatically adjusts quantity and price to meet exchange rules."""
        cleaned_qty = self.round_step(quantity, rules['step_size'])
        
        cleaned_price = None
        if price:
            cleaned_price = self.round_step(price, rules['tick_size'])
            
        return cleaned_qty, cleaned_price

    def validate(self, symbol, side, order_type, quantity, price=None, rules=None):
        # Basic checks first
        if quantity <= 0:
            return False, "Quantity must be positive."
        
        if not rules:
            return True, None

        # Notional Check (Price * Quantity >= Min Notional)
        check_price = price if price else 0 
        if check_price > 0:
            notional = quantity * check_price
            if notional < rules['min_notional']:
                return False, f"Order too small: ${notional} < ${rules['min_notional']} min."

        return True, None