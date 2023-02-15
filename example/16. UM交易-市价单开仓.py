from binance_trade import BinanceUM
from pprint import pprint


# 成功触发的回调函数
def callback(information):
    '''
    :param information: 交易过程信息字典
        information = {
            'status': <订单状态（取消订单之前的）>,
            'meta': <传递过来的参数>,
            'request_param': <发送下单请求的具体参数>,
            'func_param': <open_market中的参数>,
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
            'func_param': <open_market中的参数>,
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
    binanceUM = BinanceUM(key=key, secret=secret)

    symbol = 'xxxx'  # 测试产品 可以选择：BATUSDT
    buyMoney = 15  # 购买金额

    # 市价单开仓
    binanceUM.trade.open_market(
        symbol=symbol,  # 产品
        marginType='ISOLATED',  # 保证金模式： ISOLATED: 逐仓 CROSSED: 全仓
        positionSide='LONG',  # 持仓方向 LONG: 多单 SHORT: 空单
        buyMoney=buyMoney,  # 开仓金额 开仓金额buyMoney和开仓数量quantity必须输入其中一个
        leverage=1,  # 开仓杠杆
        quantity=None,  # 开仓数量 None：用buyMoney计算可以购买的最大数量
        timeout=10,  # 等待订单成功的超时时间
        delay=0.2,  # 间隔多少秒检测订单是否成功
        cancel=True,  # 订单超时后是否取消
        callback=callback,  # 开仓成功触发的回调函数
        errorback=errorback,  # 开仓失败触发的回调函数
        newThread=False,  # 是否开启一个新的线程维护这个订单
        newClientOrderId='',  # 客户自定义订单ID
        meta={},  # 向回调函数中传递的参数字典
    )
