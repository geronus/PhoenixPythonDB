#test case data for caboosemdw
inputData = """You have 1 tokens. (Unbound: 1 Account Bound: 0)

Purchase Tokens | Permanent Boosts | Temporary Boosts | Miscellaneous

Gold Boost: 1000/1000%
Experience Boost: 1000/1000%
Stat Drop Boost: 1000/1000%
Quest Boost: 1000/1000%
Global Drop Boost: 312/1000%  +1% for 3 Tokens | +10% for 30 Tokens | +100% for 300 Tokens
Health Boost: 50/50%
Attack Boost: 50/50%
Defence Boost: 50/50%
Accuracy Boost: 25/25%
Evasion Boost: 25/25%
Jack of All Jades: 50/50%
Dungeon Mastery: 50/50%
Areaboss Taxonomy'n Taxidermy: 50/50%

[Reset all boosts. You will get back 24386 out of 24436 tokens.]

Autos: 506  +1 for 42 Tokens

[Reset autos. You will get back 8802 out of 8852 tokens.]

Jewellery Slots: 10/10
Tradeskill slots: 20/20

You have reset 1 times. The cost per reset will go up by 50 tokens or 10% of tokens spent each time you reset (whichever's cheaper). Both autos and boosts are on the same reset counter. This is not something that is meant to be used frequently, but more of a one-time 'oh shit I fucked up I need to reset to fix that' kind of thing."""

output = dict()

boostDict = dict({
  'goldTB':'Gold Boost: ',
  'xpTB':'Experience Boost: ',
  'statTB':'Stat Drop Boost: ',
  'questTB':'Quest Boost: ',
  'dropTB':'Global Drop Boost: ',
  'healthTB':'Health Boost: ',
  'attackTB':'Attack Boost: ',
  'defenseTB':'Defense Boost: ',
  'accuracyTB':'Accuracy Boost: ',
  'evasionTB':'Evasion Boost: ',
  'joajTB':'Jack of All Jades: ',
  'dmTB':'Dungeon Mastery: ',
  'taxiTB':"Areaboss Taxonomy'n Taxidermy: ",
  'autosTB':'Autos: ',
  'jewelsTB':'Jewellery Slots: ',
  'tsTB':'Tradeskill slots: '
})

def calcBoost(boostName,line):
  global output
  tempBoost = boostDict[boostName]
  if boostName == 'autosTB': eosChar = ' '
  else: eosChar = '/'
  if tempBoost in line:
    eosIndex = line.index(eosChar,len(tempBoost)+1)
    output[boostName] = int(line[len(tempBoost):eosIndex])

def updateTokenBoosts(data):
  # returns a dictionary (output) with the integer values of the % of the boost that the user pasted into the data.
  # so if the return is 1000, that means the boost is 1000%, and if the return is 300, that means the boost is 300%.
  listed = data.split('\n')
  for item in listed:
    for x in boostDict:
      calcBoost(x,item)
  return output

# # test case for caboosemdw token boosts as 'inputData'
# temp = updateTokenBoosts(inputData)
# for x in temp:
#   print(str(x) + ' == ' + str(temp[x]))
