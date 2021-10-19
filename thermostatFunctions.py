import os
import datetime
import pyowm

import RPi.GPIO as GPIO

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

import pyowm

from mysql.connector import connect, Error

#--------------------------------------------------------------------------
# other
#--------------------------------------------------------------------------
def getTemp(w1id):
	try:
		cmd = "cat /sys/devices/w1_bus_master1/"+w1id+"/w1_slave"
		result = os.popen(cmd).read()
		result = result[result.find('t=')+2:]
		t = int(result)/1000.0
		#C to F
		t *= 1.8
		t += 32
		return t
	except Exception as e:
		return -1

def logData(data):
	logfilename = datetime.datetime.now().strftime('/home/pi/temp-thermostat/logDir/log_%Y_%m_%d_.txt')
	with open(logfilename, 'a+') as w:
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
	#print(arr)
	#same = True
	#curent code has x=4. Instead of all or nothing try counting passes and if 75% pass
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
		elif arr[i] - arr[i+1] < 0.15:#.2: #0.36:
			#same = True and same
			passes += 1
		#else: #FAILED
		#	return False
	return passes >= (0.75*x)
	#return same
	# True => turn off
	# False => keep on


# should probably merge these 2 into 1 function "changeState or setState" that takes an argument as to if should turn it on or off

def turnOFF():
	#gpio 21
	#high = no3 #on
	#low = nc3 #off
	GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
	#Stop coming out Warnings
	GPIO.setwarnings(False)
	 
	RELAIS_1_GPIO = 21
	GPIO.setup(RELAIS_1_GPIO, GPIO.OUT)

	GPIO.output(RELAIS_1_GPIO, GPIO.LOW)


def turnON():
	#gpio 21
	#high = no3 #on
	#low = nc3 #off
	GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
	#Stop coming out Warnings
	GPIO.setwarnings(False)

	RELAIS_1_GPIO = 21
	GPIO.setup(RELAIS_1_GPIO, GPIO.OUT)

	GPIO.output(RELAIS_1_GPIO, GPIO.HIGH)


#--------------------------------------------------------------------------
# db
#--------------------------------------------------------------------------

#get vars, settings
def getV_S_FromDB(): #getVarsFromDB():, getSettngsFromDB():,,,, getLastOutsideTemp(recordID):
	arr = []
	try:
		with connect(
			host="localhost",
			user="ac",
			password="",
			database="ac",
		) as connection:
			with connection.cursor() as cursor:


				cursor.execute("SELECT * FROM vars order by recordDT DESC LIMIT 1")
				records = cursor.fetchall()
				for row in records:
					for i in range(len(row)-3):
						arr.append(float(row[i]))
					arr.append(row[-3])

				cursor.execute("SELECT * FROM settings order by settingsIteration+0 DESC LIMIT 1")
				records = cursor.fetchall()
				for row in records:
					for i in range(len(row)-1): #dont need last entry (settings iteration)
						arr.append(float(row[i]))

				cursor.execute("SELECT recordDT, outside FROM weather order by recordDT DESC LIMIT 1")
				records = cursor.fetchall()
				lastOutsideTemp = 0.0
				for row in records:
					lastOutsideTemp = float(row[1])
				arr.append(lastOutsideTemp)

	except Error as e:
		print(e)


	return arr


#save vars, temps
def saveV_T_ToDB(arr):
	tzoffset = getTZoffset()
	try:
		with connect(
			host="localhost",
			user="ac",
			password="",
			database="ac",
		) as connection:
			with connection.cursor() as cursor:
				cursor.execute("INSERT INTO vars (minCooldown, maxCooldown, maxRunTime, lowCutOff, highCutOff, cooldownTime, runTime, acRunningLowCutOffRaisePercent, acRunningLowCutOffRaiseTimeMin, acOffHighCutOffLowerPercent, acOffHighCutOffLowerPercentNum2, acOffHighCutOffLowerTimeMin, acOffHighCutOffLowerTimeMinNum2, state, recordDT, utccol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CONVERT_TZ(now(), '+00:00', "+tzoffset+"), now())", (arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7], arr[8], arr[9], arr[10], arr[11], arr[12], arr[13]))
				cursor.execute("INSERT INTO temps (temp, temp_2, temp_3, attic, recordDT, utccol) VALUES (%s, %s, %s, %s, CONVERT_TZ(now(), '+00:00', "+tzoffset+"), now())", (arr[14], arr[15], arr[16], arr[17]))
				connection.commit()
	except Error as e:
		print(e)

def getLastXtemps(x): #l8r this can have a second input to get from different probes
	arr = []
	try:
		with connect(
			host="localhost",
			user="ac",
			password="",
			database="ac",
		) as connection:
			with connection.cursor() as cursor:
				cursor.execute("SELECT recordDT, temp FROM (SELECT recordDT, temp FROM temps order by recordDT DESC LIMIT "+str(x)+") tmp ORDER BY tmp.recordDT")
				records = cursor.fetchall()
				for row in records:
					arr.append(float(row[1]))
	except Error as e:
		print(e)

	return arr


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

def getTZoffset():
	ret = "'+00:00'" #default to utc
	try:
		try:
			with connect(
				host="localhost",
				user="ac",
				password="",
				database="ac",
			) as connection:
				with connection.cursor() as cursor:
					cursor.execute("SELECT tzoffset FROM personal")
					records = cursor.fetchall()
					for row in records:
						ret = row[0]
		except Error as e:
			print(e)
	except Error as e:
		raise e

	return ret

def getTempSensors():
	ret = []
	try:
		try:
			with connect(
				host="localhost",
				user="ac",
				password="",
				database="ac",
			) as connection:
				with connection.cursor() as cursor:
					cursor.execute("SELECT * FROM tempsensors order by priority+0 asc")
					records = cursor.fetchall()
					for row in records:
						#print(row[0], row[1], row[2])
						ret.append([row[1], row[2]])
						#ret.append(row[1]) #name (row[2]) will be needed in future versions
		except Exception as e:
			print(e)
	except Error as e:
		raise e
	return ret