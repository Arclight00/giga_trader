import time

import certifi
import os
import logging

from binance.lib.utils import config_logging
from binance.um_futures import UMFutures
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient

from config.config import Config

from futures import MomentumStrategy
from futures.examples import BinanceFuturesBot

os.environ['SSL_CERT_FILE'] = certifi.where()
config_logging(logging, logging.DEBUG)

cfg = Config()

symbol = "btcusdt"
# symbol = "bnbusdt"
interval = "1m"

um_futures_client = UMFutures(key=cfg.binance_api_key, secret=cfg.binance_secret_key, base_url=cfg.base_url)

# momentum_strategy = MomentumStrategy(symbol, interval, um_futures_client)
bot = BinanceFuturesBot(um_futures_client, symbol)


def message_handler(message):
    if "e" in message and message['e'] == "continuous_kline" and message['k']['x']:
        data = message['k']
        print(data)
        bot.on_kline_update(data)


ws_client = UMFuturesWebsocketClient(stream_url=cfg.future_stream_uri)
ws_client.start()

ws_client.continuous_kline(
    pair=symbol,
    id=1,
    contractType="perpetual",
    interval="1m",
    callback=message_handler,
)
time.sleep(60*60)
logging.debug("closing ws connection")
ws_client.stop()
