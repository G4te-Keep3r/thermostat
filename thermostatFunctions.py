from os import popen, path
from OmegaExpansion import relayExp
import urllib2, urllib, sqlite3
import datetime
import pyowm

data_dir = '/tmp/mounts/USB-A/4/'
db_name = 'db_v4.db'
t_id1 = "28-0516a02c71ff"

def getLastOutsideTemp(recordID):
	conn = sqlite3.connect(data_dir+db_name)
	cur = conn.execute("SELECT outside FROM weather WHERE recordID = "+str(recordID-1))
	ret = 0.0
	for row in cur:
		ret = float(row[0])
	conn.close()
	return ret

def getWeather(recordID):
	ret = ''
	try:
		owm = pyowm.OWM('API KEY HERE')
		observation = owm.weather_at_id(4699540)
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

def sendToSite(recordID, temp, highCutOff, lowCutOff):
	try:
		mydata=[('recordID',str(recordID)),('temp',str(temp)),('highCutOff',str(highCutOff)),('lowCutOff',str(lowCutOff)),('temp_hall','71.1771'),('outside','82.2882'),('attic','75.5775')]
		mydata=urllib.urlencode(mydata)
		path='http://192.168.2.236/saveTempToDB.php'
		req=urllib2.Request(path, mydata)
		req.add_header("Content-type", "application/x-www-form-urlencoded")
		page=urllib2.urlopen(req).read()
	except Exception, e:
		raise e

def sendHallToSite(recordID, temp_hall):
	try:
		mydata=[('recordID',str(recordID)),('temp_hall',str(temp_hall))]
		mydata=urllib.urlencode(mydata)
		path='http://192.168.2.236/saveHallTempToDB.php'
		req=urllib2.Request(path, mydata)
		req.add_header("Content-type", "application/x-www-form-urlencoded")
		page=urllib2.urlopen(req).read()
	except Exception, e:
		raise e

def sendAtticToSite(recordID, attic):
	try:
		mydata=[('recordID',str(recordID)),('attic',str(attic))]
		mydata=urllib.urlencode(mydata)
		path='http://192.168.2.236/saveAtticToDB.php'
		req=urllib2.Request(path, mydata)
		req.add_header("Content-type", "application/x-www-form-urlencoded")
		page=urllib2.urlopen(req).read()
	except Exception, e:
		raise e

def sendOutsideToSite(recordID, outside):
	try:
		mydata=[('recordID',str(recordID)),('outside',str(outside))]
		mydata=urllib.urlencode(mydata)
		path='http://192.168.2.236/saveOutsideTempToDB.php'
		req=urllib2.Request(path, mydata)
		req.add_header("Content-type", "application/x-www-form-urlencoded")
		page=urllib2.urlopen(req).read()
	except Exception, e:
		raise e

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
	with open(data_dir+'log.txt', 'a+') as w:
		w.write(data)
		w.write('\n')

def saveTempsToDB(arr, recordID):
	conn = sqlite3.connect(data_dir+db_name)
	conn.execute("INSERT INTO temps (temp, temp_door, temp_hall, recordID) VALUES (?, ?, ?, ?)", (arr[0], arr[1], arr[2], recordID))
	conn.execute("INSERT INTO datetime (datetime, recordID) VALUES (?, ?)", (str(datetime.datetime.now()), recordID))
	conn.commit()
	conn.close()

def saveHallTempToDB(temp_hall, recordID):
	conn = sqlite3.connect(data_dir+db_name)
	conn.execute("UPDATE temps SET temp_hall = ? WHERE recordID = ?", (temp_hall, recordID))
	conn.commit()
	conn.close()

def saveAtticToDB(attic, recordID):
	conn = sqlite3.connect(data_dir+db_name)
	conn.execute("UPDATE temps SET attic = ? WHERE recordID = ?", (attic, recordID))
	conn.commit()
	conn.close()

def saveOutsideTempToDB(outside, recordID):
	conn = sqlite3.connect(data_dir+db_name)
	conn.execute("UPDATE temps SET outside = ? WHERE recordID = ?", (outside, recordID))
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

def coolingLimitReached(x, aboveHigh, runTime):
	if runTime<10:
		return False

	arr = getLastXtemps(x)
	#same = True
	#curent code has x=4. Instead of all or nothing try coutning passes and if 75% pass
	#need to make simulator to virtually test all the variations
	passes = 0
	for i in range(x-1):
		# % diff is a problem as they get closer
		# trying where if same or delta is < 0.15

		#are they the same?
		if arr[i]==arr[i+1]:
			#same = True and same
			passes += 1
		#or is the delta < 0.15
		elif arr[i] - arr[i+1] < 0.11 and arr[i] - arr[i+1] >= 0:
			#same = True and same
			passes += 1
		#else: #FAILED
		#	return False
	return passes >= (0.75*x)
	#return same
	# True => turn off
	# False => keep on

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

def turnON():
	relayAddr = 7
	initRelay = relayExp.driverInit(relayAddr)
	if relayExp.checkInit(relayAddr):
		logData('relay is init')
	else:
		logData('ERR relay not init')
		exit()
	relayExp.setChannel(relayAddr, 0, 1)

def prepareOLEDstring(arr):
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
	oledStr += str(arr[-1][0]) + '  ' + arr[-1][1] + '  ' + str(arr[-1][2])
	return oledStr