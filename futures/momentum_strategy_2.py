import logging

from binance.lib.utils import config_logging
from config.config import Config

config_logging(logging, logging.DEBUG)

cfg = Config()


class MomentumStrategy:

    def __init__(self, symbols, interval, min_momentum, amount):
        self.symbols = symbols
        self.interval = interval
        self.min_momentum = min_momentum
        self.amount = amount
        self.positions = {}

    def update_positions(self):
        account_info = self.client.futures_account()
        positions = account_info['positions']
        self.positions = {}
        for position in positions:
            symbol = position['symbol']
            position_side = position['positionSide']
            if position_side == "BOTH":
                continue
            if position_side not in self.positions:
                self.positions[position_side] = {}
            self.positions[position_side][symbol] = position