from kiteconnect import KiteConnect
from kiteconnect.exceptions import DataException

from toolbox.requests.util import retry


class Kite(object):

    def __init__(self, api_key, access_token, debug=False):
        self.kite = KiteConnect(api_key=api_key, access_token=access_token, debug=debug)

    @retry((DataException,), tries=5, delay=5)
    def historical_data(self, *args, **kwargs):
        """
        https://kite.trade/docs/pykiteconnect/v3/#kiteconnect.KiteConnect.historical_data
        :param args:
        :param kwargs:
        :return:
        """
        return self.kite.historical_data(*args, **kwargs)

    @retry((DataException,), tries=5, delay=5)
    def instruments(self, *args, **kwargs):
        """
        https://kite.trade/docs/pykiteconnect/v3/#kiteconnect.KiteConnect.instruments
        :param args:
        :param kwargs:
        :return:
        """
        return self.kite.instruments(*args, **kwargs)
