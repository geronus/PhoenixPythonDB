#test case data for caboosemdw
inputData = """Welcome to the Jade Temple! Monks with ancient knowledge inhabit this place. They may be willing to share their knowledge with you in exchange for pieces of their favourite pretty stones. They have graciously expanded their teaching services, but they ask that you train each skill no more than 100 times per session.
Critical Hit Chance: 197.5% Train times for 0 jade.
Critical Hit Damage: 227.5% Train times for 0 jade.
Heroism: 302.00% Train times for 0 jade.
Leadership: 150% Train times for 0 jade.
Archaeology: 0% Train times for 0 jade.
Jewelcrafting: 0% Train times for 0 jade.
Serendipity: 0.00 level bonus Train times for 0 jade.
E-Peen: 0.01 inches Train times for 0 jade.
Statue of the Jade God: Offer jade.
a total of 0 jade to the monks.
this form."""

output = dict()

jadeSkillDict = dict({
  'chc':'Critical Hit Chance: ',
  'chd':'Critical Hit Damage: ',
  'heroism':'Heroism: ',
  'leadership':'Leadership: ',
  'archaeology':'Archaeology: ',
  'jc':'Jewelcrafting: ',
  'serendipity':'Serendipity: ',
  'epeen':'E-Peen: '
})

def calcSkill(jsName,line):
  global output
  tempJSN = jadeSkillDict[jsName]
  if tempJSN in line:
    eos = 0
    if line.find('%') > 0:
      eos = line.find('%')
    else:
      eos = len(tempJSN) + line[len(tempJSN):].find(' ')
    output[jsName] = float(line[len(tempJSN):eos])

def updateJS(data):
  # call this function on the input from the text box to return a dictionary of the field names as the key and the user's js # as the value.
  # this function returns the dictionary to be handled by the backend.
  # the username will need to be pulled from the combobox where they select who they are to update the jskills.
  listed = data.split("\n")
  for item in listed[1:len(listed)]:
    for x in jadeSkillDict:
      calcSkill(x,item)
  # print(output)
  # for y in output:
  #   print(y + ' === ' + str(output[y]))
  return output

def test(inputData):
  testing = updateJS(inputData)
  for x in testing:
    print(x + ' == ' + str(testing[x]))

test(inputData)
