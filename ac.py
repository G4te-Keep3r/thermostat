from time import sleep
import datetime
from thermostatFunctions import *

def main():
	logData('---code run top')

	V_S_arr = getV_S_FromDB()
	varsArr = V_S_arr[:14]

	minCooldown = varsArr[0]
	maxCooldown = varsArr[1]
	maxRunTime = varsArr[2]
	lowCutOff = varsArr[3] ## ones that are variable and change
	highCutOff = varsArr[4] ##
	cooldownTime = int(varsArr[5]) ##
	runTime = int(varsArr[6]) ##
	acRunningLowCutOffRaisePercent = varsArr[7]
	acRunningLowCutOffRaiseTimeMin = varsArr[8]
	acOffHighCutOffLowerPercent = varsArr[9]
	acOffHighCutOffLowerPercentNum2 = varsArr[10]
	acOffHighCutOffLowerTimeMin = varsArr[11]
	acOffHighCutOffLowerTimeMinNum2 = varsArr[12]
	state = varsArr[13]

	settingsArr = V_S_arr[14:]

	#the idea here (with rough times) is to over cool before midday heat spike
	hour = datetime.datetime.now().hour
	minute = datetime.datetime.now().minute

	preHeatCooling = False

	lastOutsideTemp = V_S_arr[-1]
	adjDelta = getAdjDelta(hour, minute, lastOutsideTemp, highCutOff)
	if adjDelta != 0:
		preHeatCooling = True
		settingsArr[3] -= adjDelta
		settingsArr[4] -= adjDelta
	if hour >= 18:
		settingsArr[2] += 15

	#read temps
	sensorIDs = getTempSensors()
	temp = getTemp(sensorIDs[0][0])#t_id1)
	temp_2 = getTemp(sensorIDs[1][0])#t_door)
	temp_3 = getTemp(sensorIDs[2][0])#t_hall)
	attic = getTemp(sensorIDs[-1][0])#t_attic)		# -1 because it allows easier addition/removal of others

	logData("temp is %s"%temp)
	logData("%s is %s" % (sensorIDs[1][1],temp_2))
	logData("%s is %s" % (sensorIDs[2][1],temp_3))
	logData("attic is %s"%attic)
	logData("")
	logData("highCutOff is %s"%highCutOff)
	logData("lowCutOff is %s"%lowCutOff)
	logData("")
	logData("state %s"%state)
	logData("runTime %s"%runTime)
	logData("cooldownTime %s"%cooldownTime)

	# new sensor failover handling
	# it had been so long since a failure that the redundancy/safemode was lost in migration
	failure_ergo_SAFEMODE = False
	activeTemp = 0 + temp
	if activeTemp == -1: #should consider comparing the 3 to catch erroneous readings that are not flat failures
		activeTemp = 0 + temp_2
		logData('temp failed, trying temp_2')
		if activeTemp == -1:
			activeTemp = 0 + temp_3
			logData('temp_2 failed, trying temp_3')
			if activeTemp == -1:
				failure_ergo_SAFEMODE = True
				logData('temp_3 failed, entering failure_ergo_SAFEMODE')

	if failure_ergo_SAFEMODE:
		if state == 'ON': #on/ac running
			#if (runTime > maxRunTime):
			if runTime > 10: #should set the safemode on/off times in settings possibly
				turnOFF()
				logData('turned AC OFF - ' + str(highCutOff) + ' - ' + str(lowCutOff))
				runTime = 0
				state = 'OFF'
				minCooldown = settingsArr[0]
				maxCooldown = settingsArr[1]
				maxRunTime = settingsArr[2]
				lowCutOff = settingsArr[3]
				highCutOff = settingsArr[4]
				cooldownTime = settingsArr[5]
				runTime = settingsArr[6]
				acRunningLowCutOffRaisePercent = settingsArr[7]
				acRunningLowCutOffRaiseTimeMin = settingsArr[8]
				acOffHighCutOffLowerPercent = settingsArr[9]
				acOffHighCutOffLowerPercentNum2 = settingsArr[10]
				acOffHighCutOffLowerTimeMin = settingsArr[11]
				acOffHighCutOffLowerTimeMinNum2 = settingsArr[12]
			else:
				runTime += 1
		else: #off/ac not running
			if cooldownTime >= 10:
				turnON()
				logData('turned AC ON - ' + str(highCutOff) + ' - ' + str(lowCutOff))
				cooldownTime = 0
				state = 'ON'
				minCooldown = settingsArr[0]
				maxCooldown = settingsArr[1]
				maxRunTime = settingsArr[2]
				lowCutOff = settingsArr[3]
				highCutOff = settingsArr[4]
				cooldownTime = settingsArr[5]
				runTime = settingsArr[6]
				acRunningLowCutOffRaisePercent = settingsArr[7]
				acRunningLowCutOffRaiseTimeMin = settingsArr[8]
				acOffHighCutOffLowerPercent = settingsArr[9]
				acOffHighCutOffLowerPercentNum2 = settingsArr[10]
				acOffHighCutOffLowerTimeMin = settingsArr[11]
				acOffHighCutOffLowerTimeMinNum2 = settingsArr[12]
			else:
				cooldownTime += 1

	else:
		#determine if should change state
		if state == 'ON': #on/ac running
			if (activeTemp < lowCutOff) or (runTime > maxRunTime) or (coolingLimitReached(6, (activeTemp>=((highCutOff+lowCutOff)/2) or preHeatCooling), runTime)): 
				turnOFF()
				logData('turned AC OFF - ' + str(highCutOff) + ' - ' + str(lowCutOff))
				runTime = 0
				state = 'OFF'
				minCooldown = settingsArr[0]
				maxCooldown = settingsArr[1]
				maxRunTime = settingsArr[2]
				lowCutOff = settingsArr[3]
				highCutOff = settingsArr[4]
				cooldownTime = settingsArr[5]
				runTime = settingsArr[6]
				acRunningLowCutOffRaisePercent = settingsArr[7]
				acRunningLowCutOffRaiseTimeMin = settingsArr[8]
				acOffHighCutOffLowerPercent = settingsArr[9]
				acOffHighCutOffLowerPercentNum2 = settingsArr[10]
				acOffHighCutOffLowerTimeMin = settingsArr[11]
				acOffHighCutOffLowerTimeMinNum2 = settingsArr[12]
			else:
				runTime += 1
				if runTime > acRunningLowCutOffRaiseTimeMin and activeTemp < highCutOff:
					lowCutOff += acRunningLowCutOffRaisePercent * (activeTemp - lowCutOff)
		else: #off/ac not running
			if (activeTemp >= highCutOff and cooldownTime >= minCooldown) or (cooldownTime > maxCooldown):
				turnON()
				logData('turned AC ON - ' + str(highCutOff) + ' - ' + str(lowCutOff))
				cooldownTime = 0
				state = 'ON'
				minCooldown = settingsArr[0]
				maxCooldown = settingsArr[1]
				maxRunTime = settingsArr[2]
				lowCutOff = settingsArr[3]
				highCutOff = settingsArr[4]
				cooldownTime = settingsArr[5]
				runTime = settingsArr[6]
				acRunningLowCutOffRaisePercent = settingsArr[7]
				acRunningLowCutOffRaiseTimeMin = settingsArr[8]
				acOffHighCutOffLowerPercent = settingsArr[9]
				acOffHighCutOffLowerPercentNum2 = settingsArr[10]
				acOffHighCutOffLowerTimeMin = settingsArr[11]
				acOffHighCutOffLowerTimeMinNum2 = settingsArr[12]
			else:
				cooldownTime += 1
				if cooldownTime > acOffHighCutOffLowerTimeMin:
					###### this is where weater api comes in...copy out of older code
					highCutOff -= acOffHighCutOffLowerPercent * (highCutOff - activeTemp)
				if cooldownTime > acOffHighCutOffLowerTimeMinNum2: #>45 is >15 so it'll lower cutoff twice...reverse order and use if elif or take that into account
					highCutOff -= acOffHighCutOffLowerPercentNum2 * (highCutOff - activeTemp)

	#save to db
	V_T_arr = []
	for var in [minCooldown, maxCooldown, maxRunTime, lowCutOff, highCutOff, cooldownTime, runTime, acRunningLowCutOffRaisePercent, acRunningLowCutOffRaiseTimeMin, acOffHighCutOffLowerPercent, acOffHighCutOffLowerPercentNum2, acOffHighCutOffLowerTimeMin, acOffHighCutOffLowerTimeMinNum2, state]:
		V_T_arr.append(var)

	V_T_arr.extend([temp, temp_2, temp_3, attic])

	saveV_T_ToDB(V_T_arr)

	logData('---code run done\n')

if __name__ == '__main__':
	main()
