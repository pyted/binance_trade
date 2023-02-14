from binance_trade import BinanceUM
from pprint import pprint

if __name__ == '__main__':
    key = '****'
    secret = '****'
    binanceUM = BinanceUM(key=key, secret=secret)

    # 普通下单购买
    set_order = binanceUM.trade.set_order(
        symbol='xxx',
        side='BUY',
        type='LIMIT',
        timeInForce='GTC',
        quantity='xxx',
        price='xxx',
    )
    pprint(set_order)

    # 查询订单
    order = binanceUM.trade.get_order(
        symbol='xxx',
        orderId='xxx'
    )
    pprint(order)

    # 查看全部当前全部挂单
    openOrders = binanceUM.trade.get_openOrders()
    pprint(openOrders)

    # 查询单个产品当前挂单
    openOrder = binanceUM.trade.get_openOrder(symbol='xxx')
    pprint(openOrder)

    # 撤销订单
    binanceUM.trade.cancel_order(
        symbol='xxx',
        orderId='xxx',
    )

    # 等待订单成交
    binanceUM.trade.wait_order_FILLED(
        symbol='xxx',
        orderId='xxx',
    )
