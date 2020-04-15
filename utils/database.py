import discord
from tinydb import TinyDB, Query, where
from datetime import datetime

guilds = TinyDB('guilds.json')
members = TinyDB('members.json')

gifs = TinyDB('gifs.json')
hug = gifs.table('hug')
kiss = gifs.table('kiss')
slap = gifs.table('slap')
cuddle = gifs.table('cuddle')
blush = gifs.table('pout')

def tableLen(table):
    table = globals()[table]
    return len(table)

def insertGif(gif, table):
    table = globals()[table]
    return table.insert({'url':gif})

def getGif(id, table):
    table = globals()[table]
    return table.get(doc_id=id)

def removeGif(id, table):
    table = globals()[table]
    table.remove(doc_ids=[id])
    
def getGuild(guild):
    return guilds.get(Query().id == guild.id)

def insertGuild(guild):
    if (guilds.search(Query().id == guild.id)):
        return

    guilds.insert({
        "id": guild.id, 
        "name": guild.name,
        "owner": guild.owner.id,
        "joined_at": datetime.now().isoformat(),
        "created_at": guild.created_at.isoformat(),
        "config": {
            "autodelete": 0
        }
    })

def insertMember(member):
    if (members.search(Query().id == member.id)):
        return
    
    members.insert({
        "id": member.id,
        "name": member.name,
        "created_at": member.created_at.isoformat()
    })

def queryGuild(query, val):
    return(guilds.search(query== val))

def upsertGuild(doc, query, val):
    guilds.update(doc, query == val)


