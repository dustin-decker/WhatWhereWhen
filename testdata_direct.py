#-------------------------------------------------------------------------------
# Name:        test data
# Purpose:     This inserts a bunch of documents using the api
#
# Author:      a

# Licence:     MIT
#-------------------------------------------------------------------------------
from pymongo import MongoClient
import datetime

#MongoDB settings
def connect():
    connection = MongoClient("localhost",27017)
    handle = connection["apitest1"]
    handle.authenticate("user","pw")
    return handle
handle = connect()

def report():

    count=0

    while count < 501:
        postitreport(count)
        count = count + 1
        print count

def postitreport(count):
    blank=""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    tagid = 'tag'+str(count)
    locationid = 'location'+str(count)
    assetid = 'asset'+str(count)
    payload = {'assetid': assetid, 'tagid': tagid, 'locationid': locationid, \
                'timestamp': timestamp, \
                'timestamp2': blank, \
                'timestamp3': blank, \
                'timestamp4': blank, \
                'timestamp5': blank, \
                'location2': blank, \
                'location3': blank, \
                'location4': blank, \
                'location5': blank
                }
    upsert = handle.trackingdb.insert(payload)



if __name__ == '__main__':
    report()
