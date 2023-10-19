from binance_trade.binance_spot.account import AccountSPOT
from binance_trade.binance_spot.market import MarketSPOT
from binance_trade.binance_spot.trade import TradeSPOT


class BinanceSPOT():
    def __init__(self, key: str, secret: str, timezone: str = 'America/New_York', proxies={}, proxy_host: str = None):
        self.account = AccountSPOT(key=key, secret=secret, proxies=proxies, proxy_host=proxy_host)
        self.market = MarketSPOT(key=key, secret=secret, timezone=timezone, proxies=proxies, proxy_host=proxy_host)
        self.trade = TradeSPOT(key=key, secret=secret, timezone=timezone, account=self.account, market=self.market,
                               proxies=proxies, proxy_host=proxy_host)
