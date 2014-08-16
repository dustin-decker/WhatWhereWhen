#-------------------------------------------------------------------------------
# Name:        test data
# Purpose:     This inserts a bunch of documents using the api
#
# Author:      a

# Licence:     MIT
#-------------------------------------------------------------------------------
import requests0 as requests #using old requests-transition package to avoid error
from requests0.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
import sys
import json

global serverpath
#serverpath = "https://localhost:5000"
serverpath = "https://68.172.220.96:5000"

def report():

    count=1

    while count < 500:
        postitupsert('asset' + str(count), 'tag' + str(count))
        postitreport('tag' + str(count), 'location' + str(count))
        count = count + 1


def postitreport(tag, location):
    #change verifiy to True if using valid certs
    #opens a session so we have the same token for our two requests
    client = requests.session(config={'verbose': sys.stderr}, verify=False, \
            auth=('user', 'pw'))
    csrftoken = getcsrftoken(client) #get session token
    payload = {'tag': tag, 'location': location} #information to upsert
    payload.update(csrftoken) #append csrftoken dictionary to payload
    #post the payload to the api
    r = client.post(serverpath + "/reportwrite", data=payload, \
    verify=False) #make True for production use with valid certs
    #print(r.text)

def postitupsert(asset, tag):
    #change verifiy to True if using valid certs
    #opens a session so we have the same token for our two requests
    client = requests.session(config={'verbose': sys.stderr}, verify=False, \
            auth=('user', 'pw'))
    csrftoken = getcsrftoken(client) #get session token
    payload = {'asset': asset, 'tag': tag} #information to upsert
    payload.update(csrftoken) #append csrftoken dictionary to payload
    #post the payload to the api
    r = client.post(serverpath + "/upsertwrite", data=payload, \
    verify=False) #make True for production use with valid certs
    #print(r.text)

def getcsrftoken(client):
    #retrieve page content
    soup = BeautifulSoup(client.get(serverpath).content)
    #parse page content for CSRF token
    csrftoken = soup.find("input", {"name": "_csrf_token"})["value"]
    tokendict = {} #create empty dictionary
    tokendict["_csrf_token"] = csrftoken #add token to dictionary
    return tokendict


if __name__ == '__main__':
    report()
