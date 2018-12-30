#!/usr/bin/env python

# [START imports]
import os
import urllib
import json
import hashlib
import Utilities
import database

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
        for member in result['members']:
            candidate_key = tryKey(member['id'])

            #If member not found, create a new one
            if candidate_key == None:
                candidate_key = Member(id=member['id'],
                                       username=member['username'],
                                       level=member['level'],
                                       kills=member['kills']['kills'],
                                       xp=member['donation']['exp_donated'],
                                       food=member['donations']['food'],
                                       stone=member['donations']['stone'],
                                       iron=member['donations']['iron'],
                                       lumber=member['donations']['lumber'],
                                       gems=member['donations']['gems'],
                                       money=member['donations']['money'],
                                       jade=member['donations']['jade'],
                                       double=member['donations']['double'],
                                       gdp=member['gdp']['dp'],
                                       gdp_spent=member['gdp']['dp_spent'],
                                       weekly_gdp=member['gdp']['weekly_dp'],
                                       last_weekly_gdp=member['gdp']['last_weekly_dp'],
                                       rp=member['rp']['donated'])

            #Otherwise, retrieve and update the existing entry
            else:
                entry = candidate_key.get()
                entry.username = member['username']
                entry.level = member['level']
                entry.kills = member['kills']['kills']
                enrey.xp = member['donation']['exp_donated']
                entry.food = member['donations']['food']
                entry.stone = member['donations']['stone']
                entry.iron = member['donations']['iron']
                entry.lumber = member['donations']['lumber']
                entry.gems = member['donations']['gems']
                entry.money = member['donations']['money']
                entry.jade = member['donations']['jade']
                entry.double = member['donations']['double']
                entry.gdp = member['gdp']['dp']
                entry.gdp_spent = member['gdp']['dp_spent']
                entry.weekly_gdp = member['gdp']['weekly_dp']
                entry.last_weekly_gdp = member['gdp']['last_weekly_dp']
                entry.rp = member['rp']['donated']

            #Update the database entry
            candidate_key.put()

    	#Normalize values
    	for member in result['members']:
    		member['donations']['money'] = Utilities.money_external(member['donations']['money'])

    	#Write return
        template = JINJA_ENVIRONMENT.get_template('gtable.html')
        self.response.write(template.render(data=result))

# [END guild_table]

# [START app]
app = webapp2.WSGIApplication([
    ('/', GuildTable),
], debug=True)
# [END app]
