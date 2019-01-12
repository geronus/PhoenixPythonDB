#!/usr/bin/env python

# [START imports]
import os
import urllib
import json
import hashlib
import Utilities

from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
from database import Member

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('./html/'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# [END imports]

# [START stats_table]
class StatsTable(webapp2.RequestHandler):

    def get(self):
      
        root_url = 'https://lyrania.co.uk/api/accounts/public_profile.php?'
        memberlist = []

        members = Member.query(Member.active == True).order(Member.username)

        for member in members:

            #Form URL
            params = {'search': str(member.key.id())}
            encoded_params = urllib.urlencode(params)
            url = root_url + encoded_params

            #Fetch request and format response
            response = urlfetch.fetch(url=url, validate_certificate=True)
            result = json.loads(response.content)
            list_addition = [result]
            memberlist = memberlist + list_addition

            #Do stuff with the database HERE
            member.username = result['name']
            member.level = int(result['level'])
            member.quests = int(result['quests_complete'])
            member.base_stats = int(result['base_stats'])
            member.dp = int(result['earned_dp'])

            if result['guild_name'] != 'Phoenix':
                member.active = False
            
            member.put()

        #Write return
        template = JINJA_ENVIRONMENT.get_template('stats.html')
        self.response.write(template.render(data=memberlist))

# [END stats_table]

# [START app]
app = webapp2.WSGIApplication([
    ('/', StatsTable),
    ('/stats', StatsTable)
], debug=True)
# [END app]
