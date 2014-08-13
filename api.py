#-------------------------------------------------------------------------------
# Name:        api
# Purpose:     api for asset tracking
#
# Author:      a

# Licence:     MIT
#-------------------------------------------------------------------------------
from flask import Flask, render_template, request, redirect, session, abort
import os
from pymongo import MongoClient
from OpenSSL import SSL
import random
import string

def connect():
    connection = MongoClient("localhost",27017)
    handle = connection["apitest1"]
    handle.authenticate("user","pw")
    return handle

app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'
handle = connect()

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
        for _ in range(10))
    return session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token

#for SSL
context = SSL.Context(SSL.SSLv23_METHOD)
context.use_privatekey_file('ast.key')
context.use_certificate_file('ast.crt')

#MAIN ROUTES
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/upsert", methods=['GET'])
def upsert():
    userinputs = [x for x in handle.trackingdb.find()]
    return render_template('upsert.html', userinputs=userinputs)

@app.route("/find", methods=['GET'])
def find():
    return render_template('find.html')

@app.route("/report", methods=['GET'])
def report():
    userinputs = [x for x in handle.trackingdb.find()]
    return render_template('report.html', userinputs=userinputs)

@app.route("/findassetread", methods=['POST'])
def findassetread():
    form1 = {
            "assetid": request.form.get("asset")
            }
    queries = handle.trackingdb.find(form1)
    return render_template('find.html', queries=queries)

@app.route("/findtagread", methods=['POST'])
def findtagread():
    form1 = {
            "tagid": request.form.get("tag")
            }
    queries = handle.trackingdb.find(form1)
    return render_template('find.html', queries=queries)

@app.route("/findreaderread", methods=['POST'])
def findreaderread():
    form1 = {
            "readerid": request.form.get("reader")
            }
    queries = handle.trackingdb.find(form1)
    return render_template('find.html', queries=queries)

#WRITE FUNCTIONS
@app.route("/upsertwrite", methods=['POST'])
def upsertwrite():
    tag1 = {"tagid": request.form.get("tag")}
    query = {"assetid": request.form.get("asset")}
    assetid = handle.trackingdb.update(query,{"$set": tag1},**{'upsert':True})
    return redirect ("/upsert")

@app.route("/reportwrite", methods=['POST'])
def reportwrite():
    loc1 = {"readerid": request.form.get('reader')}
    query = {"tagid": request.form.get('tag')}
    assetid = handle.trackingdb.update(query,{"$set": loc1},**{'upsert':True})
    return redirect ("/report")

@app.route("/deleteall", methods=['GET'])
def deleteall():
    handle.trackingdb.remove()
    return redirect ("/")

# Remove the "debug=True" for production
if __name__ == '__main__':
    app.run(host='localhost',debug=True,port=5000,ssl_context=context)