#-------------------------------------------------------------------------------
# Name:        reporter
# Purpose:     reporter module to post to api
#
# Author:      a

# Licence:     MIT
#-------------------------------------------------------------------------------
import requests

def main():
    payload = {'tag': 'tag5', 'reader': 'shelf5'}
    r = requests.post("https://localhost:5000/reportwrite", data=payload, \
    verify=False) #turn off for production use with valid certs
    #print(r.text)
    print 'done'

if __name__ == '__main__':
    main()
