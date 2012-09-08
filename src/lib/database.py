# -*- coding: utf8 -*-

import os, sqlite3

dbfile = os.path.expanduser('~/.config/qtdenter/data.sqlite')

def createDB():
    db = sqlite3.connect(dbfile)
    db.execute('''CREATE TABLE "posts" ("id" INTEGER PRIMARY KEY AUTOINCREMENT, "recordid" INTEGER UNIQUE, "name" VARCHAR, "timestamp" VARCHAR, "text" VARCHAR, "favorited" VARCHAR, "source" VARCHAR, "reply_to_user" VARCHAR, "reply_to_user_id" VARCHAR, "unread" VARCHAR)''')
    db.execute('''CREATE TABLE "mentions" ("id" INTEGER PRIMARY KEY AUTOINCREMENT, "recordid" INTEGER UNIQUE, "name" VARCHAR, "timestamp" VARCHAR, "text" VARCHAR, "favorited" VARCHAR, "source" VARCHAR, "reply_to_user" VARCHAR, "reply_to_user_id" VARCHAR, "unread" VARCHAR)''')
    db.execute('''CREATE TABLE "users" ("id" INTEGER PRIMARY KEY AUTOINCREMENT, "username" VARCHAR UNIQUE, "description" VARCHAR, "profile_link" VARCHAR, "register_date" VARCHAR, "posted_statuses" VARCHAR, "avatar_link" VARCHAR, "site" VARCHAR, "following" VARCHAR, "blocked" VARCHAR)''')
    db.close()

def loadAllPosts():
    result = []
    db = sqlite3.connect(dbfile)
    queryResult = db.execute('''SELECT * FROM posts''')
    for item in queryResult:
        result.append(item)
    db.close()
    return result

def loadAllMentions():
    result = []
    db = sqlite3.connect(dbfile)
    queryResult = db.execute('''SELECT * FROM mentions''')
    for item in queryResult:
        result.append(item)
    db.close()
    return result

def addData(postdata, userdata):
    db = sqlite3.connect(dbfile)
    try:
        db.execute('''INSERT INTO "posts" VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, NULL)''', (postdata[0], postdata[1], postdata[2], postdata[3], postdata[4], postdata[5], postdata[6], postdata[7]))
        db.commit()
        status = 0
    except:
        status = 1

    try:
        db.execute('''INSERT INTO "users" VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (userdata[0], userdata[1], userdata[2], userdata[3], userdata[4], userdata[5], userdata[6], userdata[7], userdata[8]))
        db.commit()
    except:
        print "User", userdata[0], "already in database."

    db.close()

    if status == 0:
        return 0
    else:
        return 1

def addMentionData(postdata, userdata):
    db = sqlite3.connect(dbfile)
    try:
        db.execute('''INSERT INTO "mentions" VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, NULL)''', (postdata[0], postdata[1], postdata[2], postdata[3], postdata[4], postdata[5], postdata[6], postdata[7]))
        db.commit()
        status = 0
    except:
        status = 1

    try:
        db.execute('''INSERT INTO "users" VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (userdata[0], userdata[1], userdata[2], userdata[3], userdata[4], userdata[5], userdata[6], userdata[7], userdata[8]))
        db.commit()
    except:
        print "User", userdata[0], "already in database."

    db.close()

    if status == 0:
        return 0
    else:
        return 1

def setPostUnreadStatus(postid):
    db = sqlite3.connect(dbfile)
    db.execute('UPDATE "posts" SET unread="1" WHERE recordid="' + str(postid) + '"')
    db.commit()
    db.close()

def setPostReadStatus(postid):
    db = sqlite3.connect(dbfile)
    db.execute('UPDATE "posts" SET unread="0" WHERE recordid="' + str(postid) + '"')
    db.commit()
    db.close()

def loadUser(username):
    userdata = []
    db = sqlite3.connect(dbfile)
    queryResult = db.execute("SELECT * FROM users WHERE username='"+ username + "'")
    userdata = queryResult.fetchone()
    db.close()
    return userdata

def deleteAllPosts():
    db = sqlite3.connect(dbfile)
    db.execute("DELETE FROM posts")
    db.commit()
    db.close()
