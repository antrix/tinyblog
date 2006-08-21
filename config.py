import os
import web

# Data file
yaml_file = 'tb.yml'
# Entries to display per page
per_page = 20
# Cache templates
cache = True
# Default webpy middleware list
middleware = []
#middleware = [web.reloader]
# Use debug error pages
web.webapi.internalerror = web.debugerror
# Workaround webpy fcgi bug
#web.wsgi.runwsgi = lambda func: web.wsgi.runfcgi(func, addr=None)
