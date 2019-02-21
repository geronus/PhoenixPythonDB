#!/usr/bin/env python

# [START imports]
import os
import urllib
import json
import hashlib
import Utilities
import logging

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

GUILD_SECRET = '1596210'
# [END imports]



def try_key(member_id):
    try:
        candidate_key = ndb.Key('Member', member_id)
    except:
        logging.error("Error retrieving Member from store: " + str(member_id))
        return None

    return candidate_key

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
            #Attempt to fetch this member from the DB
            candidate_key = try_key(member['id'])
            entry = candidate_key.get()

            #If member is in the database, update
            if entry is not None:

                entry.username = member['username']
                entry.active = True
                entry.level = int(member['level'])
                entry.kills = int(member['kills']['kills'])
                entry.xp = int(member['donations']['exp_donated'])
                entry.food = int(member['donations']['food'])
                entry.stone = int(member['donations']['stone'])
                entry.iron = int(member['donations']['iron'])
                entry.lumber = int(member['donations']['lumber'])
                entry.gems = int(member['donations']['gems'])
                entry.money = int(member['donations']['money'])
                entry.jade = int(member['donations']['jade'])
                entry.double = int(member['donations']['double'])
                entry.gdp = int(member['gdp']['dp'])
                entry.gdp_spent = int(member['gdp']['dp_spent'])
                entry.weekly_gdp = int(member['gdp']['weekly_dp'])
                entry.last_weekly_gdp = int(member['gdp']['last_weekly_dp'])
                entry.rp = int(member['rp']['donated'])

                #Update the database
                entry.put()

                #Get display values
                member['kills7'] = sum(entry.kill_list[23:])
                member['kills14'] = sum(entry.kill_list[16:])
                member['kills30'] = sum(entry.kill_list)

            member['donations']['money'] = Utilities.money_external(member['donations']['money'])

    	#Write return
        template = JINJA_ENVIRONMENT.get_template('gtable.html')
        self.response.write(template.render(data=result))

# [END guild_table]

# [START app]
app = webapp2.WSGIApplication([
    ('/', GuildTable),
    ('/gtable', GuildTable)
], debug=True)
# [END app]
