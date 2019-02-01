#!/usr/bin/env python

# [START imports]
import os
import urllib
import json
import hashlib
import Utilities
import datetime
import logging

from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
from database import Member
from database import Contest
from database import ContestScore

import webapp2

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
class DailyMaintenance(webapp2.RequestHandler):

    def get(self):
        logging.info("Starting maintenance job...")

        #Form URL
        url = 'https://lyrania.co.uk/api/guilds/member_list.php?'
        params = {'api_code': GUILD_SECRET}
        encoded_params = urllib.urlencode(params)
        url = url + encoded_params

        #Fetch request and format response
        response= urlfetch.fetch(url=url, validate_certificate=True)
        result = json.loads(response.content)
        contest_additions = []

        #[START UPDATE GUILD CONTRIBUTIONS]

        for member in result['members']:
            #Attempt to fetch this member from the DB
            candidate_key = try_key(member['id'])

            #If member not found, create a new one and set aside for addition to ongoing contests
            if candidate_key == None:
                logging.info("New member detected: " + member['username'])

                infant_member = Member(id=member['id'],
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
                
                infant_member.put()
                new_member = [member['id']]
                contest_additions = contest_additions + new_member

            #Otherwise, update the existing entry
            else:
                entry = candidate_key.get()
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

        #[END UPDATE GUILD CONTRIBUTIONS]
        #[START UPDATE STATS]

        root_url = 'https://lyrania.co.uk/api/accounts/public_profile.php?'
        memberlist = []

        members = Member.query(Member.active == True).order(Member.username)

        for person in members:

            #Form URL
            params = {'search': str(person.key.id())}
            encoded_params = urllib.urlencode(params)
            url = root_url + encoded_params

            #Fetch request and format response
            response = urlfetch.fetch(url=url, validate_certificate=True)
            result = json.loads(response.content)
            list_addition = [result]
            memberlist = memberlist + list_addition

            #Do stuff with the database HERE
            person.username = result['name']
            person.level = int(result['level'])
            person.quests = int(result['quests_complete'])
            person.base_stats = int(result['base_stats'])
            person.dp = int(result['earned_dp'])

            if result['guild_name'] != 'Phoenix':
                logging.info("Member no longer in guild: " + person.username)
                person.active = False
                
            person.put()

        #[END UPDATE STATS]
        #[START UPDATE CONTESTS]

        #Get today and also yesterday, since contests up until yesterday are relevant
        today = datetime.date.today()
        date_adjust = datetime.timedelta(days=-1)
        yesterday = today + date_adjust

        contest_list = Contest.query(Contest.end >= yesterday)

        if contest_list is None:
            logging.info("No active contests")

        else:
            for item in contest_list:
                logging.info("Updating contest: " + item.name)

                if item.start <= today and item.end > today:
                    item.active = True
                else:
                    item.active = False

                for score in item.scores:
                    candidate_key = try_key(score.member_id)

                    if candidate_key is not None:
                        this_member = candidate_key.get()
                        score.current_gdp = this_member.gdp

                        if item.start == today:
                            score.start_gdp = this_member.gdp

                    else:
                        logging.warning("Unable to retrieve member: " + score.member_name)

                for addition in contest_additions:
                    entity = try_key(addition)

                    if entity is not None:
                        new_score = ContestScore(member_id=entity.key.id(),
                                                 member_name=entity.username,
                                                 start_gdp=entity.gdp,
                                                 current_gdp=entity.gdp)

                        item.scores = item.score + [new_score]

                    else:
                        logging.warning("Unable to add contest addition: " + str(addition))

                item.put()
        #[END Update Contests]

# [START app]
app = webapp2.WSGIApplication([
    ('/maintenance', DailyMaintenance)
], debug=True)
# [END app]
