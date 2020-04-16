import discord
from tinydb import TinyDB, Query, where
from datetime import datetime
import pymongo
from pymongo.errors import OperationFailure, BulkWriteError, DuplicateKeyError
import os
from dotenv import load_dotenv
load_dotenv()
client = pymongo.MongoClient(os.getenv('MONGODB'))
dev = os.getenv('DEV')

if dev:
    db = client.niatest
else:
    db = client.nia

#### guild operations ####
def insertGuilds(guild):
    try:
        if isinstance(guild, list):
            doclist=[]
            for g in guild:
                if not db.guilds.find_one({"_id": g.id}):
                    doc = {
                        "_id": g.id, 
                        "name": g.name,
                        "owner": g.owner.id,
                        "joined_at": datetime.now().isoformat(),
                        "created_at": g.created_at.isoformat(),
                        "config": { "autodelete": [] }
                    }
                    doclist.append(doc)
            if len(doclist) > 1:
                try:
                    return db.guilds.insert_many(doclist)
                except BulkWriteError as e:
                     print(f"Write error for guild insert, error: {e}")

            elif len(doclist) == 1:
                return db.guilds.insert_one(doclist[0])
            else:
                pass #probably log smt idk
        else: 
            if not db.guilds.find_one({"_id": guild.id}):
                db.guilds.insert_one({
                        "_id": guild.id, 
                        "name": guild.name,
                        "owner": guild.owner.id,
                        "joined_at": datetime.now().isoformat(),
                        "created_at": guild.created_at.isoformat(),
                        "config": { "autodelete": [] }
                    })
    except OperationFailure as e:
        print(f"Write error for guild {g}, error: {e}")

def removeGuild(guild):
    try:
        return db.guilds.delete_one({"_id": guild.id})
    except Exception as e:
        print(f"Delete error for guild {guild}, error: {e}") 

def findGuild(query):
    return db.guilds.find_one(query)

def updateGuild(id, val):
    db.guilds.update_one({"_id": id}, val)

#### member operations ####
def insertMembers(member):
    try:
        if isinstance(member, list):
            doclist=[]
            for m in member:
                if not db.members.find_one({"_id": m.id}):
                    doc = {
                        "_id": m.id,
                        "name": m.name,
                        "created_at": m.created_at.isoformat()
                    }
                    doclist.append(doc)
            if len(doclist) > 1:
                try:
                    return db.members.insert_many(doclist)
                except BulkWriteError as e:
                    print(f"Write error for member insert, error: {e}")

            elif len(doclist) == 1:
                return db.members.insert_one(doclist[0])
            else:
                pass #probably log smt idk
        else:
            if not db.members.find_one({"_id": member.id}):
                db.members.insert_one({
                    "_id": member.id,
                    "name": member.name,
                    "created_at": member.created_at.isoformat()
                })
    except OperationFailure as e:
         print(f"Write error for member insert, error: {e}")

def queryMembers(q1, q2):
    return db.members.find_one({q1: q2})

def removeMember(q1, q2):
    return db.members.delete_one({q1: q2})

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