import time
import sqlite3   #enable control of an sqlite database

#adds entry into db for when a user creates a new story
def createStory(title, newEntry, username):
    f = "database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops

    origTime = time.time()
    fullStory = newEntry
    lastEdit = fullStory
    getLatestID = "SELECT storyId FROM stories"
    c.execute(getLatestID)
    l = c.fetchall()
    if l: #if list not empty, there are stories already
        storyId = max(l)[0]+1
    else:
        storyId = 0
    p = """INSERT INTO stories VALUES ("%s","%s","%s", %d, %d, %d)""" %(title, fullStory, lastEdit, origTime, origTime, storyId)
    c.execute(p)
    userId = getUserId(username)
    p = """INSERT INTO edit_logs VALUES (%d,%d,%d)""" %(userId,storyId,origTime)
    c.execute(p)
    db.commit()
    db.close()
    return 1

#return the userId from the username
def getUserId(username):
    f = "database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops

    getId = """SELECT userId FROM users WHERE username == "%s" """ % (username)
    c.execute(getId)

    ans = c.fetchone()[0]

    db.commit()
    db.close()
    return ans

#returns whole story of story whose storyId was given
def getWholeStory(storyId):
    f = "database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops

    p = """SELECT fullStory FROM stories WHERE storyId == %s""" %(storyId)
    c.execute(p)

    ans = c.fetchone()
    db.commit()
    db.close()
    return ans

#returns all necessary components to edit a story
def getEditStats(storyId):
    f = "database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops

    p = """SELECT title, lastEdit FROM stories WHERE storyId == %s""" %(storyId)
    c.execute(p)

    stats = c.fetchone()
    
    db.commit()
    db.close()
    
    ans = []
    ans.append( stats[0] ) #title
    ans.append( stats[1] ) #lastEdit
    ans.append( storyId ) #storyId
    return ans

#update the full story, last edit, and latest time
#connect story submission with user
def updateStory(storyId, newEdit, userId):
    f = "database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops

    #save the edit into the db...
    p = """UPDATE stories SET lastEdit = "%s" WHERE storyId == %d"""%(newEdit, storyId)
    c.execute(p)

    #concatenate the edit to the story...
    wholeStory = getWholeStory(storyId)[0]
    wholeStory += " " + newEdit
    p = """UPDATE stories SET fullStory = "%s" WHERE storyId == %d"""%(wholeStory, storyId)
    c.execute(p)

    #update the time stamp...
    nowTime = time.time()
    p = """UPDATE stories SET latestTime = %d WHERE storyId == %d"""%(nowTime,storyId)
    c.execute(p)
    
    #log the edit in the edit_logs so user cannot edit this story again
    p = """INSERT INTO edit_logs VALUES(%d,%d,%d)""" %(userId, storyId,nowTime)
    c.execute(p)
    
    db.commit()
    db.close()
    
#takes a 2D list, where each sublist has an integer at sublist[index]
#this integer is the timestamp in epoch time
#converts this int to datetime in YYYY-MM-DD- HH:MM:SS format
def convertTimeStamps(twoDList, index):
    for lis in twoDList:
        lis[index] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime( int(lis[index])))
    return twoDList

#helper fxn for sorting a 2d list
def numerize(item):
    return item[1]#returns second entry

def alphabetize(item):
    return item[0].lower()

#return list of stories the user has edited
#sorted by time of edit or title as dictated by flag
#  flag == 0 -> time of last edit; flag == 1 -> title
def doneStories(username, flag):
    f = "database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops

    #pull storyId of every story the user has edited
    userId = getUserId(username)
    p = """SELECT storyId,time FROM edit_logs WHERE userId == %d"""%(userId)
    c.execute(p)
    totalTuple = c.fetchall()

    finalList = []

    for story in totalTuple:
        p = """SELECT title,latestTime,fullStory FROM stories WHERE storyId == %d"""%(story[0])
        c.execute(p)
        totes = c.fetchall()
        theWhole = []
        for i in totes:
            theWhole.append(list(i))
        finalList.append(theWhole[0])
    if flag == 0:
        finalList = sorted(finalList, key=numerize, reverse=True) #sort stories by time of edit
    else:
        finalList = sorted(finalList, key=alphabetize) #sort stories by time of edit
    finalList = convertTimeStamps(finalList, 1)

    db.commit()
    db.close()
  
    return finalList


#return list of stories the user has not edited
#sorted by time of edit or title as dictated by flag
#  flag == 0 -> time of last edit; flag == 1 -> title
def undoneStories(username, flag):
    f = "database.db"
    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor()    #facilitate db ops

    userId = getUserId(username)
    p = """SELECT storyId FROM edit_logs WHERE userId == %d"""%(userId)
    c.execute(p)
    badOne = c.fetchall()

    p = """SELECT storyId FROM stories"""
    c.execute(p)
    allOne = c.fetchall()
    theIds = []
    alreadyCompleted = False
    for one in allOne:
        for storyId in badOne:
            if one[0] == storyId[0]:
                alreadyCompleted = True
        if not alreadyCompleted:
            theIds.append(one)
        alreadyCompleted = False
    finalList = []
    for story in theIds:
        p = """SELECT title,latestTime,lastEdit,storyId FROM stories WHERE storyId == %d"""%(story[0])
        c.execute(p)
        totes = c.fetchall()
        theWhole = []
        for i in totes:
            theWhole.append(list(i))
        finalList.append(theWhole[0])
    if flag == 0:
        finalList = sorted(finalList, key=numerize, reverse=True)
    else:
        finalList = sorted(finalList, key=alphabetize)
    finalList = convertTimeStamps(finalList, 1)

    db.commit()
    db.close()
    
    return finalList



