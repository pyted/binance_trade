from binance_trade.binance_cm.account import AccountCM
from binance_trade.binance_cm.market import MarketCM
from binance_trade.binance_cm.trade import TradeCM


class BinanceCM():
    def __init__(self, key: str, secret: str, timezone: str = 'America/New_York', proxies={}, proxy_host: str = None):
        self.account = AccountCM(key=key, secret=secret, proxies=proxies, proxy_host=proxy_host)
        self.market = MarketCM(key=key, secret=secret, timezone=timezone, proxies=proxies, proxy_host=proxy_host)
        self.trade = TradeCM(key=key, secret=secret, timezone=timezone, account=self.account, market=self.market,
                             proxies=proxies, proxy_host=proxy_host)
