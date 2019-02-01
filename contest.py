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
                        break

            contest.put()

        today = datetime.date.today()

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
            active = active + [current]
        else:
            current = None
            current_dict = {}
            scores = []

        #Format results for the template
        active_list = []

        for item in active:
                
            item_dict = {'id': item.key.urlsafe(),
                         'name': item.name,
                         'start': item.start.strftime('%d-%m-%Y'),
                         'end': item.end.strftime('%d-%m-%Y')}

            active_list = active_list + [item_dict]

        if current is not None:

            scores = current.scores

            current_dict = {'id': current.key.urlsafe(),
                            'name': current.name,
                            'start': current.start.strftime('%d-%m-%Y'),
                            'end': current.end.strftime('%d-%m-%Y')}

        #Write return
        template = JINJA_ENVIRONMENT.get_template('contest.html')
        self.response.write(template.render(active_contests=active_list,upcoming_contests=upcoming,current=current_dict,scores=scores))

# [END contest_table]
# [START contest_admin]

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
            logging.error("RegEx Exception in the Date Parser!")
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
            new_contest = Contest(active=False,
                                  name=contest_name,
                                  start=start_date,
                                  end=end_date,
                                  scores=score_list)

            new_contest.put()
            result = contest_name + " successfully created!"

            template = JINJA_ENVIRONMENT.get_template('contest_admin.html')
            self.response.write(template.render(info=result))

# [END contest_admin]

# [START app]
app = webapp2.WSGIApplication([
    ('/contest', ContestPublic),
    ('/contest/admin', ContestAdmin),
    ('/contest/admin/submit_contest', ContestAdmin)
], debug=True)
# [END app]
