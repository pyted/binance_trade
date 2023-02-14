from binance_trade import BinanceUM
from pprint import pprint

if __name__ == '__main__':
    key = '****'
    secret = '****'
    binanceUM = BinanceUM(key=key, secret=secret)

    # 获取账户信息
    account = binanceUM.account.get_account()
    pprint(account)

    # 获取账户全部余额
    balances = binanceUM.account.get_balances()
    pprint(balances)

    # 获取账户单个货币余额
    balance = binanceUM.account.get_balance(asset='BTC')
    pprint(balance)

    # 调整开仓杠杆
    leverage = binanceUM.account.set_leverage(symbol='BTCUSDT', leverage=1)
    pprint(leverage)

    # 更改持仓模式
    marginType = binanceUM.account.set_marginType(symbol='BTCUSDT', marginType='ISOLATED')
    pprint(marginType)

    # 获取全部产品的持仓信息
    positions = binanceUM.account.get_positions()
    pprint(positions)

    # 获取单个产品的持仓信息
    position = binanceUM.account.get_position(symbol='BTCUSDT')
    pprint(position)