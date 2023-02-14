from binance_trade.binance_um.account import AccountUM
from binance_trade.binance_um.market import MarketUM
from binance_trade.binance_um.trade import TradeUM


class BinanceUM():
    def __init__(self, key: str, secret: str, timezone: str = 'America/New_York'):
        self.account = AccountUM(key=key, secret=secret)
        self.market = MarketUM(key=key, secret=secret, timezone=timezone)
        self.trade = TradeUM(key=key, secret=secret, timezone=timezone, account=self.account, market=self.market)
