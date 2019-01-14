# create the costs of the equipments
unitCost = [0,5000]
for x in range(2,3001):
  unitCost.append(5000*(x+(x-1)*(x-2))+9900*(x-1))

def equipUpgradeCalc(current,new,bsl=50):
  # current is the current level of equipment,
  # new is the desired level of equipment,
  # bsl is the blacksmith level (default to 50)
  output = dict({'1equip':0,'2weaps':0,'7armors':0})
  temp = 0
  for y in range(current,new):
    temp += unitCost[y]
  temp = round(temp*bsl/100)
  output['1equip'] = temp
  output['2weaps'] = 2*temp
  output['7armors'] = 7*temp
  return(output)

# test case 763 to 764 with no blacksmith level supplied
# should return 1455384400 (1455p 38g 44s 0c for bsl 50)
# print(equipUpgradeCalc(763,764))

# test case 1133 to 1150
# should return 55329993500 (55,329p 99g 35s 0c)
# print(equipUpgradeCalc(1133,1150,50))
