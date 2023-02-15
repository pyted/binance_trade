# Binance_trade 说明文档

## 1 Binance_trade 介绍

Biance_trade基于pbinance与binance_candle封装了现货（SPOT）、U本位（UM）与币本位（CM）中常用的函数，降低量化交易难度。

## 2 安装Binance_trade

```cmd
pip3 install binance_trade
```

## 3 快速开始

1.获取现货现货交易BTCUSDT的价格，降价2%挂单买入，买入金额为1000USDT，挂单时间为2小时，如果超时则取消订单。

```python
from binance_trade import BinanceSPOT
from pprint import pprint

if __name__ == '__main__':
    binanceSPOT = BinanceSPOT(
        key='****',
        secret='****',
    )

    # 产品
    symbol = 'BTCUSDT'
    # 开仓金额
    buyMoney = 10000
    # 购买价格
    askPrice = binanceSPOT.market.get_bookTicker(symbol=symbol)['data']['askPrice']  # 卖1价格
    askPrice = float(askPrice)
    buyLine = askPrice * 0.98  # 降价2%
    # 挂单时间
    timeout = 60 * 60 * 2  # 单位秒
    # 超时是否取消订单
    cancel = True
    # 是否堵塞模式
    block = True

    # 限价单开仓
    result = binanceSPOT.trade.open_limit(
        symbol=symbol,  # 产品
        buyLine=buyLine,  # 开仓价格
        buyMoney=buyMoney,  # 开仓金额 开仓金额buyMoney和开仓数量quantity必须输入其中一个 优先级：quantity > buyMoney
        timeout=timeout,  # 等待订单成功的超时时间
        cancel=True,  # 订单超时后是否取消
    )
    pprint(result)
```

2.获取U本位合约BTCUSDT的价格，降价5%，采用逐仓、10倍杠杆、开仓金额1000USDT挂单，挂单时间为2小时，如果超时则取消。

**采用异步的方式管理这个订单，并设置订单成功或失败后的回调函数**

```python
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
    binanceUM = BinanceUM(
        key='****',
        secret='****'
    )

    # 产品
    symbol = 'BTCUSDT'
    # 开仓金额
    buyMoney = 10000
    # 购买价格
    askPrice = binanceUM.market.get_bookTicker(symbol=symbol)['data']['askPrice']  # 卖1价格
    askPrice = float(askPrice)
    buyLine = askPrice * 0.95  # 降价5%

    # 限价单开仓
    binanceUM.trade.open_limit(
        symbol=symbol,  # 产品
        buyLine=buyLine,  # 开仓价格
        marginType='ISOLATED',  # 保证金模式： ISOLATED: 逐仓 CROSSED: 全仓
        positionSide='LONG',  # 持仓方向 LONG: 多单 SHORT: 空单
        leverage=10,  # 开仓金额
        buyMoney=buyMoney,  # 开仓金额 开仓金额buyMoney和开仓数量quantity必须输入其中一个 优先级：quantity > buyMoney
        quantity=None,  # 开仓数量 None：用buyMoney计算可以购买的最大数量
        block=True,  # 是否以堵塞的模式
        timeout=60 * 60 * 2,  # 等待订单成功的超时时间
        delay=0.2,  # 间隔多少秒检测订单是否成功
        cancel=True,  # 订单超时后是否取消
        callback=callback,  # 开仓成功触发的回调函数
        errorback=errorback,  # 开仓失败触发的回调函数
        newThread=True,  # 是否开启一个新的线程维护这个订单
        newClientOrderId='',  # 客户自定义订单ID
        meta={},  # 向回调函数中传递的参数字典
    )
```

3.对于U本位合约以当前BTCUSDT的价格，止盈20%挂单买入平空，超时时间2小时，超时后取消订单，并设置回调函数。


```python
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
    binanceUM = BinanceUM(
        key='****',
        secret='****'
    )

    # 产品
    symbol = 'BTCUSDT'

    # 限价单平仓
    binanceUM.trade.close_limit(
        symbol=symbol,  # 产品
        marginType='ISOLATED',  # 保证金模式： ISOLATED: 逐仓 CROSSED: 全仓
        positionSide='LONG',  # 持仓方向 LONG: 多单 SHORT: 空单
        sellLine=None,  # 平仓价格 平仓价格sellLine与止盈率tpRate必须添加一个 优先级sellLine > tpRate
        tpRate=0.2,  # 止盈率
        # 平多 positionSide="LONG":   sellLine = askPrice * (1 + abs(tpRate))
        # 平空 positionSide="SHORT":  sellLine = askPrice * (1 - abs(tpRate))
        quantity='all',  # 平仓数量，'all' 表示全部
        block=True,  # 是否以堵塞的模式
        timeout=60 * 60 * 2,  # 等待订单成功的超时时间
        delay=0.2,  # 间隔多少秒检测订单是否成功
        cancel=True,  # 订单超时后是否取消
        callback=callback,  # 平仓成功触发的回调函数
        errorback=errorback,  # 平仓失败触发的回调函数
        newThread=True,  # 是否开启一个新的线程维护这个订单
        newClientOrderId='',  # 客户自定义订单ID
        meta={},  # 向回调函数中传递的参数字典
    )
```

## 4 现货产品 BinanceSPOT

### 4.1 现货账户

便捷函数：

|函数名|说明|
|:---|:---|  
|get_account|获取账户信息|
|get_balances|获取全部现货余额|  
|get_balance|获取单个现货余额|

```python
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
```

### 4.2 现货行情

#### 4.2.1 现货交易规则信息

便捷函数：

|函数名|说明|
|:---|:---|  
|get_exchangeInfos|获取全部交易规则与交易对|
|get_exchangeInfo|获取单个交易规则与交易对|  
|get_symbols_trading_on|获取可以交易的产品列表|
|get_symbols_trading_off|获取不可交易的产品列表|


```python
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
```

#### 4.2.2 现货实时价格

便捷函数：

|函数名|说明|
|:---|:---|  
|get_bookTickersMap|获取全部产品的最优挂单字典(包含不可交易的产品)|
|get_bookTickers|获取全部产品的最优挂单列表(包含不可交易的产品)|
|get_bookTicker|获取单个产品的最优挂单|
|get_tickerPricesMap|获取全部产品的最新价格字典(包含不可交易的产品)|
|get_tickerPrices|获取全部产品的最新价格列表(包含不可交易的产品)|
|get_tickerPrice|获取单个产品的最新价格|
|get_depth|获取单个产品的深度交易|

```python
from binance_trade import BinanceSPOT
from pprint import pprint

if __name__ == '__main__':
    key = '****'
    secret = '****'
    binanceSPOT = BinanceSPOT(key=key, secret=secret)

    # 获取全部产品的最优挂单
    bookTickersMap = binanceSPOT.market.get_bookTickersMap()
    pprint(bookTickersMap)
    bookTickers = binanceSPOT.market.get_bookTickers()
    pprint(bookTickers)

    # 获取单个产品的最优挂单
    bookTicker = binanceSPOT.market.get_bookTicker(symbol='BTCUSDT')
    pprint(bookTicker)

    # 获取全部产品的最新价格
    tickerPricesMap = binanceSPOT.market.get_tickerPricesMap()
    pprint(tickerPricesMap)
    tickerPrices = binanceSPOT.market.get_tickerPrices()
    pprint(tickerPrices)

    # 获取单个产品的最新价格
    tickerPrice = binanceSPOT.market.get_tickerPrice(symbol='BTCUSDT')
    pprint(tickerPrice)

    # 获取单个产品的深度交易
    depth = binanceSPOT.market.get_depth(symbol='BTCUSDT', limit=100)
    pprint(depth)
```

#### 4.2.3 现货历史K线

便捷函数：

|函数名|说明|
|:---|:---|  
|get_history_candle|获取产品的历史K线数据|
|get_history_candle_latest|获取产品指定数量的最新历史K线数据|
|get_history_candle_by_date|获取产品指定日期的历史K线数据|


```python
from binance_trade import BinanceSPOT
from pprint import pprint

if __name__ == '__main__':
    key = '****'
    secret = '****'
    binanceSPOT = BinanceSPOT(key=key, secret=secret)

    # 获取产品的历史K线数据
    history_candle = binanceSPOT.market.get_history_candle(
        symbol='BTCUSDT',
        start='2023-01-01 00:00:00',
        end='2023-01-01 23:59:00',
        bar='1m',
    )
    pprint(history_candle)

    # 获取产品指定数量的最新历史K线数据
    history_candle_latest = binanceSPOT.market.get_history_candle_latest(
        symbol='BTCUSDT',
        length=1440,
        bar='1m',
    )
    pprint(history_candle_latest)

    # 获取产品指定日期的历史K线数据
    history_candle_by_date = binanceSPOT.market.get_history_candle_by_date(
        symbol='BTCUSDT',
        date='2023-01-01',
        bar='1m',
    )
    pprint(history_candle_by_date)
```

### 4.3 现货交易

#### 4.3.1 现货基础订单

便捷函数：

|函数名|说明|
|:---|:---|
|set_order|普通下单购买|  
|get_order|查询订单|  
|get_openOrders|查看全部当前全部挂单|
|get_openOrder|查询单个产品当前挂单|
|cancel_order|撤销订单|
|wait_order_FILLED|等待订单成交|

```python
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
```

#### 4.3.2 现货限价单开仓

便捷函数：

|函数名|说明|
|:---|:---|
|open_limit|限价单开仓|

```python
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
```

#### 4.2.3 现货市价单开仓

便捷函数：

|函数名|说明|
|:---|:---|
|open_market|市价单开仓|

```python
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
    binanceSPOT = BinanceSPOT(key=key, secret=secret)

    symbol = 'xxxx'  # 测试产品 可以选择：PHAUSDT
    buyMoney = 15  # 购买金额

    # 市价单开仓
    binanceSPOT.trade.open_market(
        symbol=symbol,  # 产品
        buyMoney=buyMoney,  # 开仓金额 开仓金额buyMoney和开仓数量quantity必须输入其中一个
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
```

#### 4.2.4 现货限价单平仓

便捷函数：

|函数名|说明|
|:---|:---|
|close_limit|限价单平仓|

```python
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
            'func_param': <close_limit中的参数>,
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
            'func_param': <close_limit中的参数>,
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
    base_asset = 'USDT'  # 产品的基础货币

    # 限价单平仓
    binanceSPOT.trade.close_limit(
        symbol=symbol,  # 产品
        base_asset=base_asset,  # 产品的基础货币
        sellLine=None,  # 平仓价格 平仓价格sellLine与止盈率tpRate必须添加一个 优先级sellLine > tpRate
        tpRate=0.05,  # 以(当前实时价格 * (1 + tpRate)) 作为平仓价格
        quantity='all',  # 平仓数量，'all' 表示全部
        block=True,  # 是否以堵塞的模式
        timeout=10,  # 等待订单成功的超时时间
        delay=0.2,  # 间隔多少秒检测订单是否成功
        cancel=True,  # 订单超时后是否取消
        callback=callback,  # 平仓成功触发的回调函数
        errorback=errorback,  # 平仓失败触发的回调函数
        newThread=True,  # 是否开启一个新的线程维护这个订单
        newClientOrderId='',  # 客户自定义订单ID
        meta={},  # 向回调函数中传递的参数字典
    )
```

#### 4.2.5 现货市价单平仓

便捷函数：

|函数名|说明|
|:---|:---|
|close_market|市价单平仓|

```python
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
            'func_param': <close_market中的参数>,
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
            'func_param': <close_market中的参数>,
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

    symbol = 'xxxx'  # 测试产品 可以选择：PHAUSDT
    base_asset = 'USDT'  # 产品的基础货币

    # 市价单平仓
    binanceSPOT.trade.close_market(
        symbol=symbol,  # 产品
        base_asset=base_asset,  # 产品的基础货币
        quantity='all',  # 平仓数量，'all' 表示全部
        timeout=10,  # 等待订单成功的超时时间
        delay=0.2,  # 间隔多少秒检测订单是否成功
        cancel=True,  # 订单超时后是否取消
        callback=callback,  # 平仓成功触发的回调函数
        errorback=errorback,  # 平仓失败触发的回调函数
        newThread=False,  # 是否开启一个新的线程维护这个订单
        newClientOrderId='',  # 客户自定义订单ID
        meta={},  # 向回调函数中传递的参数字典
    )
```

## 5 U本位合约 BinanceUM

便捷函数：

|函数名|说明|
|:---|:---|
|get_account|获取账户信息|
|get_balances|获取账户全部余额|
|get_balance|获取账户单个货币余额|
|set_leverage|调整开仓杠杆|
|set_marginType|更改持仓模式|
|get_positions|获取全部产品的持仓信息|
|get_position|获取单个产品的持仓信息|

### 5.1 U本位账户

```python
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
```

### 5.2 U本位行情

#### 5.2.1 U本位交易规则信息

便捷函数：

|函数名|说明|
|:---|:---|  
|get_exchangeInfos|获取全部交易规则与交易对|
|get_exchangeInfo|获取单个交易规则与交易对|  
|get_symbols_trading_on|获取可以交易的产品列表|
|get_symbols_trading_off|获取不可交易的产品列表|

```python
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
```

#### 5.2.2 U本位实时价格

便捷函数：

|函数名|说明|
|:---|:---|  
|get_bookTickersMap|获取全部产品的最优挂单字典(包含不可交易的产品)|
|get_bookTickers|获取全部产品的最优挂单列表(包含不可交易的产品)|
|get_bookTicker|获取单个产品的最优挂单|
|get_tickerPricesMap|获取全部产品的最新价格字典(包含不可交易的产品)|
|get_tickerPrices|获取全部产品的最新价格列表(包含不可交易的产品)|
|get_tickerPrice|获取单个产品的最新价格|
|get_depth|获取单个产品的深度交易|

```python
from binance_trade import BinanceUM
from pprint import pprint

if __name__ == '__main__':
    key = '****'
    secret = '****'
    binanceUM = BinanceUM(key=key, secret=secret)

    # 获取全部产品的最优挂单
    bookTickersMap = binanceUM.market.get_bookTickersMap()
    pprint(bookTickersMap)
    bookTickers = binanceUM.market.get_bookTickers()
    pprint(bookTickers)

    # 获取单个产品的最优挂单
    bookTicker = binanceUM.market.get_bookTicker(symbol='BTCUSDT')
    pprint(bookTicker)

    # 获取全部产品的最新价格
    tickerPricesMap = binanceUM.market.get_tickerPricesMap()
    pprint(tickerPricesMap)
    tickerPrices = binanceUM.market.get_tickerPrices()
    pprint(tickerPrices)

    # 获取单个产品的最新价格
    tickerPrice = binanceUM.market.get_tickerPrice(symbol='BTCUSDT')
    pprint(tickerPrice)

    # 获取单个产品的深度交易
    depth = binanceUM.market.get_depth(symbol='BTCUSDT', limit=100)
    pprint(depth)
```

#### 5.2.3 U本位历史K线

便捷函数：

|函数名|说明|
|:---|:---|  
|get_history_candle|获取产品的历史K线数据|
|get_history_candle_latest|获取产品指定数量的最新历史K线数据|
|get_history_candle_by_date|获取产品指定日期的历史K线数据|

```python
from binance_trade import BinanceUM
from pprint import pprint

if __name__ == '__main__':
    key = '****'
    secret = '****'
    binanceUM = BinanceUM(key=key, secret=secret)
    
    # 获取产品的历史K线数据
    history_candle = binanceUM.market.get_history_candle(
        symbol='BTCUSDT',
        start='2023-01-01 00:00:00',
        end='2023-01-01 23:59:00',
        bar='1m',
    )
    pprint(history_candle)

    # 获取产品指定数量的最新历史K线数据
    history_candle_latest = binanceUM.market.get_history_candle_latest(
        symbol='BTCUSDT',
        length=1440,
        bar='1m',
    )
    pprint(history_candle_latest)

    # 获取产品指定日期的历史K线数据
    history_candle_by_date = binanceUM.market.get_history_candle_by_date(
        symbol='BTCUSDT',
        date='2023-01-01',
        bar='1m',
    )
    pprint(history_candle_by_date)
```

### 5.3 U本位交易

#### 5.3.1 U本位基础订单

便捷函数：

|函数名|说明|
|:---|:---|
|set_order|普通下单购买|  
|get_order|查询订单|  
|get_openOrders|查看全部当前全部挂单|
|get_openOrder|查询单个产品当前挂单|
|cancel_order|撤销订单|
|wait_order_FILLED|等待订单成交|

```python
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
        positionSide='LONG',
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
```

#### 5.3.2 U本位限价单开仓

便捷函数：

|函数名|说明|
|:---|:---|
|open_limit|限价单开仓|

```python
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
    binanceUM = BinanceUM(key=key, secret=secret)

    symbol = 'BATUSDT'  # 测试产品
    buyMoney = 15  # 购买金额
    askPrice = binanceUM.market.get_bookTicker(symbol=symbol)['data']['askPrice']  # 卖1价格
    askPrice = float(askPrice)
    buyLine = askPrice * 0.8  # 购买价格为卖1价的8折，测试挂单

    # 限价单开仓
    binanceUM.trade.open_limit(
        symbol=symbol,  # 产品
        buyLine=buyLine,  # 开仓价格
        marginType='ISOLATED',  # 保证金模式： ISOLATED: 逐仓 CROSSED: 全仓
        positionSide='LONG',  # 持仓方向 LONG: 多单 SHORT: 空单
        leverage=1,  # 开仓杠杆
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
```

#### 5.3.3 U本位市价单开仓

便捷函数：

|函数名|说明|
|:---|:---|
|open_market|市价单开仓|

```python
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
```

#### 5.3.4 U本位限单价平仓

便捷函数：

|函数名|说明|
|:---|:---|
|close_limit|限价单平仓|

```python
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
            'func_param': <close_limit中的参数>,
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
            'func_param': <close_limit中的参数>,
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

    symbol = 'BATUSDT'  # 测试产品

    # 限价单平仓
    binanceUM.trade.close_limit(
        symbol=symbol,  # 产品
        marginType='ISOLATED',  # 保证金模式： ISOLATED: 逐仓 CROSSED: 全仓
        positionSide='LONG',  # 持仓方向 LONG: 多单 SHORT: 空单
        sellLine=None,  # 平仓价格 平仓价格sellLine与止盈率tpRate必须添加一个 优先级sellLine > tpRate
        tpRate=0.05,  # 止盈率
        # 平多 positionSide="LONG":   sellLine = askPrice * (1 + abs(tpRate))
        # 平空 positionSide="SHORT":  sellLine = askPrice * (1 - abs(tpRate))
        quantity='all',  # 平仓数量，'all' 表示全部
        block=True,  # 是否以堵塞的模式
        timeout=10,  # 等待订单成功的超时时间
        delay=0.2,  # 间隔多少秒检测订单是否成功
        cancel=True,  # 订单超时后是否取消
        callback=callback,  # 平仓成功触发的回调函数
        errorback=errorback,  # 平仓失败触发的回调函数
        newThread=True,  # 是否开启一个新的线程维护这个订单
        newClientOrderId='',  # 客户自定义订单ID
        meta={},  # 向回调函数中传递的参数字典
    )
```

#### 5.3.5 U本位市价单平仓

便捷函数：

|函数名|说明|
|:---|:---|
|close_market|市价单平仓|

```python
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
            'func_param': <close_market中的参数>,
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
            'func_param': <close_market中的参数>,
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

    # 市价单平仓
    binanceUM.trade.close_market(
        symbol=symbol,  # 产品
        marginType='ISOLATED',  # 保证金模式： ISOLATED: 逐仓 CROSSED: 全仓
        positionSide='LONG',  # 持仓方向 LONG: 多单 SHORT: 空单
        quantity='all',  # 平仓数量，'all' 表示全部
        timeout=10,  # 等待订单成功的超时时间
        delay=0.2,  # 间隔多少秒检测订单是否成功
        cancel=True,  # 订单超时后是否取消
        callback=callback,  # 平仓成功触发的回调函数
        errorback=errorback,  # 平仓失败触发的回调函数
        newThread=False,  # 是否开启一个新的线程维护这个订单
        newClientOrderId='',  # 客户自定义订单ID
        meta={},  # 向回调函数中传递的参数字典
    )
```

## 6 币本位合约 BinanceCM

币本位合约的使用方式与U本位相同，类名为BinanceCM

```python
from binance_trade import BinanceCM

if __name__ == '__main__':
    binanceCM = BinanceCM(
        key='****',
        secret='****',
    )

    # binanceCM.account.xxxx
    # binanceCM.market.xxxx
    # binanceCM.trade.xxxx
```