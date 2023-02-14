from binance_trade import BinanceUM
from pprint import pprint

if __name__ == '__main__':
    key = '****'
    secret = '****'
    binanceUM = BinanceUM(key=key, secret=secret)

    # 获取全部产品的最优挂单
    bookTickersMap = binanceUM.market.get_bookTickersMap()
    pprint(bookTickersMap)
    bookTickers = binanceUM.market.get_bookTickers()
    pprint(bookTickers)

    # 获取单个产品的最优挂单
    bookTicker = binanceUM.market.get_bookTicker(symbol='BTCUSDT')
    pprint(bookTicker)

    # 获取全部产品的最新价格
    tickerPricesMap = binanceUM.market.get_tickerPricesMap()
    pprint(tickerPricesMap)
    tickerPrices = binanceUM.market.get_tickerPrices()
    pprint(tickerPrices)

    # 获取单个产品的最新价格
    tickerPrice = binanceUM.market.get_tickerPrice(symbol='BTCUSDT')
    pprint(tickerPrice)

    # 获取单个产品的深度交易
    depth = binanceUM.market.get_depth(symbol='BTCUSDT', limit=100)
    pprint(depth)
