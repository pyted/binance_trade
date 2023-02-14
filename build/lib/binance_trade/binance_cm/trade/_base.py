from binance_trade.binance_cm.account import AccountCM
from binance_trade.binance_cm.market import MarketCM
from pbinance import CM


class TradeBase():
    def __init__(
            self,
            key: str,
            secret: str,
            timezone: str = 'America/New_York',
            account=None,
            market=None
    ):
        if not account:
            self._account = AccountCM(key=key, secret=secret)
        else:
            self._account = account

        if not market:
            self._market = MarketCM(key=key, secret=secret, timezone=timezone)
        else:
            self._market = market
        self.timezone = timezone
        self.inst = CM(key=key, secret=secret)

