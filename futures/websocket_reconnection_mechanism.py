import time
import logging
from binance.lib.utils import config_logging
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient

config_logging(logging, logging.DEBUG)


def message_handler(message):
    if "e" in message and message["e"] == "continuous_kline" and message["k"]["x"]:
        data = message["k"]
        momentum_strategy.on_kline_update(data)


def start_websocket_client():
    ws_client = UMFuturesWebsocketClient()
    ws_client.start()
    ws_client.continuous_kline(
        pair=symbol,
        contractType="PERPETUAL",
        interval=interval,
        callback=message_handler,
    )
    return ws_client


def maintain_websocket_connection():
    while True:
        try:
            ws_client = start_websocket_client()
            time.sleep(60 * 60)  # Run for an hour before restarting
            logging.debug("Closing WebSocket connection and restarting")
            ws_client.stop()
        except Exception as e:
            logging.error("Error in WebSocket connection: %s", e)
            time.sleep(10)  # Wait 10 seconds before reconnecting


if __name__ == "__main__":
    symbol = "btcusdt"
    interval = "1m"

    # momentum_strategy = MomentumStrategy(symbol, interval, um_futures_client)

    maintain_websocket_connection()
