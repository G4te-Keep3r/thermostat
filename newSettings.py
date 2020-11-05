import sqlite3, time

db_name = 'db_v5.db'

def updateFirstSettingItteration():
	conn = sqlite3.connect(db_name)
	cur = conn.execute("UPDATE settings SET settingsIteration = 0")# WHERE settingsIteration = None")
	#conn.commit()
	conn.close()

def addSettingsID():
	conn = sqlite3.connect(db_name)
	cur = conn.execute("ALTER TABLE settings ADD COLUMN 'settingsIteration' INT")
	#conn.commit()
	conn.close()

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
	for row in cur: #really need to find the "propper way" to do this
		for i in range(len(row)-1):
			arr.append(float(row[i]))
		arr.append(int(row[-1]))
	conn.close()
	return arr

def printSettingsAndUpdateArr(arr):
	names = ['minCooldown :  ', 'maxCooldown :  ', 'maxRunTime :  ', 'lowCutOff :  ', 'highCutOff :  ', 'cooldownTime :  ', 'runTime :  ', 'acRunningLowCutOffRaisePercent :  ', 'acRunningLowCutOffRaiseTimeMin :  ', 'acOffHighCutOffLowerPercent :  ', 'acOffHighCutOffLowerPercentNum2 :  ', 'acOffHighCutOffLowerTimeMin :  ', 'acOffHighCutOffLowerTimeMinNum2 :  '] #, 'settingsIteration']
	while 1:
		for i in [3,4]:
			print i, names[i], arr[i]
		action = raw_input('\nlimit delta, 99 to save changes and exit -  ')
		######need to add ability to change delta amount between low and high
		#print not a valid int error here...
		if action == '99':
			print 'sending updates to db'
			return arr
		else:
			delta = float(action)
			oldLow = arr[3]
			oldHigh = arr[4]
			newLow = arr[3] + delta
			newHigh = arr[4] + delta
			print oldLow, '==>', newLow
			print oldHigh, '==>', newHigh
			###setup like this for ability to add confiormation easily like changeSettings has
			###also didn't put in check for data to be valid, but trying to add a non float()-able 'action' will fail before trying to write to db, and still have to type 99 & enter

			arr[3] = newLow
			arr[4] = newHigh
			print

def main():
	#addSettingsID()
	#updateFirstSettingItteration()
	#return

	arr = getSettngsFromDB()
	newArr = printSettingsAndUpdateArr(arr)
	writeSettingsChanges(newArr, arr[-1]+1)

if __name__ == '__main__':
	main()

'''
to do:
	have settings iteration equal the recordID when they were set...maybe
	it would make correlationg vars/temps and settings easier
'''