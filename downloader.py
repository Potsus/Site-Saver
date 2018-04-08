from subprocess import call
from s3 import s3Connect
from db import hashUrl, isBlacklisted, findOrAddSite, updateSite
from time import time as now

def downloadSite(url):
    s3 = s3Connect()
    url = cleanUrl(url)
    # I should add some stuff to parse robots.txt 
    # and also find a user agent that will let me do this safely
    call(['wget', '-mkEpnp', url])
    zipfile = hashUrl(url)
    call(['zip', '-r', zipfile, url])
    zipfile = '%s.zip' % zipfile
    return zipfile



def cleanUrl(url):
    cleanUrl = str(url)
    # I don't know what I need for this yet
    return cleanUrl

def processSiteRequest(url):
    zipfile = downloadSite(url)

    s3 = s3Connect()
    s3.uploadFile(zipfile, zipfile)

    dlUrl = s3.getDownloadUrl(zipfile)
    call(['rm', '-rf', url])
    call(['rm', '-f', zipfile])
    return dlUrl

def runJob(url):
    if isBlacklisted(url):
        return False
    site = findOrAddSite(url)
    site['start'] = now()
    updateSite(site)

    try: 
        dl = processSiteRequest(url)
        site['copied'] = True
        site['s3url'] = dl
        site['error'] = False
        site['end'] = now()
        site['time'] = site['start'] - site['end']
        updateSite(site)
    except Exception as e:
        site['copied'] = False
        site['s3url'] = None
        site['error'] = True
        site['message'] = '%s: %s' % (e, e.__doc__)
        site['end'] = now()
        site['time'] = site['end'] - site['start']
        updateSite(site)
    
    return site
