from utils.process import readjson
config = readjson('config.json')

def isDev(ctx):
    return ctx.message.author.id in config.devs