#-------------------------------------------------------------------------------
# Name:        api
# Purpose:     api for asset tracking
#
# Author:      a

# Licence:     MIT
#-------------------------------------------------------------------------------
from flask import Flask, render_template, request, redirect, session, abort, \
                    _request_ctx_stack
from flask.ext.basicauth import BasicAuth
from flask.ext.navigation import Navigation
from flask_limiter import Limiter
import os
from pymongo import MongoClient
from OpenSSL import SSL
import random
import string
import datetime

#MongoDB settings
def connect():
    connection = MongoClient("localhost",27017)
    handle = connection["apitest1"]
    handle.authenticate("user","pw")
    return handle
handle = connect()

app = Flask(__name__)
app.secret_key = os.urandom(24)
nav = Navigation(app)
limiter = Limiter(app)

#SOME SECURITY

#for CSRF attacks
@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = \
        ''.join(random.choice(string.ascii_uppercase + string.digits) \
        for _ in range(24))
    return session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token

#for Clickjacking and some other stuff
@app.after_request
def frame_buster(response):
    ctx = _request_ctx_stack.top
    headers = response.headers
    #prevent clickjacking
    headers['X-Frame-Options'] = 'DENY'
    #forces XSS filter built into recent web browsers
    headers['X-XSS-Protection'] = '1'
    return response

#for SSL
context = SSL.Context(SSL.SSLv23_METHOD)
context.use_privatekey_file('ast.key')
context.use_certificate_file('ast.crt')

#some basic authentication
app.config['BASIC_AUTH_USERNAME'] = 'user'
app.config['BASIC_AUTH_PASSWORD'] = 'pw'
basic_auth = BasicAuth(app)

#MAIN ROUTES
navbar_top = nav.Bar('top', [
    nav.Item('Index', 'index'),
    nav.Item('Upsert', 'upsert'),
    nav.Item('Find', 'find'),
    nav.Item('Report', 'report'),
])

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/upsert", methods=['GET'])
@basic_auth.required
@limiter.limit("100/hour")
def upsert():
    userinputs = [x for x in handle.trackingdb.find().sort("_id",-1).limit(25)]
    return render_template('upsert.html', userinputs=userinputs)

@app.route("/find", methods=['GET'])
def find():
    return render_template('find.html')

@app.route("/report", methods=['GET'])
@basic_auth.required
def report():
    userinputs = [x for x in handle.trackingdb.find().sort("_id",-1).limit(25)]
    return render_template('report.html', userinputs=userinputs)

@app.route("/findassetread", methods=['POST'])
@limiter.limit("75/hour")
def findassetread():
    form1 = {
            "assetid": request.form.get("asset")
            }
    queries = handle.trackingdb.find(form1)
    return render_template('find.html', queries=queries)

@app.route("/findtagread", methods=['POST'])
@limiter.limit("75/hour")
def findtagread():
    form1 = {
            "tagid": request.form.get("tag")
            }
    queries = handle.trackingdb.find(form1)
    return render_template('find.html', queries=queries)

@app.route("/findreaderread", methods=['POST'])
@limiter.limit("75/hour")
def findreaderread():
    form1 = {
            "locationid": request.form.get("location")
            }
    queries = handle.trackingdb.find(form1)
    return render_template('find.html', queries=queries)

#WRITE FUNCTIONS
@app.route("/upsertwrite", methods=['POST'])
@basic_auth.required
def upsertwrite():
    """New record function"""
    blank = ""
    fields = {"tagid": request.form.get("tag"), \
            #create empty keys from the hidden value in the form:
            "locationid": blank,\
            "locationid2": blank,\
            "locationid3": blank,\
            "locationid4": blank,\
            "locationid5": blank,\
            "timestamp": blank,\
            "timestamp2": blank,\
            "timestamp3": blank,\
            "timestamp4": blank,\
            "timestamp5": blank,\
            }

    query = {"assetid": request.form.get("asset")}
    #upsert the new record
    assetid = handle.trackingdb.update(query,{"$set": fields},**{'upsert':True})
    return redirect ("/upsert")

@app.route("/reportwrite", methods=['POST'])
@basic_auth.required
def reportwrite():
    """Location reporting function"""
    location = request.form.get('location')
    query = {"tagid": request.form.get('tag')}
    #get document as dictionary:
    retrieve = handle.trackingdb.find_one(query)
    #get the current date and time
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    def replace_value(key_to_find, value):
        """replaces value of specified key in a dict"""
        for key in retrieve.keys():
            if key == key_to_find:
                retrieve[key] = value

    #if the location has changed...:
    try:
        if location != retrieve.get("locationid", ""):
            #shift all of the key values and insert the new one
            replace_value("locationid5", retrieve.get("locationid4", ""))
            replace_value("locationid4", retrieve.get("locationid3", ""))
            replace_value("locationid3", retrieve.get("locationid2", ""))
            replace_value("locationid2", retrieve.get("locationid", ""))
            replace_value("locationid", location)
            replace_value("timestamp5", retrieve.get("timestamp4", ""))
            replace_value("timestamp4", retrieve.get("timestamp3", ""))
            replace_value("timestamp3", retrieve.get("timestamp2", ""))
            replace_value("timestamp2", retrieve.get("timestamp", ""))
            replace_value("timestamp", timestamp)
            objid = retrieve.pop("_id", None)
            #update the document
            assetid = handle.trackingdb.update({'_id':objid},{"$set": retrieve},\
                        **{'upsert':True})
    except:
        return redirect ("/report")

    return redirect ("/report")


#this is a development feature, it will not be on a production server
#this is vulnerable to CSRF
@app.route("/deleteall", methods=['GET'])
@basic_auth.required
def deleteall():
    handle.trackingdb.remove()
    return redirect ("/")

# Remove the "debug=True" for production
if __name__ == '__main__':
    #app.run(debug=True,port=5000,ssl_context=context,host= 'localhost')
    app.run(debug=False,port=5000,ssl_context=context,host= '0.0.0.0')