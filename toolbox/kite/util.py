from kiteconnect import KiteConnect
from kiteconnect.exceptions import DataException

from toolbox.requests.util import retry


class Kite(object):

    def __init__(self, api_key, access_token, debug=False):
        self.kite = KiteConnect(api_key=api_key, access_token=access_token, debug=debug)

        # Products
        self.PRODUCT_MIS = self.kite.PRODUCT_MIS
        self.PRODUCT_CNC = self.kite.PRODUCT_CNC
        self.PRODUCT_NRML = self.kite.PRODUCT_NRML
        self.PRODUCT_CO = self.kite.PRODUCT_CO
        self.PRODUCT_BO = self.kite.PRODUCT_BO

        # Order types
        self.ORDER_TYPE_MARKET = self.kite.ORDER_TYPE_MARKET
        self.ORDER_TYPE_LIMIT = self.kite.ORDER_TYPE_LIMIT
        self.ORDER_TYPE_SLM = self.kite.ORDER_TYPE_SLM
        self.ORDER_TYPE_SL = self.kite.ORDER_TYPE_SL

        # Varieties
        self.VARIETY_REGULAR = self.kite.VARIETY_REGULAR
        self.VARIETY_BO = self.kite.VARIETY_BO
        self.VARIETY_CO = self.kite.VARIETY_CO
        self.VARIETY_AMO = self.kite.VARIETY_AMO

        # Transaction type
        self.TRANSACTION_TYPE_BUY = self.kite.TRANSACTION_TYPE_BUY
        self.TRANSACTION_TYPE_SELL = self.kite.TRANSACTION_TYPE_SELL

        # Validity
        self.VALIDITY_DAY = self.kite.VALIDITY_DAY
        self.VALIDITY_IOC = self.kite.VALIDITY_IOC

        # Position Type
        self.POSITION_TYPE_DAY = self.kite.POSITION_TYPE_DAY
        self.POSITION_TYPE_OVERNIGHT = self.kite.POSITION_TYPE_OVERNIGHT

        # Exchanges
        self.EXCHANGE_NSE = self.kite.EXCHANGE_NSE
        self.EXCHANGE_BSE = self.kite.EXCHANGE_BSE
        self.EXCHANGE_NFO = self.kite.EXCHANGE_NFO
        self.EXCHANGE_CDS = self.kite.EXCHANGE_CDS
        self.EXCHANGE_BFO = self.kite.EXCHANGE_BFO
        self.EXCHANGE_MCX = self.kite.EXCHANGE_MCX
        self.EXCHANGE_BCD = self.kite.EXCHANGE_BCD

        # Margins segments
        self.MARGIN_EQUITY = self.kite.MARGIN_EQUITY
        self.MARGIN_COMMODITY = self.kite.MARGIN_COMMODITY

        # Status constants
        self.STATUS_COMPLETE = self.kite.STATUS_COMPLETE
        self.STATUS_REJECTED = self.kite.STATUS_REJECTED
        self.STATUS_CANCELLED = self.kite.STATUS_CANCELLED

        # GTT order type
        self.GTT_TYPE_OCO = self.kite.GTT_TYPE_OCO
        self.GTT_TYPE_SINGLE = self.kite.GTT_TYPE_SINGLE

        # GTT order status
        self.GTT_STATUS_ACTIVE = self.kite.GTT_STATUS_ACTIVE
        self.GTT_STATUS_TRIGGERED = self.kite.GTT_STATUS_TRIGGERED
        self.GTT_STATUS_DISABLED = self.kite.GTT_STATUS_DISABLED
        self.GTT_STATUS_EXPIRED = self.kite.GTT_STATUS_EXPIRED
        self.GTT_STATUS_CANCELLED = self.kite.GTT_STATUS_CANCELLED
        self.GTT_STATUS_REJECTED = self.kite.GTT_STATUS_REJECTED
        self.GTT_STATUS_DELETED = self.kite.GTT_STATUS_DELETED

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
