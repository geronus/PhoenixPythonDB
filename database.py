#!/usr/bin/env python

# [START imports]
import Utilities

from google.appengine.ext import ndb

# [END imports]

class Member(ndb.Model):

	username = ndb.StringProperty()
	active = ndb.BooleanProperty()
	rank = ndb.StringProperty()

	#Personal Stats

	level = ndb.IntegerProperty()
	kills = ndb.IntegerProperty()
	quests = ndb.IntegerProperty()
	base_stats = ndb.IntegerProperty()
	buffed_stats = ndb.IntegerProperty()
	dp = ndb.IntegerProperty()

	#Jade Skills - Computed properties commented out for now
	chc = ndb.IntegerProperty()
	#chc_ext = ndb.ComputedProperty(lambda self: str(float(self.chc) / 100) + '%')
	chd = ndb.IntegerProperty()
	#chd_ext = ndb.ComputedProperty(lambda self: str(float(self.chd) / 100) + '%')
	heroism = ndb.IntegerProperty()
	#heroism_ext = ndb.ComputedProperty(lambda self: str(float(self.heroism) / 40) + '%')
	leadership = ndb.IntegerProperty()
	#leadership_ext = ndb.ComputedProperty(lambda self: str(self.leadership) + '%')
	archaeology = ndb.IntegerProperty()
	#archaeology_ext = ndb.ComputedProperty(lambda self: str(self.archaeology) + '%')
	jc = ndb.IntegerProperty()
	#jc_ext = ndb.ComputedProperty(lambda self: str(self.jc) + '%')
	serendipity = ndb.StringProperty()
	epeen = ndb.IntegerProperty()
	#epeen_ext = ndb.ComputedProperty(lambda self: str(float(self.epeen) / 100) + ' inches')

	#Equipment
	w1 = ndb.IntegerProperty()
	w2 = ndb.IntegerProperty()
	a1 = ndb.IntegerProperty()
	a2 = ndb.IntegerProperty()
	a3 = ndb.IntegerProperty()
	a4 = ndb.IntegerProperty()
	a5 = ndb.IntegerProperty()
	a6 = ndb.IntegerProperty()
	a7 = ndb.IntegerProperty()

	#Current Guild Contributions
	xp = ndb.IntegerProperty()
	money = ndb.IntegerProperty()
	jade = ndb.IntegerProperty()
	gems = ndb.IntegerProperty()
	food = ndb.IntegerProperty()
	iron = ndb.IntegerProperty()
	stone = ndb.IntegerProperty()
	lumber = ndb.IntegerProperty()
	gdp = ndb.IntegerProperty()
	gdp_spent = ndb.IntegerProperty()
	double = ndb.IntegerProperty()
	rp = ndb.IntegerProperty()
	weekly_gdp = ndb.IntegerProperty()
	last_weekly_gdp = ndb.IntegerProperty()

	#Previous Guild Contributions
	xp_prev = ndb.IntegerProperty()
	money_prev = ndb.IntegerProperty()
	jade_prev = ndb.IntegerProperty()
	gems_prev = ndb.IntegerProperty()
	food_prev = ndb.IntegerProperty()
	iron_prev = ndb.IntegerProperty()
	stone_prev = ndb.IntegerProperty()
	lumber_prev = ndb.IntegerProperty()
	gdp_prev = ndb.IntegerProperty()
	gdp_spent_prev = ndb.IntegerProperty()
	rp = ndb.IntegerProperty()
	
	#Token Boosts
	#if renamed, also rename the dictionary entries in the 'tokenBoostParser.py' file
	goldTB = ndb.IntegerProperty()
	xpTB = ndb.IntegerProperty()
	statTB = ndb.IntegerProperty()
	questTB = ndb.IntegerProperty()
	dropTB = ndb.IntegerProperty()
	healthTB = ndb.IntegerProperty()
	attackTB = ndb.IntegerProperty()
	defenseTB = ndb.IntegerProperty()
	accuracyTB = ndb.IntegerProperty()
	evasionTB = ndb.IntegerProperty()
	joajTB = ndb.IntegerProperty()
	dmTB = ndb.IntegerProperty()
	taxiTB = ndb.IntegerProperty()
	autosTB = ndb.IntegerProperty()
	jewelsTB = ndb.IntegerProperty()
	tsTB = ndb.IntegerProperty()
