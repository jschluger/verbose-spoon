import dbManager
import api
import sqlite3
import locale

'''locale.setlocale(locale.LC_ALL, 'en_US')'''

def displayPrice( x ):
    return locale.format("%f", 1255000, True)

def get_stock_info(ticker, **kwargs):
    info = api.get_quote_dict(ticker)
    if isinstance(info, basestring):
        return info
    company_name = info['Name']
    last_price = info['LastPrice']
    timestamp = info['Timestamp']
    resp = [ticker, company_name, last_price, timestamp]
    if 'username' in kwargs:
        num_stocks = dbManager.get_owned_stocks(kwargs['username'],symbol=ticker)
        resp.append(num_stocks)
    return resp

#print get_stock_info("CHK", username='jordan')

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
    result = [[0 for x in range(len(dictOfDicts[0]))]for y in range(len(dictOfDicts))]
    for i in range(len(dictOfDicts)):
        result[i][0] = dictOfDicts[i]['Name']
        result[i][1] = dictOfDicts[i]['Symbol']
    return result
        
