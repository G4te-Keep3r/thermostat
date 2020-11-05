from time import sleep
from OmegaExpansion import oledExp
import datetime
from thermostatFunctions import *

'''
for my config:
*t_id1 is in my room (closer to me)
*t_door is near my door and is only really used as a backup
*t_hall is where thermostat is/ac wires
*t_attic is run thru the wall with the ac wires and hanging in the attic

i know, not super generic use case, but this project started from a specific problem case and has evolved over time...but is mostly tied to specific hardware/hardware limitations and badly insulated attic with texas heat (still toying with a distributed form of this)
'''
t_id1 = "28-0516a02c71ff"
t_hall = "28-0516a06388ff"
t_door = "28-0516a3734cff"

#t_attic = "28-0516a069b0ff"
t_attic = "28-0301a279034b"

def getAdjDelta(hour, minute, lastOutside, highCutOff):
	if lastOutside < highCutOff - 15:
		#real fun is if daily high < highCutOff + 15, dont precool ie return 0
		return 0
	if hour >= 3 and hour <= 15:
		#based on the latest adjDict
		#3-9 0.5 deg lower an hour (-0.5 to -3.5)
		#9-10 0.25 lower (-3.5 to -3.75)
		if hour < 10:
			if hour < 9:
				ret = (hour - 2) * 0.5
				ret += 0.5 * (minute / 60.0)
				return ret
			#else, so hour 9
			ret = 3.5
			ret += 0.25 * (minute / 60.0)
			return ret

		#10-11 0.25 higher (-3.75 to -3.5)
		#11-12 0.25 higher (-3.5 to -3)
		#***EXPERIMENT-diff than adjDict***
		#12-4 0.75 higher per hour (-3 to 0)
		else:
			if hour == 10:
				ret = 3.75
				#ret -= 0.25 * (hour - 10)
				ret -= 0.25 * (minute / 60.0)
				return ret
			if hour == 11:
				ret = 3.5
				#ret -= 0.25 * (hour - 10)
				ret -= 0.5 * (minute / 60.0)
				return ret

			#else, hour 12+
			ret = 3.0
			ret -= 0.75 * (hour - 12)
			ret -= 0.75 * (minute / 60.0)
			return ret
	else:
		return 0

def main():
	'''
	params - so get from db
	move vare to dict at some point
	'''
	V_S_arr = getV_S_FromDB()
	#varsArr = getVarsFromDB()
	varsArr = V_S_arr[:15]

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

	#recordID = varsArr[-1] #not sure why it took me this long to change this
	recordID = varsArr[14] #not sure why it took me this long to change this

	#settingsArr = getSettngsFromDB()
	settingsArr = V_S_arr[15:-1]

	#the idea here (with rough times) is to over cool before midday heat spike
	'''cooled by 9am or too late it seems'''
	hour = datetime.datetime.now().hour
	minute = datetime.datetime.now().minute
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
	adjDict = {3: 0.5,
	4: 1.0,
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


	#second half neeeds to come back to normal faster

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

	logData('variables loaded, entering readings/logic/settings')
	logData('recordID: '+str(recordID))
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
			#saveTempsToDB([0, 0, temp], varsArr[-1])
		#else: #temp failed but door succeeded
		#	#saveTempsToDB([0, temp, 0], varsArr[-1])
	#else:
	#	#saveTempsToDB([temp, 0, 0], varsArr[-1])

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
			#if (temp < lowCutOff) or (runTime > maxRunTime) or (coolingLimitReached(6, (temp>=((highCutOff+lowCutOff)/2) or preHeatCooling), runTime)): 
			
			# change limit variable to 4 while running easy till they inspect the unit
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
	#saveVarsToDB([minCooldown, maxCooldown, maxRunTime, lowCutOff, highCutOff, cooldownTime, runTime, acRunningLowCutOffRaisePercent, acRunningLowCutOffRaiseTimeMin, acOffHighCutOffLowerPercent, acOffHighCutOffLowerPercentNum2, acOffHighCutOffLowerTimeMin, acOffHighCutOffLowerTimeMinNum2, state], recordID)
	V_T_arr = []
	for var in [minCooldown, maxCooldown, maxRunTime, lowCutOff, highCutOff, cooldownTime, runTime, acRunningLowCutOffRaisePercent, acRunningLowCutOffRaiseTimeMin, acOffHighCutOffLowerPercent, acOffHighCutOffLowerPercentNum2, acOffHighCutOffLowerTimeMin, acOffHighCutOffLowerTimeMinNum2, state]:
		V_T_arr.append(var) #this is to (**) avoid any pointer issues, but since this code runs 1 time and is not a while 1, probably safe to start with V_T_arr = [minC....] and append the temps
		#(**) help avoid...to make sure i would need to make a None variable and add the var to it and then append it

	#try:
	#	sendToSite(recordID, temp, highCutOff, lowCutOff, state)
	#except:
	#	logData("sendToSite failed. temp:"+str(temp)+", highCutOff:"+str(highCutOff)+", lowCutOff:"+str(lowCutOff)+", state:"+state)

	### get and update outside temp (l8r other weather details too)
	try:
		outside = getWeather(recordID)
		#saveOutsideTempToDB(outside, varsArr[-1])
		#sendOutsideToSite(recordID, outside)
	except:
		outside = 82.2882

	logData('$ start OLED $')
	#with regular printing is 8 rows of 21 characters

	if datetime.datetime.now().hour == 12: #noon
		hr_min = 'noon:'+str(datetime.datetime.now().minute)
	elif datetime.datetime.now().hour == 0: #midnight
		hr_min = 'midnight:'+str(datetime.datetime.now().minute) #hope those 3 characters arent too much
	elif datetime.datetime.now().hour > 12: #pm
		hr_min = str(datetime.datetime.now().hour-12)+':'+str(datetime.datetime.now().minute)+' p'
	else: #am
		hr_min = str(datetime.datetime.now().hour)+':'+str(datetime.datetime.now().minute)+' a'
	
	oledStr = ''

	#configure fitst line
	if outside == 82.2882:
		firstLine = [str(temp)]
	else:
		firstLine = [str(temp), 'o: '+str(outside)]

	#lastLine = [str(lowCutOff), hr_min, str(highCutOff)]
	lastLine = [lowCutOff, hr_min, highCutOff]

	if cooldownTime == 0 and runTime == 0:
		oledStrArr = [firstLine, ['   cdt: '+state], ['   rnt: '+state], ['---'], [str(recordID)], [temp_source], lastLine]
	else: #display minutes and dash on the mode not active
		oledStrArr = [firstLine, ['   cdt: '+str('-' if cooldownTime==0 else cooldownTime)], ['   rnt: '+str('-' if runTime==0 else runTime)], ['---'], [str(recordID)], [temp_source], lastLine]

	initOled = oledExp.driverInit()
	MMDD = str(datetime.datetime.now().month)+'-'+str(datetime.datetime.now().day)
	oledExp.write(prepareOLEDstring(oledStrArr, adjDelta, MMDD))
	logData('$ end OLED $')

	'''
	current time to run whole code is ~48 seconds
	need to narrow timings without locking omega up from too many reads too close together
	'''
	if temp_source == ' :)': #read main sensor no problem
		#wait 10 seconds and read hall
		#sleep(10)
		# running the rest of the script should have given enough time...?
		try:
			temp_hall = getTemp(t_hall)
			logData("*&*&* t_hall = "+str(temp_hall))
			#saveHallTempToDB(temp_hall, varsArr[-1])
			#sendHallToSite(recordID, temp_hall)
		except:
			logData("hall failed")
			temp_hall = '71.1771'

		#get attic
		try:
			sleep(15)
			#test showed takes like 27 seconds to run without attic reading
			#so with sleep 15 still under the 1 minute cronjob mark
			attic = getTemp(t_attic)
			logData("AT-_-_-T-_-_-IC* t_attic = "+str(attic))
			#saveAtticToDB(attic, varsArr[-1])
			#sendAtticToSite(recordID, attic)
		except:
			logData("attic failed")
			attic = '75.5775'

		#saveTempsToDB([temp, 0, temp_hall, attic, outside], recordID)
		#for var in [temp, 0, temp_hall]:#, attic, outside]:
		#	V_T_arr.append(var)
		V_T_arr.extend([temp, 0, temp_hall])

		try:
			#add to oled
			oledStrArr[2].append('a: '+str(attic))
			#put on oled
			initOled = oledExp.driverInit()
			oledExp.write(prepareOLEDstring(oledStrArr, adjDelta, MMDD))
			logData('$ OLED contains attic $')
		except:
			logData("add attic to oled failed")
	else:
		#go back and add get attic here...maybe
		attic = '75.5775'
		#this is a failed state so might be better to not so the system has an easy run
		if temp_source == '     ** door **':
			#saveTempsToDB([0, temp, 0], recordID)
			V_T_arr.extend([0, temp, 0])
		elif temp_source == '     ** hall **':
			#saveTempsToDB([0, 0, temp], recordID)
			V_T_arr.extend([0, 0, temp])
		else:
			logData("!@#$ errorrrrrrrrr $#@!")
			############################################
			#  errorrrrrrrrr
			############################################
	V_T_arr.extend([attic, outside])

	saveV_T_ToDB(V_T_arr, recordID)

	#sendAllToSite(recordID, temp, highCutOff, lowCutOff, state, temp_hall=71.1771, outside=82.2882, attic=75.5775)
	try:
		sendAllToSite(recordID, temp, highCutOff, lowCutOff, state, temp_hall, outside, attic)
	except Exception as e:
		logData("sendAllToSite failed. temp:"+str(temp)+", highCutOff:"+str(highCutOff)+", lowCutOff:"+str(lowCutOff)+", state:"+state+", temp_hall:"+str(temp_hall)+", outside:",+str(outside)+", attic:"+str(attic))

	logData('---code run done\n')

if __name__ == '__main__':
	main()
