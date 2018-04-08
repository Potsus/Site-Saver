from pandas import read_csv, DataFrame
from subprocess import call
from db import blacklist, hashUrl
from config import BLACKLIST_URL


print('saving blacklist')
call(['wget', BLACKLIST_URL])

file = BLACKLIST_URL.split('/')[-1]
print('unzipping blacklist')
call(['unzip', file])

csv = file.replace('.zip', '')
print('loading sites from alexa top 1m csv')
topAlexa  = read_csv(csv, header=None, usecols=[0,1], names=['rank', 'url'])
print('loading sites from blacklist csv')
custom = read_csv('blacklist.csv', header=None, usecols=[0,1], names=['rank', 'url'])

# check and make sure I can do lookups
# df[df['url'].str.contains('youtube.com')==True]


print('hashing each url')
hashFrame = DataFrame()
blackFrame = DataFrame()
hashFrame['site'] = topAlexa['url'].apply(hashUrl)
blackFrame['site'] = custom['url'].apply(hashUrl)
print(hashFrame)
print(blackFrame)
hashFrame = hashFrame.append(blackFrame, ignore_index=True)
print(hashFrame)

print('dropping old blacklist')
blacklist.drop()

print('adding sites to blacklist')
blacklist.insert_many(hashFrame.to_dict('records'))

print('cleaning up downloads')
call(['rm', '-f', csv])
call(['rm', '-f', file])