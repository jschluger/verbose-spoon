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

def updateFullName(username, name):
    f = "database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops

    p = 'SELECT EXISTS(SELECT fullName FROM users WHERE username = "%s" LIMIT 1)'%(username)
    c.execute(p)
    if (c.fetchone()[0] == 0):
        oldName = "you had no previous name!"
    else:
        p = 'SELECT fullName FROM users WHERE username == "%s" '%(username)
        c.execute(p)
        oldName = c.fetchone()[0]

    p = 'UPDATE stocks SET fullName = "%s" WHERE username == "%s"'%(name, username)
    c.execute(p)

    db.commit()
    db.close()
    return oldName

def updateDob(username,birth):
    f = "database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops
    
    p = 'SELECT EXISTS(SELECT dob FROM users WHERE username = "%s" LIMIT 1)'%(username)
    c.execute(p)
    if (c.fetchone()[0] == 0):
        oldDob = "you had no previous birthdate!"
    else:
        p = 'SELECT dob FROM users WHERE username == "%s" '%(username)
        c.execute(p)
        oldDob = c.fetchone()[0]

    p = 'UPDATE stocks SET dob = %d WHERE username == "%s"'%(birth, username)
    c.execute(p)

    db.commit()
    db.close()
    return oldDob

def updateFav(username,stock):
    f = "database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops

    p = 'SELECT EXISTS(SELECT favStock FROM users WHERE username = "%s" LIMIT 1)'%(username)
    c.execute(p)
    if (c.fetchone()[0] == 0):
        oldFav = "you had no previous name!"
    else:
        p = 'SELECT favStock FROM users WHERE username == "%s" '%(username)
        c.execute(p)
        oldFav = c.fetchone()[0]

    p = 'UPDATE stocks SET favStock = "%s" WHERE username == "%s"'%(stock, username)
    c.execute(p)

    db.commit()
    db.close()
    return oldFav
