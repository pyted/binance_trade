from binance_trade.binance_cm.account import AccountCM
from binance_trade.binance_cm.market import MarketCM
from binance_trade.binance_cm.trade import TradeCM


class BinanceCM():
    def __init__(self, key: str, secret: str, timezone: str = 'America/New_York'):
        self.account = AccountCM(key=key, secret=secret)
        self.market = MarketCM(key=key, secret=secret, timezone=timezone)
        self.trade = TradeCM(key=key, secret=secret, timezone=timezone, account=self.account, market=self.market)
