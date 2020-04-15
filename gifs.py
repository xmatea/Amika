import random
import utils.database as db

def getGif(args):
    length = db.tableLen(args)
    r= random.randint(0, length-1)
    return db.getGif(r, args)["url"]
