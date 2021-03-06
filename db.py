from pymongo import MongoClient
from config import MONGO_HOST, MONGO_PORT, MONGO_DB

client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client[MONGO_DB]

blacklist = db.blacklist
queue = db.queue
sites = db.sites

from time import time as now

#### custom json encoder ####
from bson.objectid import ObjectId
from bson.json_util import loads, dumps, RELAXED_JSON_OPTIONS
from flask import Response

def jsonify(*args, **kwargs):
    ### jsonify with support for MongoDB ObjectId
    # return make_response(dumps(*args, json_options=RELAXED_JSON_OPTIONS))
    return Response(dumps(*args, json_options=RELAXED_JSON_OPTIONS), mimetype='application/json')



import hashlib
def hashUrl(url):
    return hashlib.md5(url.encode('utf-8')).hexdigest()



def isBlacklisted(url):
    urlHash = hashUrl(url)
    return blacklist.find({'site': urlHash}).count() != 0

def addToQueue(siteId):
    pass

def findOrAddSite(url):
    if siteExists(url):
        pass
    else:
        addSite(url)
    return getSite(url)

def addSite(url):
    site = {
        'url': url,
        'hash': hashUrl(url),
        'firstAdded': now(),
        'copied': False,
        'start': None,
        'end': None,
        'time': None,
        's3url': None,
        'error': False,
        'message': ''
    }
    return sites.insert_one(site).inserted_id

def updateSite(site):
    oid = site.get('_id')
    if oid != None:
        return sites.update_one({'_id':oid}, {'$set': site}, upsert=False).raw_result

def findSite(url):
    if siteExists(url):
        return getSite(url)
    else:
        return None

def getSite(url):
    return sites.find_one({'hash': hashUrl(url)})

def siteExists(url):
    return sites.find({'hash': hashUrl(url)}).count() != 0