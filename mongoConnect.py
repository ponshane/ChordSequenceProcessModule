from pymongo import MongoClient
from pymongo import errors
import ConfigParser

Config = ConfigParser.ConfigParser()
Config.read("./config.ini")

ACCOUNT = Config.get("MongoInformation","Account")
PW = Config.get("MongoInformation","Password")
IP = Config.get("MongoInformation","IP")
DB = Config.get("MongoInformation","Database")

mongoURI = "mongodb://%s:%s@%s/%s?authMechanism=SCRAM-SHA-1" % (ACCOUNT, PW, IP, DB)
try:
    client = MongoClient(mongoURI)
    print client.server_info()
    db = client.Youtube_Tutorials
except errors.ConnectionFailure as err:
    print err
