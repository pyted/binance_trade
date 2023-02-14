from binance_trade import BinanceSPOT
from pprint import pprint

if __name__ == '__main__':
    key = '****'
    secret = '****'
    binanceSPOT = BinanceSPOT(key=key, secret=secret)

    # 普通下单购买
    set_order = binanceSPOT.trade.set_order(
        symbol='xxx',
        side='BUY',
        type='LIMIT',
        timeInForce='GTC',
        quantity='xxx',
        price='xxx',
    )
    pprint(set_order)

    # 查询订单
    order = binanceSPOT.trade.get_order(
        symbol='xxx',
        orderId='xxx'
    )
    pprint(order)

    # 查看全部当前全部挂单
    openOrders = binanceSPOT.trade.get_openOrders()
    pprint(openOrders)

    # 查询单个产品当前挂单
    openOrder = binanceSPOT.trade.get_openOrder(symbol='xxx')
    pprint(openOrder)

    # 撤销订单
    binanceSPOT.trade.cancel_order(
        symbol='xxx',
        orderId='xxx',
    )

    # 等待订单成交
    binanceSPOT.trade.wait_order_FILLED(
        symbol='xxx',
        orderId='xxx',
    )
