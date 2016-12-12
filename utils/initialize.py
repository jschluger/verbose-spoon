#!/usr/bin/python
'''
block comment describing the contents of this file
'''
import sqlite3   #enable control of an sqlite database
import os

keyFile = open("utils/key", "w")
keyFile.write(os.urandom(32))
keyFile.close()

f = "database.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

#------------------------create tables---------------------------------------
q = "CREATE TABLE users (username TEXT, password TEXT, userId INTEGER, funds FLOAT, fullName TEXT, dob INTEGER, favStock TEXT)"
c.execute(q)

print "g"
q="CREATE TABLE stocks (username TEXT, stockName TEXT, shares INTEGER)"
c.execute(q)
print "g"

db.commit()
db.close()
