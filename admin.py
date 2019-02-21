#!/usr/bin/env python

# [START imports]
import os
import urllib
import json
import Utilities
import datetime
import logging
import re

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

RANKS = [1000,2000,3000,4000,5000,
         7500,10000,12500,15000,20000,
         25000,30000,35000,40000,50000,
         60000,70000,80000,90000,100000,
         120000,140000,160000,180000,200000,
         220000,240000,260000,280000,300000,
         320000,340000,360000,380000,400000,
         420000,440000,460000,480000,500000,
         525000,550000,575000,600000,625000,
         650000,675000,700000,725000,750000,
         775000,800000,825000,850000,875000,
         900000,925000,950000,975000,1000000]

# [START admin]

class Admin(webapp2.RequestHandler):

    def get(self):

        members = Member.query(Member.active == True).order(Member.username)

        #Identify the slackers for future shaming
        double_list = []
        kill_tracker = []
        
        for person in members:
            
            if person.double < 0:
                double_list.append(person)

            kill_list = person.kill_list
            logging.debug("Type of kill_list: " + str(type(kill_list)))

            kills7 = sum(kill_list[23:])
            kills14 = sum(kill_list[16:])
            kills30 = sum(kill_list)

            kill_dict = {'name': person.username,
                         'kills7': kills7,
                         'kills14': kills14,
                         'kills30': kills30}

            kill_tracker.append(kill_dict)

        template = JINJA_ENVIRONMENT.get_template('admin.html')
        self.response.write(template.render(kills=kill_tracker,double=double_list))

# [END admin]

# [START admin_submit]
class Admin_Submit(webapp2.RequestHandler):

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
            logging.error("RegEx Exception in the Date Parser!")
            return None

    def post(self):

        action = self.request.get('action')
        logging.info("Admin action: " + action)

        if action == "newcontest":

            contest_name = self.request.get('contestname')
            start_date = self.parseDate(str(self.request.get('startdate')))
            end_date = self.parseDate(str(self.request.get('enddate')))

            #If dates could not be parsed, return error.
            if start_date is None or end_date is None:
                result = "Invalid date parameters: Please use DD-MM-YYYY or YYYY-MM-DD"

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
                new_contest = Contest(active=False,
                                      name=contest_name,
                                      start=start_date,
                                      end=end_date,
                                      scores=score_list)

                new_contest.put()
                result = "Contest " + new_contest.name + " successfully created!"

        else:
            logging.warning("Admin action: Unable to resolve action type!")
            result = "Error: Unknown action"

        #Output
        template = JINJA_ENVIRONMENT.get_template('admin_submit.html')
        self.response.write(template.render(info=result))

# [START app]
app = webapp2.WSGIApplication([
    ('/admin/submit', Admin_Submit),
    ('/admin', Admin)
], debug=True)
# [END app]