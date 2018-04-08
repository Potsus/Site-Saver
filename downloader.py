from subprocess import call
from s3 import s3Connect
from db import hashUrl

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