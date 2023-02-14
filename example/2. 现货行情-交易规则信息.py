from binance_trade import BinanceSPOT
from pprint import pprint

if __name__ == '__main__':
    key = '****'
    secret = '****'
    binanceSPOT = BinanceSPOT(key=key, secret=secret)

    # 获取全部交易规则与交易对
    exchangeInfos = binanceSPOT.market.get_exchangeInfos()
    pprint(exchangeInfos)

    # 获取单个交易规则与交易对
    exchangeInfo = binanceSPOT.market.get_exchangeInfo(symbol='BTCUSDT')
    pprint(exchangeInfo)

    # 获取可以交易的产品列表
    symbols_trading_on = binanceSPOT.market.get_symbols_trading_on()
    pprint(symbols_trading_on)

    # 获取不可交易的产品列表
    get_symbols_trading_off = binanceSPOT.market.get_symbols_trading_off()
    pprint(get_symbols_trading_off)

