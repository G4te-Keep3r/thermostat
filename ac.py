from time import sleep
import datetime
from thermostatFunctions import *

def main():
	logData('---code run top')

	V_S_arr = getV_S_FromDB()
	#varsArr = getVarsFromDB()
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

	#settingsArr = getSettngsFromDB()
	settingsArr = V_S_arr[14:]

	#the idea here (with rough times) is to over cool before midday heat spike
	hour = datetime.datetime.now().hour
	minute = datetime.datetime.now().minute

	preHeatCooling = False

	#if hour in adjDict:# and getLastOutsideTemp(varsArr[-1]) > 55.0:
	lastOutsideTemp = V_S_arr[-1]
	#adjDelta = getAdjDelta(hour, minute, getLastOutsideTemp(recordID), highCutOff)
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
	temp_door = getTemp(sensorIDs[1][0])#t_door)
	temp_hall = getTemp(sensorIDs[2][0])#t_hall)
	attic = getTemp(sensorIDs[-1][0])#t_attic)		# -1 because it allows easier addition/removal of others

	logData("temp is %s"%temp)
	logData("temp_door is %s"%temp_door)
	logData("temp_hall is %s"%temp_hall)
	logData("attic is %s"%attic)
	logData("")
	logData("highCutOff is %s"%highCutOff)
	logData("lowCutOff is %s"%lowCutOff)
	logData("")
	logData("state %s"%state)
	logData("runTime %s"%runTime)
	logData("cooldownTime %s"%cooldownTime)




	#determine if should change state
	if state == 'ON': #on/ac running
		if (temp < lowCutOff) or (runTime > maxRunTime) or (coolingLimitReached(6, (temp>=((highCutOff+lowCutOff)/2) or preHeatCooling), runTime)): 
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
			if runTime > acRunningLowCutOffRaiseTimeMin and temp < highCutOff:
				lowCutOff += acRunningLowCutOffRaisePercent * (temp - lowCutOff)
	else: #off/ac not running
		if (temp >= highCutOff and cooldownTime >= minCooldown) or (cooldownTime > maxCooldown):
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
				highCutOff -= acOffHighCutOffLowerPercent * (highCutOff - temp)
			if cooldownTime > acOffHighCutOffLowerTimeMinNum2: #>45 is >15 so it'll lower cutoff twice...reverse order and use if elif or take that into account
				highCutOff -= acOffHighCutOffLowerPercentNum2 * (highCutOff - temp)

	#save to db
	V_T_arr = []
	for var in [minCooldown, maxCooldown, maxRunTime, lowCutOff, highCutOff, cooldownTime, runTime, acRunningLowCutOffRaisePercent, acRunningLowCutOffRaiseTimeMin, acOffHighCutOffLowerPercent, acOffHighCutOffLowerPercentNum2, acOffHighCutOffLowerTimeMin, acOffHighCutOffLowerTimeMinNum2, state]:
		V_T_arr.append(var)

	V_T_arr.extend([temp, temp_door, temp_hall, attic])

	saveV_T_ToDB(V_T_arr)

	logData('---code run done\n')

if __name__ == '__main__':
	main()
