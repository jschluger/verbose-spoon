import dbManager

def get_stock_info(ticker, **kwargs):
    info = get_quote_dict(ticker)
    company_name = info['Name']
    last_price = info['LastPrice']
    timestamp = info['Timestamp']
    resp = [ticker, company_name, last_price, timestamp]
    if 'username' in kwargs:
        stocks = dbManager.get_owned_stocks(ticker)
        resp.extend(stocks)
    return resp
