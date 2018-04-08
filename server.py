from flask import Flask, request, Response
from flask_restful import Resource, Api, reqparse
from flask_pymongo import PyMongo

from flask_cors import CORS

from db import jsonify, findSite, findOrAddSite, isBlacklisted
from downloader import runJob

from config import MONGO_URL, MONGO_DB

app = Flask(__name__)
app.config['MONGO_DBNAME'] = MONGO_DB
app.config['MONGO_URI'] = MONGO_URL

api = Api(app)
CORS(app, send_wildcard=True, origins=['*'], always_send=True)

mongo = PyMongo(app)

###### redis stuff #####
from redis import Redis
from rq import Queue

q = Queue(connection=Redis())
########################

class checkSite(Resource):
    def get(self): 
        args = request.args.copy()
        data = None
        if args.get('site') != None:
            data = findSite(args['site'])

        return jsonify({'data':data})

class requestSite(Resource):
    def get(self):
        args = request.args.copy()
        data = None
        if args.get('site') != None:
            url = args['site']
            if isBlacklisted(url):
                data = {'error': 'URL is blacklisted, will not be processed'}
            else:
                data = findOrAddSite(url)
                result = q.enqueue(runJob, url)
        return jsonify({'data': data})

api.add_resource(checkSite, '/getSite')
api.add_resource(requestSite, '/requestSite')

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000)


