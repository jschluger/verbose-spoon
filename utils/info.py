import dbManager
import api

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



def get_user_info(username):
    f = "database.db"
    db = sqlite3.connect(f)
    c = db.cursor()

    query = "SELECT * FROM users WHERE username == ?"
    c.execute(query, (username,))
    personal_info = c.fetchone()
    
    pstocks_info = dbManager.get_owned_stocks(username)

    resp = [personal_info, pstocks_info]
    return resp

def search_results(search):
    dictOfDicts = api.lookup(search)
    result = [][]
    for i in range(len(dictOfDicts)):
        result[i][0] = dictOfDicts[i]['Name']
        result[i][1] = dictOfDicts[i]['Symbol']
    return result
        
