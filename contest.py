#!/usr/bin/env python

# [START imports]
import os
import urllib
import json
import Utilities
import re
import datetime
import logging

from google.appengine.api import users
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

# [END imports]

# [START stats_table]
class ContestTable(webapp2.RequestHandler):

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

class ContestAdmin(webapp2.RequestHandler):

    #For validating date input and converting it into a Python date object
    def parseDate(self, string_in):

        #Use regular expressions to validate format and specify match groups for the interesting bits, i.e. year, month and day

        #LittleEndian pattern, e.g. DD-MM-YYYY
        matchLittle = re.match(r'([0-3]\d).([01]\d).(\d{4})', string_in)

        #BigEndian pattern, e.g. YYYY-MM-DD
        matchBig = re.match(r'(\d{4}).([01]\d).([0-3]\d)', string_in)

        #Take match groups and use them to generate a Python date object for return; else return None
        try:

            if matchLittle is not None:
                result = datetime.date(int(matchLittle.group(3)), int(matchLittle.group(2)), int(matchLittle.group(1)))
            elif matchBig is not None:
                result = datetime.date(int(matchBig.group(1)), int(matchBig.group(2)), int(matchBig.group(3)))
            else:
                result = None

            return result

        except:
            return None

    #Handle new Contest submission
    def post(self):

        contest_name = self.request.get('contestname')
        start_date = self.parseDate(str(self.request.get('startdate')))
        end_date = self.parseDate(str(self.request.get('enddate')))

        #If dates could not be parsed, return error.
        if start_date is None or end_date is None:
            error_msg = "Error: Invalid date format. Use YYYY-MM-DD or DD-MM-YYYY."

            template = JINJA_ENVIRONMENT.get_template('error.html')
            self.response.write(template.render(error=error_msg))
        #Else proceed with database update.
        else:
            #Get a list of current members. API call unnecessary since baseline GDP won't be calculated until contest starts.
            members = Member.query(Member.active == True).order(Member.username)
            score_list = []

            #Set up a ContestScore entity for each member
            for person in members:
                new_score = ContestScore(member_id=person.key.id(),
                                         member_name=person.username,
                                         start_gdp=0,
                                         current_gdp=0)

                score_list = score_list + [new_score]

            #Create new Contest
            new_contest = Contest(name=contest_name,
                                  start=start_date,
                                  end=end_date,
                                  scores=score_list)

            new_contest.put()
            result = contest_name + " successfully created!"

            template = JINJA_ENVIRONMENT.get_template('contest_admin.html')
            self.response.write(template.render(info=result))

# [START app]
app = webapp2.WSGIApplication([
    ('/contest/admin', ContestAdmin),
    ('/contest/admin/submit_contest', ContestAdmin)
], debug=True)
# [END app]
