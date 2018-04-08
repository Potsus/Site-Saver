from flask import Flask, request, Response
from flask_restful import Resource, Api, reqparse
from flask_pymongo import PyMongo

from flask_cors import CORS

from db import jsonify

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'sitedb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/sitedb'

api = Api(app)
CORS(app, send_wildcard=True, origins=['*'], always_send=True)

mongo = PyMongo(app)

class checkJob(Resource):
    def get(self, site): 
        col = mongo.db[savedsites]
        data = col.find_one({'site': site})

        return jsonify({'data':data})

class makeJob(Resource):
    def post(self, site):
        col = mongo.db[blacklist]
        # data = col.find_one({'site': site})

        return jsonify({'data':data})


api.add_resource(clearBucket, '/clearbucket')

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000)


