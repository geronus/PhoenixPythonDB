#!/usr/bin/env python

# [START imports]
import os
import urllib
import json
import hashlib
import Utilities
import datetime
import logging
import convertARnumbers

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

# [START DailyMaintenance]
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

        #[START UPDATE GUILD MEMBERS]

        for member in result['members']:
            #Attempt to fetch this member from the DB
            candidate_key = try_key(member['id'])
            entry = candidate_key.get()

            #If member not found, create a new one and set aside for addition to ongoing contests
            if entry is None:
                logging.info("New member detected: " + member['username'])

                #The kill_list property is a list of daily kills totals for the 30 days. We initialize it here by setting the first 29 values to 0
                kill_tracker = []

                for x in xrange(0,29):
                    kill_tracker.append(0)

                #
                # Then we set the last value to the new member's kills from yesterday.
                # When we read this list back for the UI, we do so starting from the end, so the list is in reverse order.
                # E.g., the first value in the list is actually the oldest, and the one at the end is the newest.
                #
                kill_tracker.append(int(member['kills']['kills']) - int(member['kills']['yesterdays_kills']))

                infant_member = Member(id=member['id'],
                                       username=member['username'],
                                       rank="0",
                                       rank_int=0,
                                       rank_milestone=1000,
                                       rank_new=False,
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
                                       rp_prev=0,
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
                                       a7=0,
                                       kill_list=kill_tracker)
                
                infant_member.put()
                new_member = [member['id']]
                contest_additions = contest_additions + new_member

            #Otherwise, update the existing entry
            else:
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

                #Update kill tracker
                kill_tracker = entry.kill_list

                yesterdays_kills = int(member['kills']['kills']) - int(member['kills']['yesterdays_kills'])

                kill_tracker.append(yesterdays_kills)
                kill_tracker = kill_tracker[1:]
                entry.kill_list = kill_tracker

                #Update rank
                if entry.gdp >= entry.rank_milestone:
                    entry.rank_new = True
                    new_rank = 0

                    #Rank corresponds to index of RANKS array in Utilities module
                    for x in xrange(0, (len(Utilities.RANKS) - 1)):
                        if entry.gdp >= Utilities.RANKS[x]:
                            new_rank = x
                        else:
                          break

                    entry.rank_int = new_rank
                    entry.rank_milestone = Utilities.RANKS[new_rank + 1]
                    #Convert arabic rank number to roman numerals and save as a string
                    entry.rank = convertARnumbers.converts(new_rank)

                #Update the database
                entry.put()

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

            #If no longer a member, inactivate and store off previous stats
            if result['guild_name'] != 'Phoenix':
                logging.info("Member no longer in guild: " + person.username)
                person.active = False
                person.xp_prev = person.xp
                person.money_prev = person.money
                person.jade_prev = person.jade
                person.gems_prev = person.gems
                person.food_prev = person.food
                person.iron_prev = person.iron
                person.stone_prev = person.stone
                person.lumber_prev = person.lumber
                person.gdp_prev = person.gdp
                person.gdp_spent_prev = person.gdp_spent
                person.rp_prev = person.rp

                #Wipe the kill tracker
                kill_tracker = person.kill_list
                
                for x in xrange(0,30):
                    kill_tracker[x] = 0

                person.kill_list = kill_tracker
                
            person.put()

        #[END UPDATE GUILD MEMBERS]
        #[START UPDATE CONTESTS]

        #Get today and also yesterday, since contests up until yesterday are relevant
        today = Utilities.todayUTC()
        date_adjust = datetime.timedelta(days=-1)
        yesterday = today + date_adjust

        contest_list = Contest.query(Contest.end >= yesterday)

        if contest_list is None:
            logging.info("No active contests")

        else:
            for item in contest_list:
                logging.info("Updating contest: " + item.name)

                if item.start <= today and item.end >= today:
                    item.active = True
                else:
                    item.active = False

                for score in item.scores:
                    candidate_key = try_key(score.member_id)
                    this_member = candidate_key.get()

                    if this_member is not None:
                        score.current_gdp = this_member.gdp
                        score.member_name = this_member.username

                        if item.start == today:
                            score.start_gdp = this_member.gdp

                    else:
                        logging.warning("Unable to retrieve member: " + score.member_name)

                for addition in contest_additions:
                    candidate_key = try_key(addition)
                    entity = candidate_key.get()

                    if entity is not None:
                        new_score = ContestScore(member_id=entity.key.id(),
                                                 member_name=entity.username,
                                                 start_gdp=entity.gdp,
                                                 current_gdp=entity.gdp)

                        item.scores = item.scores + [new_score]

                    else:
                        logging.warning("Unable to add contest addition: " + str(addition))

                item.put()
        #[END Update Contests]
#[END DailyMaintenace]

# [START app]
app = webapp2.WSGIApplication([
    ('/maintenance', DailyMaintenance)
], debug=True)
# [END app]
