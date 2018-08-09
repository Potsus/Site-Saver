MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'sitedb'
MONGO_URL = 'mongodb://%s:%s/%s' %(MONGO_HOST, MONGO_PORT, MONGO_DB)

S3_BUCKET = 'sitesaver'

BLACKLIST_URL = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'

MAX_RUNTIME = 900