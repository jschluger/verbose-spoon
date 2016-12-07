import urllib2, json

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

def lookup(search_term):
    if search_term == '':
        return 'No empty string search terms'

    data = get_json_response('http://dev.markitondemand.com/Api/v2/Lookup/json?input=' + search_term)

    if 'Message' in data:
        return 'Error'

    return data
