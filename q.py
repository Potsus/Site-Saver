from redis import Redis
from rq import Queue


q = Queue(connection=Redis())

from downloader import processSiteRequest
result = q.enqueue(processSiteRequest, 'apotts.me')
print(result)
result2 = q.enqueue(processSiteRequest, 'spoitchloefresh.com')
print(result2)