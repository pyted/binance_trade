from binance_trade.binance_spot.account import AccountSPOT
from binance_trade.binance_spot.market import MarketSPOT
from pbinance import SPOT


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
            self._account = AccountSPOT(key=key, secret=secret)
        else:
            self._account = account

        if not market:
            self._market = MarketSPOT(key=key, secret=secret, timezone=timezone)
        else:
            self._market = market
        self.timezone = timezone
        self.inst = SPOT(key=key, secret=secret)

