from kiteconnect import KiteConnect
from kiteconnect.exceptions import DataException

from toolbox.requests.util import retry


class Kite(object):

    def __init__(self, api_key, access_token, debug=False, logger=None):
        self.kite = KiteConnect(api_key=api_key, access_token=access_token, debug=debug)

    @retry((DataException,), tries=5, delay=5)
    def historical_data(self, *args, **kwargs):
        return self.kite.historical_data(*args, **kwargs)
