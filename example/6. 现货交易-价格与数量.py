from pprint import pprint
from binance_trade import BinanceSPOT

if __name__ == '__main__':
    key = '****'
    secret = '****'
    binanceSPOT = BinanceSPOT(key=key, secret=secret)

    # 圆整下单数量
    round_quantity_result = binanceSPOT.trade.round_quantity(
        quantity=100.00023234234234,
        symbol='MANAUSDT',
    )
    pprint(round_quantity_result)
    # 圆整下单价格
    round_price_result = binanceSPOT.trade.round_price(
        price=20.123123123,
        symbol='MANAUSDT',
        type='FLOOR',  # FLOOR:向下圆整 CEIL:向上圆整
    )
    pprint(round_price_result)
    # 根据开仓金额、开仓价格与杠杆计算最大可开仓数量
    get_quantity_result = binanceSPOT.trade.get_quantity(
        openPrice=2.123123,
        openMoney=20,
        symbol='MANAUSDT',
        leverage=1
    )
    pprint(get_quantity_result)
    # 将下单数量转化为字符串
    quantity_to_f_result = binanceSPOT.trade.quantity_to_f(
        quantity=get_quantity_result['data'],
        symbol='MANAUSDT',
    )
    pprint(quantity_to_f_result)
    # 将下单价格转化为字符串
    price_to_f_result = binanceSPOT.trade.price_to_f(
        price=round_price_result['data'],
        symbol='MANAUSDT',
    )
    pprint(price_to_f_result)