from binance_trade import BinanceUM
from pprint import pprint

if __name__ == '__main__':
    key = '****'
    secret = '****'
    binanceUM = BinanceUM(key=key, secret=secret)

    # 获取全部交易规则与交易对
    exchangeInfos = binanceUM.market.get_exchangeInfos()
    pprint(exchangeInfos)

    # 获取单个交易规则与交易对
    exchangeInfo = binanceUM.market.get_exchangeInfo(symbol='BTCUSDT')
    pprint(exchangeInfo)

    # 获取可以交易的产品列表
    symbols_trading_on = binanceUM.market.get_symbols_trading_on()
    pprint(symbols_trading_on)

    # 获取不可交易的产品列表
    get_symbols_trading_off = binanceUM.market.get_symbols_trading_off()
    pprint(get_symbols_trading_off)

