from binance_trade.binance_um.account import AccountUM
from binance_trade.binance_um.market import MarketUM
from pbinance import UM


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
            self._account = AccountUM(key=key, secret=secret)
        else:
            self._account = account

        if not market:
            self._market = MarketUM(key=key, secret=secret, timezone=timezone)
        else:
            self._market = market
        self.timezone = timezone
        self.inst = UM(key=key, secret=secret)

