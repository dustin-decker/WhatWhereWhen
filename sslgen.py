#-------------------------------------------------------------------------------
# Name:        sslgen
# Purpose:     generate development ssl certs
#
# Author:      a

# Licence:     MIT
#-------------------------------------------------------------------------------
from werkzeug.serving import run_simple
from werkzeug.serving import make_ssl_devcert
import os
scriptdir = os.path.dirname(os.path.abspath(__file__))



make_ssl_devcert(scriptdir+'\\ast', host='localhost', cn=None)

##app = make_app(...)
##run_simple('localhost', 8080, app, use_reloader=True)