import discord

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('<hi'):
        await message.channel.send('Hello!')

client.run('NjMwMTc5NDMyODQ5NzM1Njgx.Xoe79A.XU3KEklyi-PF2cpeKCb1K63MDqA')