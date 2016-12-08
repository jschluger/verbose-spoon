import dbManager

def get_stock_info(ticker, **kwargs):
    info = get_quote_dict(ticker)
    company_name = info['Name']
    last_price = info['LastPrice']
    timestamp = info['Timestamp']
    resp = [ticker, company_name, last_price, timestamp]
    if 'username' in kwargs:
        my_info = dbManager.get_owned_stocks(ticker)
        num_stocks = my_info[0][2]
        resp.extend(num_stocks)
    return resp


    
