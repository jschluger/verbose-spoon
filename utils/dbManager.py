import sqlite3   #enable control of an sqlite database
def toPosInt( x ):
    try:
        x = int(x)
    except:
        return -1 # bad

    if x < 0:
        return -1 # bad
    else:
        return x
   
    
def buyStock(stockName, shares, price, username):
    f = "database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops

    shares = toPosInt( shares )
    if shares < 0:
        return 0 # invalid value for shares
    
    if (enufMoney(username,shares,price)):
        theMoney = """SELECT funds FROM users WHERE username == "%s" """ % (username)
        c.execute(theMoney)
        money = c.fetchone()[0]
        deduct = price * shares
        newMoney = money - deduct
        p = 'UPDATE users SET funds = %d WHERE username == "%s"'%(newMoney, username
        )
        c.execute(p)
        
        p = 'SELECT EXISTS(SELECT 1 FROM stocks WHERE username = "%s" AND stockName = "%s")'%(username, stockName)
        c.execute(p)
        if (c.fetchone()[0] == 0):
            p = 'INSERT INTO stocks VALUES("%s","%s",%d)' %(username,stockName,shares)
            c.execute(p)
        else:
            p = 'SELECT shares FROM stocks WHERE username == "%s" AND stockName == "%s"'%(username, stockName)
            c.execute(p)
            newShares = c.fetchone()[0] + shares
            p = 'UPDATE stocks SET shares = %d WHERE username == "%s" AND stockName == "%s"'%(newShares, username, stockName)
            c.execute(p)
    else:
        db.commit()
        db.close()
        return 1 # not enough money
    
    db.commit()
    db.close()
    return 2 #success
    
def sellStock(stockName, shares, price, username):
    f = "database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops

    shares = toPosInt(shares)
    if shares < 0:
        return 0

    if (canYouEvenSell(username, stockName, shares)):
        
        theMoney = """SELECT funds FROM users WHERE username == "%s" """ % (username)
        c.execute(theMoney)
        money = c.fetchone()[0]
        add = price * shares
        newMoney = money + add
        print str(newMoney)
        p = 'UPDATE users SET funds = %d WHERE username == "%s"'%(newMoney, username)
        c.execute(p)
        p = 'SELECT funds FROM users WHERE username == "%s"'%(username)
        c.execute(p)
        print str(c.fetchone()[0])
             
        p = 'SELECT shares FROM stocks WHERE username == "%s" AND stockName = "%s"'%(username, stockName)
        c.execute(p)
        newShares = c.fetchone()[0] - shares
        p = 'UPDATE stocks SET shares = %d WHERE username == "%s" AND stockName == "%s"'%(newShares, username, stockName)
        c.execute(p)
    else:
        db.commit()
        db.close()
        return 1

    db.commit()
    db.close()
    return 2
    
def enufMoney(username,shares,price):
    f = "database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops

    trying = shares*price
    p = 'SELECT funds FROM users WHERE username == "%s"'%(username)
    c.execute(p)
    available = c.fetchone()[0]
    db.commit()
    db.close()
    return (available > trying)

def canYouEvenSell(username,stockName,shares):
    f = "database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops

    p = 'SELECT EXISTS(SELECT 1 FROM stocks WHERE username = "%s" AND stockName = "%s")'%(username, stockName)

    c.execute(p)
    if (c.fetchone()[0] == 1):
        p = 'SELECT shares FROM stocks WHERE username == "%s" AND stockName == "%s"'%(username, stockName)
        c.execute(p)
        truth = (c.fetchone()[0] >= shares)
        db.commit()
        db.close()
        return truth
    db.commit()
    db.close()
    return False

def get_owned_stocks(username, **kwargs):
    f = "database.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    
    if 'symbol' in kwargs:
        query = "SELECT * FROM stocks WHERE username == ? AND stockName == ?"
        c.execute(query, (username, kwargs['symbol'],))
        result = c.fetchall()
        db.commit()
        db.close()
        if result:
            num_stocks = result[0][2]
        else:
            num_stocks = 0
        return num_stocks
    
    query = 'SELECT * FROM stocks WHERE username == "%s"'%(username)
    c.execute(query)
    r = c.fetchall()
    result = [[0 for x in range(len(r[0]))]for y in range(len(r))]
    for i in range(len(r)):
        result[i][0] = r[i][1]
        result[i][1] = r[i][2]
    db.commit()
    db.close()

    return result




