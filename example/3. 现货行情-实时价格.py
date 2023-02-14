from binance_trade import BinanceSPOT
from pprint import pprint

if __name__ == '__main__':
    key = '****'
    secret = '****'
    binanceSPOT = BinanceSPOT(key=key, secret=secret)

    # 获取全部产品的最优挂单
    bookTickersMap = binanceSPOT.market.get_bookTickersMap()
    pprint(bookTickersMap)
    bookTickers = binanceSPOT.market.get_bookTickers()
    pprint(bookTickers)

    # 获取单个产品的最优挂单
    bookTicker = binanceSPOT.market.get_bookTicker(symbol='BTCUSDT')
    pprint(bookTicker)

    # 获取全部产品的最新价格
    tickerPricesMap = binanceSPOT.market.get_tickerPricesMap()
    pprint(tickerPricesMap)
    tickerPrices = binanceSPOT.market.get_tickerPrices()
    pprint(tickerPrices)

    # 获取单个产品的最新价格
    tickerPrice = binanceSPOT.market.get_tickerPrice(symbol='BTCUSDT')
    pprint(tickerPrice)

    # 获取单个产品的深度交易
    depth = binanceSPOT.market.get_depth(symbol='BTCUSDT', limit=100)
    pprint(depth)