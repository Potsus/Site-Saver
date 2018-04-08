from pymongo import MongoClient
from config import MONGO_HOST, MONGO_PORT, MONGO_DB

client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client[MONGO_DB]


#### custom json encoder ####
from bson.objectid import ObjectId
from bson.json_util import loads, dumps, RELAXED_JSON_OPTIONS
from flask import Response

def jsonify(*args, **kwargs):
    ### jsonify with support for MongoDB ObjectId
    # return make_response(dumps(*args, json_options=RELAXED_JSON_OPTIONS))
    return Response(dumps(*args, json_options=RELAXED_JSON_OPTIONS), mimetype='application/json')