from pymongo import MongoClient
from pymjq import JobQueue
client = MongoClient("localhost", 27017)
db = client.job_queue
jobqueue = JobQueue(db)
jobqueue.valid():