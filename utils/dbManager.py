import sqlite3   #enable control of an sqlite database

def buyStock(stockName, shares, price, username):
    f = "database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops

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
        return "you don't got enuf money, dude"
    
    db.commit()
    db.close()
    return "transaction complete"
    
def sellStock(stockName, shares, price, username):
    f = "database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops

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
        return "sold!"

    db.commit()
    db.close()
    return "you do not have enough shares of this stock to make this transaction"

    
def enufMoney(username,shares,price):
    f = "database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops

    trying = shares*price
    p = 'SELECT funds FROM users WHERE username == "%s"'%(username)
    c.execute(p)
    return (c.fetchone()[0] > trying)

    db.commit()
    db.close()

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
        print"  it says it's "
        if (truth):
            print "true"
        else:
            print "false"
        return truth
    return False

    db.commit()
    db.close()

def get_owned_stocks(username, **kwargs):
    f - database.db
    db. sqlite3.connect(f)
    c = db.cursor()
    
    if 'symbol' in kwargs:
        query = "SELECT * FROM stocks WHERE username == ? AND stockName == ?"
        c.execute(query, (username, kwargs['symbol'],))
        result = c.fetchall()
        return result

    query = "SELECT * FROM stocks WHERE username == ?"
    c.execute(query, (username,))
    result = c.fetchall()
    return result


'''testing testing 1,2,3'''

sellStock('abc', 20, 100, 'caleb')
'''sellStock('asdf', 80, 100000, 'caleb')'''

