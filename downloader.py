from subprocess import call
from s3 import s3Connect

def downloadSite(url):
    s3 = s3Connect()
    url = cleanUrl(url)
    # I should add some stuff to parse robots.txt 
    # and also find a user agent that will let me do this safely
    call(['wget', '-mkEpnp', url])
    call(['zip', '-r', url, url])
    zipfile = '%s.zip' % url
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
    call(['rm', '-f', url])
    call(['rm', '-f', zipfile])
    return dlUrl
