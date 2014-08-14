#-------------------------------------------------------------------------------
# Name:        reporter
# Purpose:     reporter module to post to api
#
# Author:      a

# Licence:     MIT
#-------------------------------------------------------------------------------
import requests0 as requests #using old requests-transition package to avoid error
from requests0.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
import sys
import json

def main():
    #change verifiy to True if using valid certs
    #opens a session so we have the same token for our two requests
    client = requests.session(config={'verbose': sys.stderr}, verify=False, \
            auth=('user', 'pw'))
    csrftoken = getcsrftoken(client) #get session token
    payload = {'tag': 'tag1', 'reader': 'gone'} #information to upsert
    payload.update(csrftoken) #append csrftoken dictionary to payload
    #post the payload to the api
    r = client.post("https://localhost:5000/reportwrite", data=payload, \
    verify=False) #make True for production use with valid certs
    #print(r.text)

def getcsrftoken(client):
    #retrieve page content
    soup = BeautifulSoup(client.get('https://localhost:5000').content)
    #parse page content for CSRF token
    csrftoken = soup.find("input", {"name": "_csrf_token"})["value"]
    tokendict = {} #create empty dictionary
    tokendict["_csrf_token"] = csrftoken #add token to dictionary
    return tokendict


if __name__ == '__main__':
    main()
