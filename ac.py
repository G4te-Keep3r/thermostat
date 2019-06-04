from time import sleep
from OmegaExpansion import oledExp
import datetime
from thermostatFunctions import *

t_id1 = "28-0516a02c71ff"
t_hall = "28-0516a06388ff"
t_door = "28-0516a3734cff"

t_attic = "28-0516a069b0ff"

def main():
	'''
	params - so get from db
	move vare to dict at some point
	'''
	varsArr = getVarsFromDB()

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

	settingsArr = getSettngsFromDB()

	#the idea here (with rough times) is to over cool before midday heat spike
	'''cooled by 9am or too late it seems'''
	hour = datetime.datetime.now().hour
	#'''
	orig_adjDict = {5: 0.5,
	6: 1.25,
	7: 2.0,
	8: 2.5,
	9: 3.0,
	10: 3.25,
	11: 3.25,
	12: 3.25,
	13: 3.25,
	14: 3.25,
	15: 3.25,
	16: 3.25,
	17: 3.25,
	18: 3.25}
	#'''
	less_far_adjDict = {5: 0.5,
	6: 1.25,
	7: 2.0,
	8: 2.5,
	9: 3.0,
	10: 3.0,
	11: 3.0,
	12: 3.0,
	13: 3.0,
	14: 3.0,
	15: 3.0,
	16: 3.0,
	17: 3.0,
	18: 3.0}
	#symetric
	adjDict = {5: 0.75,
	5: 1.5,
	6: 2.0,
	7: 2.5,
	8: 3.0,
	9: 3.5,
	10: 3.75,
	11: 3.5,
	12: 3.25,
	13: 3.0,
	14: 2.5,
	15: 2.0,
	16: 1.25,
	17: 0.5}

	preHeatCooling = False

	if hour in adjDict:# and getLastOutsideTemp(varsArr[-1]) > 55.0:
		preHeatCooling = True
		settingsArr[3] -= adjDict[hour]
		settingsArr[4] -= adjDict[hour]
	if hour >= 18:
		settingsArr[2] += 15

	logData('variables loaded, entering readings/logic/settings')
	logData('recordID: '+str(varsArr[-1]))
	temp = getTemp(t_id1)
	temp_source = ' :)'

	#temporary solution to catch (individual) bad reads
	#it seems that reading too many reading in close succession might max out the pull up
	if temp < 40:
		logData("temp was %s, trying door"%temp)
		door = getTemp(t_door)
		temp_source = '     ** door **'
		if temp < 40: #temp and door failed
			logData("door was %s, trying hall"%temp)
			temp = getTemp(t_hall)
			temp_source = '     ** hall **'
			saveTempsToDB([0, 0, temp], varsArr[-1])
		else: #temp failed but door succeeded
			saveTempsToDB([0, temp, 0], varsArr[-1])
	else:
		saveTempsToDB([temp, 0, 0], varsArr[-1])

	logData("temp is %s"%temp)
	logData("temp_source is "+temp_source)
	logData("state %s"%state)
	logData("runTime %s"%runTime)
	logData("cooldownTime %s"%cooldownTime)

	if temp == -1: #err/senor not registering again
		logData('temp err')
		if state == 'ON': #on/ac running
			if runTime > 10:
				turnOFF()
				logData('turned AC OFF, -1')
				runTime = 0
				state = 'OFF'
			else:
				runTime += 1
		else: #off/ac not running
			if cooldownTime >= 10:
				turnON()
				logData('turned AC ON, -1')
				cooldownTime = 0
				state = 'ON'
			else:
				cooldownTime += 1

	else: #we good, proceede as normal
		if state == 'ON': #on/ac running
			if (temp < lowCutOff) or (runTime > maxRunTime) or (coolingLimitReached(4, (temp>=((highCutOff+lowCutOff)/2) or preHeatCooling), runTime)): 
				turnOFF()
				logData('turned AC OFF')
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
				logData('turned AC ON')
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
	saveVarsToDB([minCooldown, maxCooldown, maxRunTime, lowCutOff, highCutOff, cooldownTime, runTime, acRunningLowCutOffRaisePercent, acRunningLowCutOffRaiseTimeMin, acOffHighCutOffLowerPercent, acOffHighCutOffLowerPercentNum2, acOffHighCutOffLowerTimeMin, acOffHighCutOffLowerTimeMinNum2, state], varsArr[-1])

	try:
		sendToSite(varsArr[-1], temp, highCutOff, lowCutOff)
	except:
		logData("sendToSite failed. temp:"+str(temp)+", highCutOff:"+str(highCutOff)+", lowCutOff:"+str(lowCutOff))

	### get and update outside temp (l8r other weather details too)
	try:
		outside = getWeather(varsArr[-1])
		saveOutsideTempToDB(outside, varsArr[-1])
		sendOutsideToSite(varsArr[-1], outside)
	except:
		outside = 82.2882

	logData('$ start OLED $')
	#with regular printing is 8 rows of 21 characters
	hr_min = str(datetime.datetime.now().hour)+':'+str(datetime.datetime.now().minute)
	oledStr = ''

	#configure fitst line
	if outside == 82.2882:
		firstLine = [str(temp)]
	else:
		firstLine = [str(temp), str(outside)]

	lastLine = [str(lowCutOff), hr_min, str(highCutOff)]

	if cooldownTime == 0 and runTime == 0:
		oledStrArr = [firstLine, ['   cdt: '+state], ['   rnt: '+state], ['---'], [str(varsArr[-1])], [temp_source], lastLine]
	else: #display minutes and dash on the mode not active
		oledStrArr = [firstLine, ['   cdt: '+str('-' if cooldownTime==0 else cooldownTime)], ['   rnt: '+str('-' if runTime==0 else runTime)], ['---'], [str(varsArr[-1])], [temp_source], lastLine]

	initOled = oledExp.driverInit()
	oledExp.write(prepareOLEDstring(oledStrArr))
	logData('$ end OLED $')

	'''
	current time to run whole code is ~48 seconds
	need to narrow timings without locking omega up from too many reads too close together
	'''
	if temp_source == ' :)': #read main sensor no problem
		#wait 10 seconds and read hall
		sleep(10)
		try:
			temp_hall = getTemp(t_hall)
			logData("*&*&* t_hall = "+str(temp_hall))
			saveHallTempToDB(temp_hall, varsArr[-1])
			sendHallToSite(varsArr[-1], temp_hall)
		except:
			logData("hall failed")

		#get attic
		try:
			sleep(15)
			#test showed takes like 27 seconds to run without attic reading
			#so with sleep 15 still under the 1 minute cronjob mark
			attic = getTemp(t_attic)
			logData("AT-_-_-T-_-_-IC* t_attic = "+str(attic))
			saveAtticToDB(attic, varsArr[-1])
			sendAtticToSite(varsArr[-1], attic)
		except:
			logData("attic failed")

		try:
			#add to oled
			oledStrArr[2].append(str(attic))
			#put on oled
			initOled = oledExp.driverInit()
			oledExp.write(prepareOLEDstring(oledStrArr))
			logData('$ OLED contains attic $')
		except:
			logData("add attic to oled failed")

	logData('---code run done')

if __name__ == '__main__':
	main()
