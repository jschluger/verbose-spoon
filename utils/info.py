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

    q = 'SELECT funds FROM users WHERE username == "%s"'%(username)
    c.execute(q)
    pfunds = c.fetchone()[0]
    q = 'SELECT fullName FROM users WHERE username == "%s"'%(username)
    c.execute(q)
    pname = c.fetchone()[0]
    q = 'SELECT dob FROM users WHERE username == "%s"'%(username)
    c.execute(q)
    pdob = c.fetchone()[0]
    q = 'SELECT favStock FROM users WHERE username == "%s"'%(username)
    c.execute(q)
    pstock = c.fetchone()[0]
    
    resp = [pfunds, pname, pdob, pstock]

    db.commit()
    db.close()
    return resp

def search_results(search):
    dictOfDicts = api.lookup(search)
    result = [][]
    for i in range(len(dictOfDicts)):
        result[i][0] = dictOfDicts[i]['Name']
        result[i][1] = dictOfDicts[i]['Symbol']
    return result
        
