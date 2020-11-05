from os import popen, path
from OmegaExpansion import relayExp
import urllib2, urllib, sqlite3
import datetime
import pyowm

data_dir = '/root/'
db_name = 'db_v5.db'
t_id1 = "28-0516a02c71ff"
ip = '192.168.2.236'
pyowm_api_key = 'yours here'
pyowm_location = yourshere

#--------------------------------------------------------------------------
# other
#--------------------------------------------------------------------------
def getTemp(w1id = t_id1):
	try:
		cmd = "cat /sys/devices/w1_bus_master1/"+w1id+"/w1_slave"
		result = popen(cmd).read()
		result = result[result.find('t=')+2:]
		t = int(result)/1000.0
		#C to F
		t *= 1.8
		t += 32
		return t
	except Exception, e:
		return -1

def logData(data):
	logfilename = datetime.datetime.now().strftime('log_%Y_%m_%d_.txt')
	with open(data_dir+logfilename, 'a+') as w:
		w.write(data)
		w.write('\n')

#x is number of last temps to look at...change name to something like history_depth?
def coolingLimitReached(x, aboveHigh, runTime):
	#############################################
	#  also safty check to not damage unit
	#############################################
	#######return False
	if runTime<10:
		return False
	#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
	#                                                min run time is a setting....should not be hard coded
	#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
	#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
	#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
	#                                                nevermind........min cooldown and max run are in settings but min run is not...maybe it should be?
	#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
	#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

	arr = getLastXtemps(x)
	#same = True
	#curent code has x=4. Instead of all or nothing try coutning passes and if 75% pass
	#need to make simulator to virtually test all the variations
	passes = 0
	for i in range(x-1):
		# % diff is a problem as they get closer
		# trying where if same or delta is < 0.15

		#are they the same? / got hotter...?
		if arr[i] <= arr[i+1]:
			#same = True and same
			passes += 1
		#or is the delta < 0.15
		#elif arr[i] - arr[i+1] < 0.11 and arr[i] - arr[i+1] >= 0:
		elif arr[i] - arr[i+1] < .2: #0.36:
			#same = True and same
			passes += 1
		#else: #FAILED
		#	return False
	return passes >= (0.75*x)
	#return same
	# True => turn off
	# False => keep on

def turnOFF():
	relayAddr = 7
	initRelay = relayExp.driverInit(relayAddr)
	if relayExp.checkInit(relayAddr):
		logData('relay is init')
	else:
		logData('ERR relay not init')
		exit()
	#when you init the relay it turns it off
	#relayExp.setChannel(relayAddr, 0, 0)

	'''   only on pro model   '''
	#set led to red (not full power)
	#echo -en "\x00\x00\x00" > /dev/ledchain2
	#cmd = "echo -en \"\\x80\\x00\\x00\" > /dev/ledchain2"
	#popen(cmd)

def turnON():
	relayAddr = 7
	initRelay = relayExp.driverInit(relayAddr)
	if relayExp.checkInit(relayAddr):
		logData('relay is init')
	else:
		logData('ERR relay not init')
		exit()
	relayExp.setChannel(relayAddr, 0, 1)

	'''   only on pro model   '''
	#set led to blue (not full power)
	#echo -en "\x00\x00\x00" > /dev/ledchain2
	#cmd = "echo -en \"\\x00\\x00\\x80\" > /dev/ledchain2"
	#popen(cmd)

def prepareOLEDstring(arr, adjDelta, MMDD): #adjDelta as new var so dont have to go change all the [-1] and might not stay
	oledStr = ''
	for data in arr[:-1]: #last line 3 col but with hard coded spaces
		if data == arr[5]:
			#right align source, which is currently the only line containing only a right aligned thing
			lineFill = ' '*(21 - len(data[0]))
			oledStr += lineFill
			oledStr += data[0]
		else:
			if len(data) == 1:
				#assume left align
				oledStr += data[0]
				lineFill = ' '*(21 - len(data[0]))
				oledStr += lineFill

			else:#if: len(data) == 2:
				#later maybe add ability to do 3 cols or whatever too
				dataA = data[0]
				dataB = data[1]
				lineFill = ' '*(21 - (len(dataA)+len(dataB)))
				oledStr += dataA
				oledStr += lineFill
				oledStr += dataB
	lastLine = ''
	#try 3 decimal points
	if len(str(arr[-1][0])) > 5:
		#comma instead of period means truncated number (rounded)...but will need to make a custom rounding function al python doesnt alwayys round floats correctly
		tmp = round(arr[-1][0], 3)
		tmp = str(tmp)
		tmp = tmp.split('.')
		tmp = ','.join(tmp)
		lastLine += tmp
	else:
		lastLine += str(arr[-1][0])

	lastLine += '  ' + arr[-1][1] + '  '

	if len(str(arr[-1][2])) > 5:
		#comma instead of period means truncated number (rounded)...but will need to make a custom rounding function al python doesnt alwayys round floats correctly
		tmp = round(arr[-1][2], 3)
		tmp = str(tmp)
		tmp = tmp.split('.')
		tmp = ','.join(tmp)
		lastLine += tmp
	else:
		lastLine += str(arr[-1][2])

	#oledStr += str(arr[-1][0]) + '  ' + arr[-1][1] + '  ' + str(arr[-1][2])
	oledStr += lastLine
	lineFill = ' '*(21 - len(lastLine))
	oledStr += lineFill

	#with spacing like so, should have an extra line at the bottom that does not need to be used as overflow
	#oledStr += '  ' + str(adjDelta)
	oledStr += '  ' + str(adjDelta) + ' '*(19 - (len(str(adjDelta))+len(MMDD))) + MMDD

	return oledStr


#--------------------------------------------------------------------------
# website / graphs
#--------------------------------------------------------------------------
def sendAllToSite(recordID, temp, highCutOff, lowCutOff, state, temp_hall=71.1771, outside=82.2882, attic=75.5775):
	#state ON = 65
	#state OFF = 75
	#refine later?
	if state == "ON":
		state = 65
	else:
		state = 75

	try:
		mydata=[('recordID',str(recordID)),('temp',str(temp)),('highCutOff',str(highCutOff)),('lowCutOff',str(lowCutOff)),('temp_hall',str(temp_hall)),('outside',str(outside)),('attic',str(attic)), ('state',str(state))]
		mydata=urllib.urlencode(mydata)
		path='http://'+ip+'/saveTempToDB.php'
		req=urllib2.Request(path, mydata)
		req.add_header("Content-type", "application/x-www-form-urlencoded")
		page=urllib2.urlopen(req).read()
	except Exception, e:
		raise e


#--------------------------------------------------------------------------
# db
#--------------------------------------------------------------------------
##### consider passing ALL weather data back, and then store in db with saveV_T_ToDB
def getWeather(recordID):
	ret = ''
	try:
		owm = pyowm.OWM(pyowm_api_key)
		observation = owm.weather_at_id(pyowm_location)
		w = observation.get_weather()
		obj = str(w)
		wind = str(w.get_wind())
		humidity = str(w.get_humidity())
		temperature = str(w.get_temperature('fahrenheit'))
		ret = w.get_temperature('fahrenheit')['temp']
		try:
			conn = sqlite3.connect(data_dir+db_name)
			conn.execute("INSERT INTO weather (obj, wind, humidity, temperature, outside, recordID) VALUES (?, ?, ?, ?, ?, ?)", (obj, wind, humidity, temperature, ret, recordID))
			conn.commit()
			conn.close()
		except Exception, e:
			raise e
			return ret
	except Exception, e:
		raise e
		return ret
	return ret

#get vars, settings
def getV_S_FromDB(): #getVarsFromDB():, getSettngsFromDB():,,,, getLastOutsideTemp(recordID):
	arr = []
	conn = sqlite3.connect(data_dir+db_name)

	cur = conn.execute("SELECT * FROM vars order by recordID DESC LIMIT 1")
	for row in cur:
		for i in range(len(row)-2):
			arr.append(float(row[i]))
		arr.append(row[-2])
		arr.append(int(row[-1]) + 1)

	cur = conn.execute("SELECT * FROM settings order by settingsIteration DESC LIMIT 1")
	for row in cur:
		for i in range(len(row)):
			arr.append(float(row[i]))

	recordID = arr[14]
	cur = conn.execute("SELECT outside FROM weather WHERE recordID = "+str(recordID-1))
	lastOutsideTemp = 0.0
	for row in cur:
		lastOutsideTemp = float(row[0])
	arr.append(lastOutsideTemp)

	conn.close()
	return arr

def get_last_recordID():
	ret = 0
	conn = sqlite3.connect(data_dir+db_name)

	cur = conn.execute("SELECT recordID FROM vars order by recordID DESC LIMIT 1")
	for row in cur:
		ret = int(row[0])

	conn.close()
	return arr

#save vars, temps
def saveV_T_ToDB(arr, recordID): #saveVarsToDB(arr, recordID):, saveTempsToDB(arr, recordID):
	conn = sqlite3.connect(data_dir+db_name)
	conn.execute("INSERT INTO vars (minCooldown, maxCooldown, maxRunTime, lowCutOff, highCutOff, cooldownTime, runTime, acRunningLowCutOffRaisePercent, acRunningLowCutOffRaiseTimeMin, acOffHighCutOffLowerPercent, acOffHighCutOffLowerPercentNum2, acOffHighCutOffLowerTimeMin, acOffHighCutOffLowerTimeMinNum2, state, recordID) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7], arr[8], arr[9], arr[10], arr[11], arr[12], arr[13], recordID))
	conn.execute("INSERT INTO temps (temp, temp_door, temp_hall, attic, outside, recordID) VALUES (?, ?, ?, ?, ?, ?)", (arr[14], arr[15], arr[16], arr[17], arr[18], recordID))
	conn.execute("INSERT INTO datetime (datetime, recordID) VALUES (?, ?)", (str(datetime.datetime.now()), recordID))
	conn.commit()
	conn.close()

def getLastXtemps(x): #l8r this can have a second input to get from different probes
	arr = []
	conn = sqlite3.connect(data_dir+db_name)
	cur = conn.execute("SELECT recordID, temp FROM (SELECT recordID, temp FROM temps order by recordID DESC LIMIT "+str(x)+") tmp ORDER BY tmp.recordID")
	for row in cur:
		arr.append(float(row[1]))
	conn.close()
	return arr


#######################################################################################
#               retired                                                               #
#######################################################################################
def saveOutsideTempToDB(outside, recordID):
	conn = sqlite3.connect(data_dir+db_name)
	conn.execute("UPDATE temps SET outside = ? WHERE recordID = ?", (outside, recordID))
	conn.commit()
	conn.close()

def saveAtticToDB(attic, recordID):
	conn = sqlite3.connect(data_dir+db_name)
	conn.execute("UPDATE temps SET attic = ? WHERE recordID = ?", (attic, recordID))
	conn.commit()
	conn.close()

def saveHallTempToDB(temp_hall, recordID):
	conn = sqlite3.connect(data_dir+db_name)
	conn.execute("UPDATE temps SET temp_hall = ? WHERE recordID = ?", (temp_hall, recordID))
	conn.commit()
	conn.close()

def sendHallToSite(recordID, temp_hall):
	try:
		mydata=[('recordID',str(recordID)),('temp_hall',str(temp_hall))]
		mydata=urllib.urlencode(mydata)
		path='http://'+ip+'/saveHallTempToDB.php'
		req=urllib2.Request(path, mydata)
		req.add_header("Content-type", "application/x-www-form-urlencoded")
		page=urllib2.urlopen(req).read()
	except Exception, e:
		raise e

def sendAtticToSite(recordID, attic):
	try:
		mydata=[('recordID',str(recordID)),('attic',str(attic))]
		mydata=urllib.urlencode(mydata)
		path='http://'+ip+'/saveAtticToDB.php'
		req=urllib2.Request(path, mydata)
		req.add_header("Content-type", "application/x-www-form-urlencoded")
		page=urllib2.urlopen(req).read()
	except Exception, e:
		raise e

def sendOutsideToSite(recordID, outside):
	try:
		mydata=[('recordID',str(recordID)),('outside',str(outside))]
		mydata=urllib.urlencode(mydata)
		path='http://'+ip+'/saveOutsideTempToDB.php'
		req=urllib2.Request(path, mydata)
		req.add_header("Content-type", "application/x-www-form-urlencoded")
		page=urllib2.urlopen(req).read()
	except Exception, e:
		raise e

def sendToSite(recordID, temp, highCutOff, lowCutOff, state):
	#state ON = 65
	#state OFF = 75
	#refine later?
	if state == "ON":
		state = 65
	else:
		state = 75

	try:
		mydata=[('recordID',str(recordID)),('temp',str(temp)),('highCutOff',str(highCutOff)),('lowCutOff',str(lowCutOff)),('temp_hall','71.1771'),('outside','82.2882'),('attic','75.5775'), ('state',str(state))]
		mydata=urllib.urlencode(mydata)
		path='http://'+ip+'/saveTempToDB.php'
		req=urllib2.Request(path, mydata)
		req.add_header("Content-type", "application/x-www-form-urlencoded")
		page=urllib2.urlopen(req).read()
	except Exception, e:
		raise e

def getVarsFromDB():
	arr = []
	conn = sqlite3.connect(data_dir+db_name)
	cur = conn.execute("SELECT * FROM vars order by recordID DESC LIMIT 1")
	for row in cur:
		for i in range(len(row)-2):
			arr.append(float(row[i]))
		arr.append(row[-2])
		arr.append(int(row[-1]) + 1)
	conn.close()
	return arr

def getSettngsFromDB():
	arr = []
	conn = sqlite3.connect(data_dir+db_name)
	cur = conn.execute("SELECT * FROM settings order by settingsIteration DESC LIMIT 1")
	for row in cur:
		for i in range(len(row)):
			arr.append(float(row[i]))
	conn.close()
	return arr

def saveVarsToDB(arr, recordID):
	conn = sqlite3.connect(data_dir+db_name)
	conn.execute("INSERT INTO vars (minCooldown, maxCooldown, maxRunTime, lowCutOff, highCutOff, cooldownTime, runTime, acRunningLowCutOffRaisePercent, acRunningLowCutOffRaiseTimeMin, acOffHighCutOffLowerPercent, acOffHighCutOffLowerPercentNum2, acOffHighCutOffLowerTimeMin, acOffHighCutOffLowerTimeMinNum2, state, recordID) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7], arr[8], arr[9], arr[10], arr[11], arr[12], arr[13], recordID))
	conn.commit()
	conn.close()

def saveTempsToDB(arr, recordID):
	conn = sqlite3.connect(data_dir+db_name)
	#conn.execute("INSERT INTO temps (temp, temp_door, temp_hall, attic, outside, recordID) VALUES (?, ?, ?, ?, ?, ?)", (arr[0], arr[1], arr[2], '75.5775', '85.5885', recordID))
	conn.execute("INSERT INTO temps (temp, temp_door, temp_hall, attic, outside, recordID) VALUES (?, ?, ?, ?, ?, ?)", (arr[0], arr[1], arr[2], arr[3], arr[4], recordID))
	conn.execute("INSERT INTO datetime (datetime, recordID) VALUES (?, ?)", (str(datetime.datetime.now()), recordID))
	conn.commit()
	conn.close()

def getLastOutsideTemp(recordID):
	conn = sqlite3.connect(data_dir+db_name)
	cur = conn.execute("SELECT outside FROM weather WHERE recordID = "+str(recordID-1))
	ret = 0.0
	for row in cur:
		ret = float(row[0])
	conn.close()
	return ret
#######################################################################################
#######################################################################################
