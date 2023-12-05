import logging

from binance.lib.utils import config_logging
from config.config import Config

config_logging(logging, logging.DEBUG)

cfg = Config()


class MomentumStrategy:
    def __init__(self, symbol, interval, um_futures_client):
        self.symbol = symbol
        self.interval = interval
        self.um_futures_client = um_futures_client
        self.previous_momentum = 0

    def calculate_momentum(self, kline):
        close_price = float(kline["c"])
        open_price = float(kline["o"])
        momentum = close_price - open_price
        return momentum

    def on_kline_update(self, kline):
        momentum = self.calculate_momentum(kline)
        logging.info("Momentum: %s", momentum)

        if momentum > self.previous_momentum:
            # Place buy order (example)
            self.place_order("BUY", quantity=0.02)
        elif momentum < self.previous_momentum:
            # Place sell order (example)
            self.place_order("SELL", quantity=0.02)

        self.previous_momentum = momentum

    def place_order(self, side, quantity, stop_loss=0.001, take_profit=0.002):
        try:
            current_price = float(self.um_futures_client.ticker_price(symbol=self.symbol)["price"])
            new_order = self.um_futures_client.new_order(
                symbol=self.symbol,
                side="BUY",
                positionSide="BOTH",
                type="MARKET",
                reduceOnly=False,
                timeInForce="GTC",
                quantity=quantity,
            )
            logging.info("New order placed: %s", new_order)
            stop_price = current_price * (1 - stop_loss) if side == "SELL" else current_price * (1 + stop_loss)
            profit_price = current_price * (1 + take_profit) if side == "BUY" else current_price * (1 - take_profit)

            # Place stop-loss order
            stop_order = self.um_futures_client.new_order(
                symbol=self.symbol,
                side="SELL",
                type="STOP_MARKET",
                stopPrice=round(float(stop_price), 2),
                timeInForce="GTC",
                quantity=quantity,
            )
            logging.info("Stop-loss order placed: %s", stop_order)

            # Place take-profit order
            take_profit_order = self.um_futures_client.new_order(
                symbol=self.symbol,
                side="SELL",
                type="LIMIT",
                timeInForce="GTC",
                price=round(float(profit_price), 2),
                quantity=quantity,
            )
            logging.info("Take-profit order placed: %s", take_profit_order)

        except Exception as e:
            logging.error("Error placing order: %s", e)

