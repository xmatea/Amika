import discord
from tinydb import TinyDB, Query
from datetime import datetime

guilds = TinyDB('guilds.json')
members = TinyDB('members.json')

def insert_guild(guild):
    if (guilds.search(Query().id == guild.id)):
        return

    guilds.insert({
        "id": guild.id, 
        "name": guild.name,
        "owner": guild.owner.id,
        "joined_at": datetime.now().isoformat(),
        "created_at": guild.created_at.isoformat()       
    })


def insert_member(member):
    if (members.search(Query().id == member.id)):
        return

    members.insert({
        "id": member.id,
        "name": member.name,
        "created_at": member.created_at.isoformat()
    })
