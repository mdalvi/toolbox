def get_strike_file_pattern(expiry, trading_symbol, variant=False, strike=None, spot_price=None, side=None, **kwargs):
    """
    Get name of strike file
    :param expiry: Expiry date, datetime/date format
    :param strike: Option strike price
    :param trading_symbol: Trading symbol
    :param spot_price: Spot price
    :param variant: Bool, some historical files observed %Y instead of %y
    :param side: PUT or CALL
    :return:
    """
    assert ((spot_price is None and side is None) is False), "Both spot_price and side cannot be None"
    assert ((strike is None and side is None) is False), "Both strike and side cannot be None"

    sp = "*"
    if strike is not None:
        sp = int(strike)

    if side is None:
        side = 'CE' if sp >= spot_price else 'PE'

    if variant:
        exp = expiry.strftime("%d%b%Y").upper()
    else:
        exp = expiry.strftime("%d%b%y").upper()

    return f"{trading_symbol}{exp}{sp}{side}.NFO.csv"
