import urllib2, json
import dbManager

def get_json_response(url):
    u = urllib2.urlopen(url)
    response = u.read()

    data = json.loads(response)

    return data

def get_stock_price(symbol):
    if symbol == '':
        return 'Invalid Stock Symbol'
    
    data = get_json_response('http://dev.markitondemand.com/Api/v2/Quote/json?symbol=' + symbol)

    if 'Message' in data:
        return 'Invalid Stock Symbol'
    
    return data['LastPrice']

# See http://dev.markitondemand.com/MODApis/ for all the elements in the dict

def get_quote_dict(symbol):
    if symbol == '':
        return 'Invalid Stock Symbol'
    
    data = get_json_response('http://dev.markitondemand.com/Api/v2/Quote/json?symbol=' + symbol)

    if 'Message' in data:
        return 'Invalid Stock Symbol'

    return data

def get_chart(symbol, normalized = "false", number_of_days = 365, data_period = 'Day', type = 'price'):
    data = {}
    data['Normalized'] = normalized
    data['NumberOfDays'] = number_of_days
    data['DataPeriod'] = data_period
    to_graph = {}
    to_graph['Symbol'] = symbol
    to_graph['Type'] = "price"
    to_graph['Params'] = ['c']
    data['Elements'] = to_graph

    json_data = json.dumps(data)

    return json_data

def lookup(search_term):
    if search_term == '':
        return 'No empty string search terms'

    data = get_json_response('http://dev.markitondemand.com/Api/v2/Lookup/json?input=' + search_term)

    if 'Message' in data:
        return 'Error'

    return data

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
    
    
    
