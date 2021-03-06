import datetime

RANKS = [0,
         1000,2000,3000,4000,5000,
         7500,10000,12500,15000,20000,
         25000,30000,35000,40000,50000,
         60000,70000,80000,90000,100000,
         120000,140000,160000,180000,200000,
         220000,240000,260000,280000,300000,
         320000,340000,360000,380000,400000,
         420000,440000,460000,480000,500000,
         525000,550000,575000,600000,625000,
         650000,675000,700000,725000,750000,
         775000,800000,825000,850000,875000,
         900000,925000,950000,975000,1000000,
         1025000,1050000,1075000,1100000,1125000,
         1150000,1175000,1200000,1225000,1250000,
         1275000,1300000,1325000,1350000,1375000,
         1400000,1425000,1450000,1475000,1500000,
         1525000,1550000,1575000,1600000,1625000,
         1650000,1675000,1700000,1725000,1750000,
         1775000,1800000,1825000,1850000,1875000,
         1900000,1925000,1950000,1975000,2000000,
         2025000,2050000,2075000,2100000,2125000,
         2150000,2175000,2200000,2225000,2250000,
         2275000,2300000,2325000,2350000,2375000,
         2400000,2425000,2450000,2475000,2500000,
         2525000,2550000,2575000,2600000,2625000,
         2650000,2675000,2700000,2725000,2750000,
         2775000,2800000,2825000,2850000,2875000,
         2900000,2925000,2950000,2975000,3000000]

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


def todayUTC():
	utc = datetime.datetime.utcnow()
	return utc.date()
	
def todayGMT():
    from datetime import timedelta, datetime as dt
    tday = dt.utcnow()
    if tday.strftime("%m %d") <= str("03 31"):timeshift = 0
    elif tday.strftime("%m %d") > str("10 27"):timeshift = 0
    else: timeshift = 1
    tday = tday + timedelta(hours=timeshift)
    tday = tday.date()
    #tday=tday.strftime('%Y-%m-%d')
    return tday

	
	
