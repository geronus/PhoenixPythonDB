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

GUILD_SECRET = '1596210'
# [END imports]



def try_key(member_id):
    try:
        candidate_key = ndb.Key(member_id)
    except:
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

            #If member not found, create a new one
            if candidate_key == None:
                candidate_key = Member(id=member['id'],
                                       username=member['username'],
                                       rank="0",
                                       active=True,
                                       level=int(member['level']),
                                       kills=int(member['kills']['kills']),
                                       quests=0,
                                       base_stats=0,
                                       buffed_stats=0,
                                       dp=0,
                                       xp=int(member['donations']['exp_donated']),
                                       xp_prev=0,
                                       food=int(member['donations']['food']),
                                       food_prev=0,
                                       stone=int(member['donations']['stone']),
                                       stone_prev=0,
                                       iron=int(member['donations']['iron']),
                                       iron_prev=0,
                                       lumber=int(member['donations']['lumber']),
                                       lumber_prev=0,
                                       gems=int(member['donations']['gems']),
                                       gems_prev=0,
                                       money=int(member['donations']['money']),
                                       money_prev=0,
                                       jade=int(member['donations']['jade']),
                                       jade_prev=0,
                                       double=int(member['donations']['double']),
                                       gdp=int(member['gdp']['dp']),
                                       gdp_prev=0,
                                       gdp_spent=int(member['gdp']['dp_spent']),
                                       gdp_spent_prev=0,
                                       weekly_gdp=int(member['gdp']['weekly_dp']),
                                       last_weekly_gdp=int(member['gdp']['last_weekly_dp']),
                                       rp=int(member['rp']['donated']),
                                       chc=0,
                                       chd=0,
                                       heroism=0,
                                       leadership=0,
                                       archaeology=0,
                                       jc=0,
                                       serendipity="",
                                       epeen=0,
                                       w1=0,
                                       w2=0,
                                       a1=0,
                                       a2=0,
                                       a3=0,
                                       a4=0,
                                       a5=0,
                                       a6=0,
                                       a7=0)

            #Otherwise, update the existing entry
            else:
                entry = candidate_key.get()
                entry.username = member['username']
                entry.active = True
                entry.level = int(member['level'])
                entry.kills = int(member['kills']['kills'])
                enrey.xp = int(member['donations']['exp_donated'])
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
    ('/gtable', GuildTable)
], debug=True)
# [END app]
