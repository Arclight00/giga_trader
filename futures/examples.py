import logging


class BinanceFuturesBot:

    def __init__(self, client, symbol):
        self.client = client
        self.symbol = symbol
        self.previous_momentum = 0
        self.set_leverage(10)
        # self.set_margin_type("ISOLATED")

    def get_position_risk(self):
        return self.client.get_position_risk(symbol=self.symbol)

    def set_leverage(self, leverage):
        self.client.change_leverage(symbol=self.symbol, leverage=leverage)

    def set_margin_type(self, margin_type):
        self.client.change_margin_type(symbol=self.symbol, marginType=margin_type)

    def calculate_momentum(self, kline):
        close_price = float(kline["c"])
        open_price = float(kline["o"])
        return close_price - open_price

    def on_kline_update(self, kline):
        momentum = self.calculate_momentum(kline)
        logging.info("Momentum: %s", momentum)

        if momentum > self.previous_momentum:
            # Place buy order (example)
            self.place_order("BUY", quantity=0.03)
        elif momentum < self.previous_momentum:
            # Place sell order (example)
            self.place_order("SELL", quantity=0.03)

        self.previous_momentum = momentum

    def place_order(self, side, quantity):
        position = self.get_position_risk()
        try:
            # Ensure only one position is active for the symbol
            if float(position[0]["positionAmt"]) != 0:
                return
            entry_order = self.client.new_order(
                symbol=self.symbol,
                side=side,
                positionSide="BOTH",
                type="MARKET",
                quantity=quantity,
                reduceOnly=False
            )
            logging.info("Entry order placed: %s", entry_order)
            position = self.get_position_risk()
            entry_price = float(position[0]["entryPrice"])
            stop_loss_percentage = 0.004
            take_profit_percentage = 0.002

            stop_price = round(float(entry_price * (1 - stop_loss_percentage)), 2)
            take_profit_price = round(float(entry_price * (1 + take_profit_percentage)), 2)

            stop_loss_order = self.client.new_order(
                symbol=self.symbol,
                side="SELL",
                positionSide="BOTH",
                type="STOP_MARKET",
                timeInForce="GTC",
                quantity=quantity,
                stopPrice=stop_price,
                closePosition=True
            )
            logging.info("Stop-loss order placed: %s", stop_loss_order)
            take_profit_order = self.client.new_order(
                symbol=self.symbol,
                side="SELL",
                positionSide="BOTH",
                type="TAKE_PROFIT_MARKET",
                timeInForce="GTC",
                quantity=quantity,
                stopPrice=take_profit_price,
                closePosition=True
            )
            logging.info("Take-profit order placed: %s", take_profit_order)

        except Exception as e:
            logging.error("Error placing order: %s", e)