import sqlite3   #enable control of an sqlite database

def buyStock(stockName, shares, price, username):
    f = "database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops

    theMoney = """SELECT funds FROM users WHERE username == "%s" """ % (username)
    c.execute(p)
    money = c.fetchone()[0]
    deduct = price * shares
    newMoney = money - deduct
    p = 'UPDATE users SET funds = %d WHERE username == "%s"'%(newMoney, username
                                                              )
    c.execute(p)

    p = 'SELECT EXISTS(SELECT 1 FROM stocks WHERE username = "%s" AND stockName = "%s" LIMIT 1)'%(username, stockName)
    c.execute(p)
    if (c.fetchone()[0] == 0):
        p = 'INSERT INTO stocks VALUES ("%s","%s",%d)' %(username,stockName,shares)
    else:
        p = 'SELECT shares FROM stocks WHERE username == "%s" AND stockName = "%s"'%(username, stockName)
        c.execute(p)
        newShares = c.fetchone()[0] + shares
        p = 'UPDATE stocks SET shares = %d WHERE username == "%s"'%(newShares, username)
        c.execute(p)

    db.commit()
    db.close()
    
def sellStock(stockName, shares, price, username):
    f = "database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops

    theMoney = """SELECT funds FROM users WHERE username == "%s" """ % (username)
    c.execute(p)
    money = c.fetchone()[0]
    add = price * shares
    newMoney = money + add
    p = 'UPDATE users SET funds = %d WHERE username == "%s"'%(newMoney, username
                                                              )
    c.execute(p) 
    p = 'SELECT shares FROM stocks WHERE username == "%s" AND stockName = "%s"'%(username, stockName)
        c.execute(p)
        newShares = c.fetchone()[0] - shares
        p = 'UPDATE stocks SET shares = %d WHERE username == "%s"'%(newShares, username)
        c.execute(p)

    db.commit()
    db.close()
