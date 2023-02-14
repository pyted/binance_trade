from typing import Union
import traceback
from threading import Thread
from paux.digit import origin_float, origin_int
from binance_trade import code
from binance_trade.binance_spot.trade.order import TradeOrder
from binance_trade.binance_spot.trade.quantity_and_price import TradeQuantityAndPrice


class TradeOpen(TradeOrder, TradeQuantityAndPrice):

    # 限价单购买 Weight > 1
    def open_limit(
            self,
            symbol: str,
            buyLine: Union[int, float, str, origin_float, origin_int],
            buyMoney: Union[int, float, None] = None,
            quantity: Union[int, float, str, origin_float, origin_int, None] = None,
            meta: dict = {},
            block: bool = True,
            timeout: Union[int, float] = 60,
            delay: Union[int, float] = 0.2,
            cancel: bool = True,
            newClientOrderId: str = '',
            newThread: bool = False,
            callback: object = None,
            errorback: object = None,
    ) -> dict:
        '''
        :param symbol: 产品
        :param buyLine: 购买价格
        :param buyMoney: 购买金额
        :param quantity: 下单数量
        :param meta: 回调函数传递参数
        :param block: 是否堵塞
        :param timeout: 订单超时时间 （秒)
        :param delay: 检测订单状态的间隔 (秒)
        :param cancel: 未完全成交是否取消订单
        :param newClientOrderId: 客户自定义订单ID
        :param newThread: 是否开启新线程执行
        :param callback: 非执行异常的回调函数
        :param errorback: 执行异常的回调函数

        buyLine与quantity
            如果是字符串类型，会跳过圆整函数
            如果是origin_float或origin_int类型，会使用origin()的字符串作为下单参数数值
            如果是其他的数字类型，包括int、float、np.float均会先进行圆整，后转化为字符串作为下单参数

        quantity如果为None，会按照购买价格buyLine、购买金额buyMoney计算可以下单的quantity数量
        quantity与buyMoney不能同时为None
        '''
        # 常量参数
        TYPE = 'LIMIT'
        TIMEINFORCE = 'GTC'
        LEVERAGE = 1  # 现货交易视为1倍杠杆
        SIDE = 'BUY'
        # 记录信息
        information = {
            'status': None,
            'meta': None,
            'request_param': None,
            'func_param': None,
            'get_order_result': None,
            'set_order_result': None,
            'error_result': None,
            'cancel_result': None,
        }
        # 函数的参数
        information['func_param'] = dict(
            symbol=symbol,
            buyLine=buyLine,
            buyMoney=buyMoney,
            quantity=quantity,
            meta=meta,
            block=block,
            timeout=timeout,
            delay=delay,
            cancel=cancel,
            newClientOrderId=newClientOrderId,
            newThread=newThread,
            callback=callback,
            errorback=errorback,
        )
        # meta
        information['meta'] = meta

        def main_func(
                symbol=symbol,
                buyLine=buyLine,
                buyMoney=buyMoney,
                quantity=quantity,
                newClientOrderId=newClientOrderId,
                block=block,
                timeout=timeout,
                delay=delay,
                cancel=cancel,
        ):
            # 【开仓数量】 -> buyLine buyLine_f
            # 字符串
            if isinstance(buyLine, str):
                buyLine_f = buyLine
                buyLine = float(buyLine)
            # origin
            elif isinstance(buyLine, origin_float) or isinstance(buyLine, origin_int):
                buyLine_f = buyLine.origin()
                buyLine = buyLine
            # 数字对象
            else:
                # 圆整 -> buyLine
                round_price_result = self.round_price(
                    price=buyLine,
                    symbol=symbol,
                    type='FLOOR',
                )
                # [ERROR RETURN]
                if round_price_result['code'] != 200:
                    return round_price_result
                # 转化为字符串 -> buyLine_f
                buyLine = round_price_result['data']
                buyLine_f_result = self.price_to_f(price=buyLine, symbol=symbol)
                # [ERROR RETURN]
                if buyLine_f_result['code'] != 200:
                    return buyLine_f_result
                buyLine_f = buyLine_f_result['data']
            # 【开仓数量】 quantity quantity_f
            # 字符串
            if isinstance(quantity, str):
                quantity_f = quantity
                quantity = float(quantity)
            # origin
            elif isinstance(quantity, origin_float) or isinstance(quantity, origin_int):
                quantity_f = quantity.origin()
            # 数字对象和None
            else:
                # None 通过buyMoney获取quantity
                if quantity == None:
                    get_quantity_result = self.get_quantity(
                        buyLine=buyLine, buyMoney=buyMoney,
                        leverage=LEVERAGE, symbol=symbol
                    )
                    # [ERROR RETURN]
                    if get_quantity_result['code'] != 200:
                        return get_quantity_result
                    quantity = get_quantity_result['data']
                # 数字对象 圆整quantity
                else:
                    round_quantity_result = self.round_quantity(
                        quantity=quantity, symbol=symbol
                    )
                    # [ERROR RETURN]
                    if round_quantity_result['code'] != 200:
                        return round_quantity_result
                    quantity = round_quantity_result['data']
                # 转化为字符串 -> quantity_f
                quantity_f_result = self.quantity_to_f(quantity=quantity, symbol=symbol)
                # [ERROR RETURN]
                if quantity_f_result['code'] != 200:
                    return quantity_f_result
                quantity_f = quantity_f_result['data']
            request_param = dict(
                symbol=symbol,
                side=SIDE,
                type=TYPE,
                quantity=quantity_f,
                price=buyLine_f,
                newClientOrderId=newClientOrderId,
                timeInForce=TIMEINFORCE,
            )
            information['request_param'] = request_param
            set_order_result = self.set_order(**request_param)  # 下单
            information['set_order_result'] = set_order_result
            # [ERROR RETURN]
            if set_order_result['code'] != 200:
                return set_order_result
            # 是否时堵塞模式
            if not block:
                return None
            orderId = set_order_result['data']['orderId']
            order_result = self.wait_order_FILLED(
                symbol=symbol,
                orderId=orderId,
                timeout=timeout,
                delay=delay,
            )
            information['get_order_result'] = order_result
            information['status'] = order_result['data']['status']
            if order_result['data']['status'] == self.ORDER_STATUS.FILLED:
                # [SUC RETURN]
                return None
            if cancel:
                # 订单取消失败
                cancel_order_result = self.cancel_order(symbol=symbol, orderId=orderId)
                information['cancel_result'] = cancel_order_result
                if cancel_order_result['code'] != 200:
                    return cancel_order_result
            return None

        main_data = dict(
            symbol=symbol,
            buyLine=buyLine,
            buyMoney=buyMoney,
            quantity=quantity,
            newClientOrderId=newClientOrderId,
            block=block,
            timeout=timeout,
            delay=delay,
            cancel=cancel,
        )

        def inner_func():
            try:
                error_result = main_func(**main_data)
                information['error_result'] = error_result
            except:
                error_msg = str(traceback.format_exc())
                error_result = {
                    'code': code.FUNC_EXCEPTION[0],
                    'data': {},
                    'msg': error_msg,
                }
                information['error_result'] = error_result

            if information['error_result']:
                if errorback:
                    errorback(information)
            else:
                if callback:
                    callback(information)
            return information

        if newThread == False:
            return inner_func()
        else:
            t = Thread(target=inner_func)
            t.start()
            return t

    # 市价单购买 Weight > 1
    def open_market(
            self,
            symbol: str,
            buyMoney: Union[int, float, None] = None,
            quantity: Union[int, float, str, origin_float, origin_int] = None,
            meta: dict = {},
            timeout: Union[int, float] = 60,
            delay: Union[int, float] = 0.2,
            cancel: bool = True,
            newClientOrderId: str = '',
            newThread: bool = False,
            callback: object = None,
            errorback: object = None,
    ) -> dict:
        '''
        :param symbol: 产品
        :param buyMoney: 购买金额
        :param quantity: 下单数量
        :param meta: 回调函数传递参数
        :param timeout: 订单超时时间 （秒)
        :param delay: 检测订单状态的间隔 (秒)
        :param cancel: 未完全成交是否取消订单
        :param newClientOrderId: 客户自定义订单ID
        :param newThread: 是否开启新线程执行
        :param callback: 非执行异常的回调函数
        :param errorback: 执行异常的回调函数

        quantity
            如果是字符串类型，会跳过圆整函数
            如果是origin_float或origin_int类型，会使用origin()的字符串作为下单参数数值
            如果是其他的数字类型，包括int、float、np.float均会先进行圆整，后转化为字符串作为下单参数
            如果为None，会选择当前最优的购买价格buyLine、再通过购买金额buyMoney计算可以下单的quantity数量
        quantity与buyMoney不能同时为None
        '''
        TYPE = 'MARKET'
        LEVERAGE = 1
        SIDE = 'BUY'
        # 记录信息
        information = {
            'status': None,
            'meta': None,
            'request_param': None,
            'func_param': None,
            'get_order_result': None,
            'set_order_result': None,
            'error_result': None,
            'cancel_result': None,
        }
        # 函数参数
        information['func_param'] = dict(
            symbol=symbol,
            buyMoney=buyMoney,
            quantity=quantity,
            meta=meta,
            timeout=timeout,
            delay=delay,
            cancel=cancel,
            newClientOrderId=newClientOrderId,
            newThread=newThread,
            callback=callback,
            errorback=errorback,
        )
        # meta
        information['meta'] = meta

        def main_func(
                symbol=symbol,
                buyMoney=buyMoney,
                quantity=quantity,
                newClientOrderId=newClientOrderId,
                timeout=timeout,
                delay=delay,
                cancel=cancel,
        ):
            # 【开仓数量】 quantity quantity_f
            # 字符串
            if isinstance(quantity, str):
                quantity_f = quantity
                quantity = float(quantity)
            # origin
            elif isinstance(quantity, origin_float) or isinstance(quantity, origin_int):
                quantity_f = quantity.origin()
                quantity = quantity
            # 数字对象和None
            else:
                # None 按照最优购买价格 计算下单数量
                if quantity == None:
                    get_bookTicker_result = self._market.get_bookTicker(symbol=symbol)
                    # [ERROR RETURN]
                    if get_bookTicker_result['code'] != 200:
                        return get_bookTicker_result
                    # 最佳卖出价格
                    buyLine = origin_float(get_bookTicker_result['data']['askPrice'])
                    get_quantity_result = self.get_quantity(
                        buyLine=buyLine, buyMoney=buyMoney,
                        leverage=LEVERAGE, symbol=symbol
                    )
                    # [ERROR RETURN]
                    if get_quantity_result['code'] != 200:
                        return get_quantity_result
                    quantity = get_quantity_result['data']
                # 数字对象 圆整下单数量
                else:
                    round_quantity_result = self.round_quantity(
                        quantity=quantity,
                        symbol=symbol
                    )
                    if round_quantity_result['code'] != 200:
                        # [ERROR RETURN]
                        return round_quantity_result
                    quantity = round_quantity_result['data']
                # 下单数量转化为字符串
                quantity_f_result = self.quantity_to_f(quantity=quantity, symbol=symbol)
                # [ERROR RETURN]
                if quantity_f_result['code'] != 200:
                    return quantity_f_result
                quantity_f = quantity_f_result['data']

            request_param = dict(
                symbol=symbol,
                side=SIDE,
                type=TYPE,
                quantity=quantity_f,
                newClientOrderId=newClientOrderId,
            )
            # 购买
            information['request_param'] = request_param
            set_order_result = self.set_order(**request_param)
            information['set_order_result'] = set_order_result

            # [ERROR RETURN]
            if set_order_result['code'] != 200:
                return set_order_result

            orderId = set_order_result['data']['orderId']
            order_result = self.wait_order_FILLED(
                symbol=symbol,
                orderId=orderId,
                timeout=timeout,
                delay=delay,
            )

            information['get_order_result'] = order_result
            information['status'] = order_result['data']['status']

            if order_result['data']['status'] == self.ORDER_STATUS.FILLED:
                # [SUC RETURN]
                return None
            if cancel:
                # 订单取消失败
                cancel_order_result = self.cancel_order(symbol=symbol, orderId=orderId)
                information['cancel_result'] = cancel_order_result
                if cancel_order_result['code'] != 200:
                    return cancel_order_result
            return None

        main_data = dict(
            symbol=symbol,
            buyMoney=buyMoney,
            quantity=quantity,
            newClientOrderId=newClientOrderId,
            timeout=timeout,
            delay=delay,
            cancel=cancel,
        )

        def inner_func():
            try:
                error_result = main_func(**main_data)
                information['error_result'] = error_result
            except:
                error_msg = str(traceback.format_exc())
                error_result = {
                    'code': code.FUNC_EXCEPTION[0],
                    'data': {},
                    'msg': error_msg,
                }
                information['error_result'] = error_result

            if information['error_result']:
                if errorback:
                    errorback(information)
            else:
                if callback:
                    callback(information)
            return information

        if newThread == False:
            return inner_func()
        else:
            t = Thread(target=inner_func)
            t.start()
            return t
