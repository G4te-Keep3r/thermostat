from time import time, sleep
from os import popen, system, path
from OmegaExpansion import relayExp
from OmegaExpansion import oledExp
import urllib2, urllib, sqlite3
import datetime
import pyowm

data_dir = '/tmp/mounts/USB-A/4/'
db_name = 'db_v4.db'

def logData(data):
	with open(data_dir+'log.txt', 'a+') as w:
		w.write(data)
		w.write('\n')

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

def main():
	varsArr = getVarsFromDB()

	minCooldown = varsArr[0]
	maxCooldown = varsArr[1]
	maxRunTime = varsArr[2]
	lowCutOff = varsArr[3] ## ones that are variable and change
	highCutOff = varsArr[4] ##
	cooldownTime = 0
	runTime = 0
	acRunningLowCutOffRaisePercent = varsArr[7]
	acRunningLowCutOffRaiseTimeMin = varsArr[8]
	acOffHighCutOffLowerPercent = varsArr[9]
	acOffHighCutOffLowerPercentNum2 = varsArr[10]
	acOffHighCutOffLowerTimeMin = varsArr[11]
	acOffHighCutOffLowerTimeMinNum2 = varsArr[12]
	state = 'OFF'

	turnOFF()

	saveVarsToDB([minCooldown, maxCooldown, maxRunTime, lowCutOff, highCutOff, cooldownTime, runTime, acRunningLowCutOffRaisePercent, acRunningLowCutOffRaiseTimeMin, acOffHighCutOffLowerPercent, acOffHighCutOffLowerPercentNum2, acOffHighCutOffLowerTimeMin, acOffHighCutOffLowerTimeMinNum2, state], varsArr[-1])

	logData('---code run done***turnoffac.py***') #remove or give different text

if __name__ == '__main__':
	main()
