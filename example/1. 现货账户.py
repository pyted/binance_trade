from binance_trade import BinanceSPOT
from pprint import pprint

if __name__ == '__main__':
    key = '****'
    secret = '****'
    binanceSPOT = BinanceSPOT(key=key, secret=secret)

    # 获取账户信息
    account = binanceSPOT.account.get_account()
    pprint(account)
    # 获取全部现货余额
    balances = binanceSPOT.account.get_balances()
    pprint(balances)
    # 获取单个现货余额
    balance = binanceSPOT.account.get_balance(
        symbol='BTCUSDT',
        base_asset='USDT'
    )  # 等价于： # balances = binanceSPOT.account.get_balance(asset='BTC')
    pprint(balance)
