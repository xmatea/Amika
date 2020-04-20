import discord
from datetime import datetime
import os

import pymongo
from pymongo.errors import OperationFailure, BulkWriteError, DuplicateKeyError
from dotenv import load_dotenv

load_dotenv()
client = pymongo.MongoClient(os.getenv('MONGODB'))
dev = os.getenv('DEV')

if dev:
    db = client.niatest
else:
    db = client.nia

### models ######
def guildModel(guild):
    return {
            "_id": guild.id, 
            "name": guild.name,
            "owner": guild.owner.id,
            "joined_at": datetime.now().isoformat(),
            "created_at": guild.created_at.isoformat(),
            "config": { "autodelete": [] }
        }

def userModel(user):
    return {
        "_id": user.id,
        "name": user.name,
        "created_at": user.created_at.isoformat(),
        "bal": 0,
        "inventory": []
    }


#### guild operations ####

def insertGuilds(guild):
    try: 
        docs=[]
        for g in guild:
            if not db.guilds.find_one({"_id": g.id}):
                doc = guildModel(g)
                docs.append(doc)
        if len(docs) > 1:
            try:
                return db.guilds.insert_many(docs)
            except BulkWriteError as e:
                    print(f"Write error for guild insert, error: {e}")
        elif len(docs) == 1:
            return db.guilds.insert_one(docs[0])
    except OperationFailure as e:
        print(f"Write error for guild {g}, error: {e}")

def insertGuild(guild):
    try:
        if not db.guilds.find_one({"_id": guild.id}):
            return db.guilds.insert_one(guildModel(guild))
    except OperationFailure as e:
        print(f"Write error for guild {guild}, error: {e}")

def removeGuild(query):
    try:
        return db.guilds.delete_one(query)
    except Exception as e:
        print(f"Delete error: {e}") 

def findGuild(query):
    return db.guilds.find_one(query)

def updateGuild(id, val):
    return db.guilds.update_one({"_id": id}, val)

#### user operations ####
def insertUsers(user):
    try: 
        docs=[]
        for u in user:
            if not db.guilds.find_one({"_id": u.id}):
                doc = userModel(u)
                docs.append(doc)
        if len(docs) > 1:
            try:
                return db.users.insert_many(docs)
            except BulkWriteError as e:
                    print(f"Write error for guild insert, error: {e}")
        elif len(docs) == 1:
            return db.users.insert_one(docs[0])
    except OperationFailure as e:
        print(f"Write error for user {u.id}, error: {e}")

def insertUser(user):
    try:
        if not db.users.find_one({"_id": user.id}):
            return db.users.insert_one(userModel(user))
    except OperationFailure as e:
         print(f"Write error for user insert, error: {e}")

def queryUsers(query):
    return db.users.find_one(query)

def updateUser(query, update, upsert):
    return db.users.update_one(query, update, upsert)

def removeUser(query):
    try:
        return db.users.delete_one(query)
    except Exception as e:
        print(f"Delete error: {e}") 

# gif operations
def insertGif(gif, tag):
    if isinstance(gif, list):
        docs=[]
        for g in gif:
            docs.append({"url": g, "tag": tag})
        return db.gifs.insert_many(docs)
    else:
        return db.gifs.insert_one({"url": gif, "tag": tag})

def randGif(tag):
    doc = db.gifs.aggregate([
        { '$match': { 'tag': tag } },
        {'$sample': { 'size': 1 } }
    ])
    
    doc = list(doc)
    return doc[0]['url']

def getGifs(ids):
    return db.gifs.find_many({"_id": ids})

def getGif(id):
    return db.gifs.find_one({"_id": id})
    
def clonecoll(args):
    if args=='gifs':
        target = client.nia.gifs
    elif args=='members':
        target = client.nia.members
    elif args=='guilds':
        target= client.nia.guilds

    i=0
    for doc in target.find():
        try:
            db.members.insert(doc)
            i+=1
        except DuplicateKeyError:
            pass
    return i