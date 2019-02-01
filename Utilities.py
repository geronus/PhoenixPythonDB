##################################################################################################
# Function: money_external
# Parameters: Int money (in copper)
# Returns: External text string with commas and denominations
##################################################################################################
def money_external(money):
	money = int(money)
	copper = money % 100
	money /= 100
	silver = money % 100
	money /= 100
	gold = money % 100
	money /= 100
	plat = "{:,}".format(money)
	return  (plat + 'p ' + str(gold) + 'g ' + str(silver) + 's ' + str(copper) + 'c')

def xp_external(xp):
	xp = int(xp)
	xp_ext = "{:,}".format(xp)
	return xp_ext