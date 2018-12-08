#!/usr/bin/env python

# [START imports]
import os
import urllib
import json
import hashlib

from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('./html/'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

GUILD_SECRET = '1596210'
# [END imports]

# [START guild_table]
class GuildTable(webapp2.RequestHandler):

    def get(self):
    	#Form URL
    	url = 'https://lyrania.co.uk/api/guilds/member_list.php?'
    	params = {'api_code': GUILD_SECRET}
    	encoded_params = urllib.urlencode(params)
    	url = url + encoded_params

    	#Fetch request and format response
    	response= urlfetch.fetch(url=url, validate_certificate=True)
    	result = json.loads(response.content)

    	#Do stuff with the database HERE

    	#Normalize values
    	

    	#Write return
        template = JINJA_ENVIRONMENT.get_template('gtable.html')
        self.response.write(template.render(urlstring=url, data=result))

# [END guild_table]

# [START app]
app = webapp2.WSGIApplication([
    ('/', GuildTable),
], debug=True)
# [END app]
