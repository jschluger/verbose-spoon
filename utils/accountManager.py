#Manages the account info tables in the db
import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O



''' 
1. authenticate: authenticate credentials
2. register: make sure username not used
'''

from hashlib import sha1

'''testing purposes
p = """INSERT INTO users VALUES("%s","%s",%d)""" %("firstEnrty","hashedpass",0)
c.execute(p)
'''
#authenticate user returns true if authentication worked

def authenticate(user,password):

    f="database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()  #facilitate db ops  <-- I don't really know what that means but ok
    isLogin = False #Default to false; login info correct?
    loginStatusMessage = "" #what's wrong
    messageNumber = 0 #represents what kind of error it is
    passHash = sha1(password).hexdigest()#hash it

    checkUser = 'SELECT * FROM users WHERE username=="%s";' % (user)  #checks if the user is in the database
    c.execute(checkUser)
    l = c.fetchone() #listifies the results
    if l == None:
        isLogin = False
        messageNumber = 0
        loginStatusMessage = "user does not exist"
    elif l[1] == passHash:
        isLogin = True
        messageNumber = 1
        loginStatusMessage = "login info correct"
    else:
        isLogin = False
        messageNumber = 2
        loginStatusMessage = "wrong password"

    db.commit() #save changes
    db.close()  #close database
    return messageNumber

#returns true if register worked
def register(user,password,pwd):    #user-username, password-password, pwd-retype
    f="database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()  #facilitate db ops  <-- I don't really know what that means but ok
    isRegister = False #defualt not work
    registerStatus = ""
    messageNumber = 0 #for message


    checkUser = 'SELECT * FROM users WHERE username=="%s";' % (user)  #checks if the user is in the database
    c.execute(checkUser)
    l = c.fetchone() #listifies the results

    if l != None:
        isRegister = False
        messageNumber = 0
        registerStatus = "username taken"
    elif (password != pwd):
        isRegister = False
        messageNumber = 1
        registerStatus = "passwords do not match"
    elif (password == pwd):
        #get latest id
        getLatestId = "SELECT userId FROM users"
        c.execute(getLatestId)
        l = c.fetchall()
        if l: #if list is not empty, there exists ids to take the max of
            userId = max(l)[0]+1
        else: #first user to register
            userId = 0

        passHash = sha1(password).hexdigest()#hash it
        insertUser = 'INSERT INTO users VALUES ("%s","%s",%d, 100000," ",0," ");' % (user,passHash,userId) #sqlite code for inserting new user

        c.execute(insertUser)

        isRegister = True
        messageNumber = 2
        registerStatus = "user %s registered!" % (user)

    db.commit() #save changes
    db.close()  #close database
    return messageNumber


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

    p = 'UPDATE users SET fullName = "%s" WHERE username == "%s"'%(name, username)
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

    p = 'UPDATE users SET dob = %d WHERE username == "%s"'%(birth, username)
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

    p = 'UPDATE users SET favStock = "%s" WHERE username == "%s"'%(stock, username)
    c.execute(p)

    db.commit()
    db.close()
    return oldFav

def updatePwd(username,pwd):
    f = "database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops
    
    passHash = sha1(pwd).hexdigest()#hash it
    p = 'UPDATE users SET password = "%s" WHERE username == "%s"'%(passHash, username)

    c.execute(p)

    db.commit()
    db.close()
    
register('bayle','michal','michal')
updatePwd('bayle','caleb')
register('caleb','michal','michal')

        
