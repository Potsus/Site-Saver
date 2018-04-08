from pandas import read_csv
from subprocess import call
from db import db
from config import BLACKLIST_URL

col = db.blacklist

print('saving blacklist')
call(['wget', BLACKLIST_URL])

file = BLACKLIST_URL.split('/')[-1]
print('unzipping blacklist')
call(['unzip', file])

csv = file.replace('.zip', '')
print('loading sites from blacklist csv')
df = read_csv(csv)

print('adding sites to blacklist')
col.insert_many(df.to_dict('records'))

print('cleaning up downloads')
call(['rm -f', csv])
call(['rm -f', file])