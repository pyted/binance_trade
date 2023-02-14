from paux.param import to_local
from pbinance import SPOT
from binance_trade import code
from binance_trade import utils
from binance_trade import exception


class AccountSPOT():

    def __init__(self, key: str, secret: str):
        self.inst = SPOT(key=key, secret=secret)

    # 获取账户信息 Weight: 5
    def get_account(self, recvWindow: int = '') -> dict:
        '''
        https://binance-docs.github.io/apidocs/spot/cn/#user_data-23
        '''
        return self.inst.accountTrade.get_account(**to_local(locals()))

    # 获取全部现货余额 Weight: 5
    def get_balances(self):
        '''
        https://binance-docs.github.io/apidocs/spot/cn/#user_data-23
        '''
        account_result = self.get_account()
        if account_result['code'] != 200:
            return account_result
        result = {
            'code': 200,
            'data': account_result['data']['balances'],
            'msg': ''
        }
        return result

    # 获取单个现货余额 Weight: 5
    def get_balance(self, asset: str = '', symbol: str = '', base_asset: str = ''):
        '''
        https://binance-docs.github.io/apidocs/spot/cn/#user_data-23

        :param asset: 货币名称
        :param symbol: 产品名称
        :param base_asset: 产品的交易基础货币
        asset与symbol不能同时为空

        例如：对于产品：BTCUSDT，其中：
            asset = 'BTC'
            symbol = 'BTCUSDT'
            base_asset = 'USDT'
        '''
        if not asset and not symbol:
            raise exception.ParamException('asset and symbol can not be empty together')
        if not asset:
            asset = utils.get_asset(symbol=symbol, base_asset=base_asset)
        account_result = self.get_account()
        if account_result['code'] != 200:
            return account_result
        for balance in account_result['data']['balances']:
            if balance['asset'] == asset:
                result = {
                    'code': 200,
                    'data': balance,
                    'msg': ''
                }
                return result
        else:
            msg = f'Can not find asset = {asset}'
            result = {
                'code': code.ASSET_ERROR[0],
                'data': {},
                'msg': msg,
            }
            return result
