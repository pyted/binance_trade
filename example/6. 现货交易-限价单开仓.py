from binance_trade import BinanceSPOT
from pprint import pprint


# 成功触发的回调函数
def callback(information):
    '''
    :param information: 交易过程信息字典
        information = {
            'status': <订单状态（取消订单之前的）>,
            'meta': <传递过来的参数>,
            'request_param': <发送下单请求的具体参数>,
            'func_param': <open_limit中的参数>,
            'get_order_result': <获取订单状态的结果>,
            'set_order_result': <下单提交的结果>,
            'error_result': <异常信息>,
            'cancel_result': <取消订单的结果>,
        }
    '''
    print('callback')
    pprint(information)


# 失败触发的回调函数
def errorback(information):
    '''
    :param information: 交易过程信息字典
        information = {
            'status': <订单状态（取消订单之前的）>,
            'meta': <传递过来的参数>,
            'request_param': <发送下单请求的具体参数>,
            'func_param': <open_limit中的参数>,
            'get_order_result': <获取订单状态的结果>,
            'set_order_result': <下单提交的结果>,
            'error_result': <异常信息>,
            'cancel_result': <取消订单的结果>,
        }
    '''
    print('errorback')
    pprint(information)


if __name__ == '__main__':
    key = '****'
    secret = '****'
    binanceSPOT = BinanceSPOT(key=key, secret=secret)

    symbol = 'PHAUSDT'  # 测试产品
    buyMoney = 15  # 购买金额
    askPrice = binanceSPOT.market.get_bookTicker(symbol=symbol)['data']['askPrice']  # 卖1价格
    askPrice = float(askPrice)
    buyLine = askPrice * 0.8  # 购买价格为卖1价的8折，测试挂单

    # 限价单开仓
    binanceSPOT.trade.open_limit(
        symbol=symbol,  # 产品
        buyLine=buyLine,  # 开仓价格
        buyMoney=buyMoney,  # 开仓金额 开仓金额buyMoney和开仓数量quantity必须输入其中一个 优先级：quantity > buyMoney
        quantity=None,  # 开仓数量 None：用buyMoney计算可以购买的最大数量
        block=True,  # 是否以堵塞的模式
        timeout=10,  # 等待订单成功的超时时间
        delay=0.2,  # 间隔多少秒检测订单是否成功
        cancel=True,  # 订单超时后是否取消
        callback=callback,  # 开仓成功触发的回调函数
        errorback=errorback,  # 开仓失败触发的回调函数
        newThread=True,  # 是否开启一个新的线程维护这个订单
        newClientOrderId='',  # 客户自定义订单ID
        meta={},  # 向回调函数中传递的参数字典
    )
