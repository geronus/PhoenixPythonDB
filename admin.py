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

# [START admin]

class Admin(webapp2.RequestHandler):

    def get(self):

        #Get the member list for the kill tracker, double tracker and ranking system
        members = Member.query(Member.active == True).order(Member.username)

        #Identify the slackers for future shaming
        double_list = []
        kill_tracker = []
        rank_tracker = []
        contests = []

        for person in members:

            #Identify the people with Double debt (slackers)
            if person.double < 0:
                double_list.append(person)

            #Compile the kill tracker
            kill_list = person.kill_list

            kills7 = sum(kill_list[23:])
            kills14 = sum(kill_list[16:])
            kills30 = sum(kill_list)

            kill_dict = {'name': person.username,
                         'kills7': kills7,
                         'kills14': kills14,
                         'kills30': kills30}

            kill_tracker.append(kill_dict)

            #Identify who needs a new rank
            if person.rank_new == True:
                gdp_total = person.gdp + person.gdp_prev
                rank_dict = {'id': person.key.urlsafe(),
                             'name': person.username,
                             'gdp': gdp_total,
                             'rank': person.rank}

                rank_tracker.append(rank_dict)

        #Get contests for deletion
        query_result = Contest.query().order(-Contest.end).fetch()

        for item in query_result:
            contest_dict = {'id': item.key.urlsafe(),
                            'name': item.name}

            contests.append(contest_dict)

        template = JINJA_ENVIRONMENT.get_template('admin.html')
        self.response.write(template.render(kills=kill_tracker,double=double_list,ranks=rank_tracker,contests=contests))

# [END admin]

# [START admin_submit]
class AdminSubmit(webapp2.RequestHandler):

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

        elif action == "updateranks":
            updates = self.request.POST.getall('member')

            for identifier in updates:
                try:
                    candidate_key = ndb.Key(urlsafe=identifier)
                except:
                    candidate_key = None
                    logging.error("Unable to retrieve Member key from POST request! Identifier was " + str(identifier))
                    logging.exception("Exception data:")

                if candidate_key is not None:
                    member = candidate_key.get()
                    member.rank_new = False
                    member.put()

            result = "Rank notifications successfully updated!"

        elif action == "deletecontest":
            contests_to_delete = self.request.POST.getall('contestdelete')

            for identifier in contests_to_delete:
                try:
                    candidate_key = ndb.Key(urlsafe=identifier)
                except:
                    candidate_key = None
                    logging.error("Unable to retrieve Contest key from POST request! Identifier was " + str(identifier))
                    logging.exception("Exception data:")

                if candidate_key is not None:
                    candidate_key.delete()

            result = "Contests successfully updated!"

        else:
            logging.warning("Admin action: Unable to resolve action type!")
            result = "Error: Unknown action"

        #Output
        template = JINJA_ENVIRONMENT.get_template('admin_submit.html')
        self.response.write(template.render(info=result))

# [START app]
app = webapp2.WSGIApplication([
    ('/admin/submit', AdminSubmit),
    ('/admin', Admin)
], debug=True)
# [END app]
