import sqlite3, time

#not implemented because this is (currently) always run from terminal and not from a system call of any sort
#when ability to change settings from website is added, will probably need to be added below
data_dir = '/tmp/mounts/USB-A/4/'

db_name = 'db_v4.db'

def writeSettingsChanges(arr, settingsIteration):
	for i in range(len(arr)-1):
		arr[i] = str(arr[i])
	saveVar = 0
	while (saveVar < 6) and (saveVar != -1):
		try:
			conn = sqlite3.connect(db_name)
			conn.execute("INSERT INTO settings (minCooldown, maxCooldown, maxRunTime, lowCutOff, highCutOff, cooldownTime, runTime, acRunningLowCutOffRaisePercent, acRunningLowCutOffRaiseTimeMin, acOffHighCutOffLowerPercent, acOffHighCutOffLowerPercentNum2, acOffHighCutOffLowerTimeMin, acOffHighCutOffLowerTimeMinNum2, settingsIteration) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7], arr[8], arr[9], arr[10], arr[11], arr[12], settingsIteration))
			conn.commit()
			saveVar = -1
		except:
			saveVar += 1
			print 'save fail,', saveVar
			time.sleep(5)
	if saveVar == -1:
		print '\nsettings saved'
		conn.close()
	else:
		print 'SETTINGS NOT SAVED'

def getSettngsFromDB():
	arr = []
	conn = sqlite3.connect(db_name)
	cur = conn.execute("SELECT * FROM settings order by settingsIteration DESC LIMIT 1")
	for row in cur:
		for i in range(len(row)-1):
			arr.append(float(row[i]))
		arr.append(int(row[-1]))
	conn.close()
	return arr

def printSettingsAndUpdateArr(arr):
	names = ['minCooldown :  ', 'maxCooldown :  ', 'maxRunTime :  ', 'lowCutOff :  ', 'highCutOff :  ', 'cooldownTime :  ', 'runTime :  ', 'acRunningLowCutOffRaisePercent :  ', 'acRunningLowCutOffRaiseTimeMin :  ', 'acOffHighCutOffLowerPercent :  ', 'acOffHighCutOffLowerPercentNum2 :  ', 'acOffHighCutOffLowerTimeMin :  ', 'acOffHighCutOffLowerTimeMinNum2 :  '] #, 'settingsIteration']
	while 1:
		for i in range(len(names)):
			print i, names[i], arr[i]
		action = raw_input('\n# of setting to change, 99 to save changes and exit -  ')
		#print not a valid int error here...
		if action == '99':
			print 'sending updates to db'
			return arr
		elif int(action) >= len(names):
			print "not a valid choice"
		else:
			action = int(action)
			print 'current '+names[action]+str(arr[action])
			newVal = raw_input('enter new value  ')
			confirm = raw_input('is '+newVal+' correct [Y / N] ')
			if confirm == 'Y' or confirm == 'y':
				arr[action] = float(newVal)
				print
			else:
				print 'try again\n'

def main():
	arr = getSettngsFromDB()
	newArr = printSettingsAndUpdateArr(arr)
	writeSettingsChanges(newArr, arr[-1]+1)

if __name__ == '__main__':
	main()
