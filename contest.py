#!/usr/bin/env python

# [START imports]
import os
import urllib
import json
import Utilities
import datetime
import logging

from google.appengine.api import urlfetch
from google.appengine.ext import ndb
from database import Member
from database import Contest
from database import ContestScore

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('./html/'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

GUILD_SECRET = '1596210'

# [END imports]

# [START contest_table]
class ContestPublic(webapp2.RequestHandler):

    def get(self):

        #Execute initial active query and retrieve active contests
        active = Contest.query(Contest.active == True).order(Contest.end).fetch()

        #Form URL for score update
        url = 'https://lyrania.co.uk/api/guilds/member_list.php?'
        params = {'api_code': GUILD_SECRET}
        encoded_params = urllib.urlencode(params)
        url = url + encoded_params

        #Fetch request and format response
        response= urlfetch.fetch(url=url, validate_certificate=True)
        result = json.loads(response.content)
            
        #Update contest scores
        #Note to self - find a way to do this that's not roughly O(n^3) if possible...
        for contest in active:

            for score in contest.scores:

                for person in result['members']:

                    if person['id'] == score.member_id:
                        score.current_gdp = int(person['gdp']['dp'])
                        score.member_name = person['username']
                        break

            contest.put()

        #The Lyr server runs in London timezone (which has daylight time), but all dates in the store are UTC, which does not.
        today = Utilities.todayUTC()

        #Refresh active query to get updated score values
        active = Contest.query(Contest.active == True).order(Contest.end).fetch()

        #Execute recent query
        recent = Contest.query(Contest.end < today).order(-Contest.end).fetch(5)

        #Excute upcoming query
        upcoming = Contest.query(Contest.start > today).order(Contest.start).fetch()

        #If the user clicked on a specific contest name, the contest id will be in the request
        query = self.request.get('id')
        
        if query != '':
            try:
                candidate_key = ndb.Key(urlsafe=query)
            except:
                candidate_key = None
                debug.error("Unable to retrieve Contest key from GET request!")
        else:
            candidate_key = None

        #If no contest was selected, determine which contest should be the default
        if candidate_key is not None:
            current = candidate_key.get()
        elif active != []:
            current = active[0]
        elif recent != []:
            current = recent[0]
        else:
            current = None
            current_dict = {}
            scores = []

        #Format results for the template
        active_list = []
        recent_list = []

        for item in active:
                
            item_dict = {'id': item.key.urlsafe(),
                         'name': item.name,
                         'start': item.start.strftime('%d-%m-%Y'),
                         'end': item.end.strftime('%d-%m-%Y')}

            active_list = active_list + [item_dict]

        for recent_item in recent:

            recent_item_dict = {'id': recent_item.key.urlsafe(),
                                'name': recent_item.name,
                                'start': recent_item.start.strftime('%d-%m-%Y'),
                                'end': recent_item.end.strftime('%d-%m-%Y')}

            recent_list = recent_list + [recent_item_dict]

        if current is not None:

            scores = current.scores

            current_dict = {'id': current.key.urlsafe(),
                            'name': current.name,
                            'start': current.start.strftime('%d-%m-%Y'),
                            'end': current.end.strftime('%d-%m-%Y')}

        #Write return
        template = JINJA_ENVIRONMENT.get_template('contest.html')
        self.response.write(template.render(active_contests=active_list,
                                            upcoming_contests=upcoming,
                                            recent_contests=recent_list,
                                            current=current_dict,
                                            scores=scores))

# [END contest_table]


# [START app]
app = webapp2.WSGIApplication([
    ('/contest', ContestPublic)
], debug=True)
# [END app]
