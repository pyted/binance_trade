from binance_trade import BinanceUM
from pprint import pprint

if __name__ == '__main__':
    key = '****'
    secret = '****'
    binanceUM = BinanceUM(key=key, secret=secret)
    
    # 获取产品的历史K线数据
    history_candle = binanceUM.market.get_history_candle(
        symbol='BTCUSDT',
        start='2023-01-01 00:00:00',
        end='2023-01-01 23:59:00',
        bar='1m',
    )
    pprint(history_candle)

    # 获取产品指定数量的最新历史K线数据
    history_candle_latest = binanceUM.market.get_history_candle_latest(
        symbol='BTCUSDT',
        length=1440,
        bar='1m',
    )
    pprint(history_candle_latest)

    # 获取产品指定日期的历史K线数据
    history_candle_by_date = binanceUM.market.get_history_candle_by_date(
        symbol='BTCUSDT',
        date='2023-01-01',
        bar='1m',
    )
    pprint(history_candle_by_date)
