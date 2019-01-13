# test case data for caboosemdw
inputData ="""
Equipment

Shortsword [763]

Dagger [763]

Helmet [436]

Shoulders [436]

Wrists [436]

Gloves [436]

Chestpiece [436]

Leggings [436]

Boots [436]
"""

output = dict({'w1':0,'w2':0,'a1':0,'a2':0,'a3':0,'a4':0,'a5':0,'a6':0,'a7':0})
translate = dict({0:'w1',1:'w2',2:'a1',3:'a2',4:'a3',5:'a4',6:'a5',7:'a6',8:'a7'})
newEquips = []

def updateEQ(data):
  # call this function on the input textbox from the 'Update Equipment' form to return a dictionary of the weapon/armor levels of the user selected in the combobox
  # this function returns the dictionary to be handled by the backend.
  # the username will need to be pulled from the combobox where they select who they are to update the equipments.
  global output
  global translate

  listed = data.split("\n")
  for item in listed:
    if item.find('[') > 0:
      newEquips.append(int(item[item.index('[')+1:item.index(']')]))

  counter = 0
  while counter < 9:
    output[translate[counter]] = newEquips[counter]
    counter += 1
  
  return output

# def test():
#   #test case for input data for caboosemdw
#   print(updateEQ(inputData))
# 
# test()
# print(output)
