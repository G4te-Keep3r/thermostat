from mysql.connector import connect, Error
from thermostatFunctions import getTZoffset

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
	tzoffset = getTZoffset()
	try:
		try:
			with connect(
				host="localhost",
				user="ac",
				password="",
				database="ac",
			) as connection:
				with connection.cursor() as cursor:
					cursor.execute("INSERT INTO settings (minCooldown, maxCooldown, maxRunTime, lowCutOff, highCutOff, cooldownTime, runTime, acRunningLowCutOffRaisePercent, acRunningLowCutOffRaiseTimeMin, acOffHighCutOffLowerPercent, acOffHighCutOffLowerPercentNum2, acOffHighCutOffLowerTimeMin, acOffHighCutOffLowerTimeMinNum2, settingsIteration, recordDT) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CONVERT_TZ(now(), '+00:00', "+tzoffset+"))", (arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7], arr[8], arr[9], arr[10], arr[11], arr[12], settingsIteration))
					connection.commit()
					print('\nsettings saved, settingsIteration: '+str(settingsIteration))
		except Error as e:
			print(e)
	except Error as e:
		raise e
		return ret

def getSettngsFromDB():
	arr = []
	try:
		try:
			with connect(
				host="localhost",
				user="ac",
				password="",
				database="ac",
			) as connection:
				with connection.cursor() as cursor:
					cursor.execute("SELECT * FROM settings order by settingsIteration+0 desc LIMIT 1")
					records = cursor.fetchall()
					for row in records: #really need to find the "propper way" to do this
						for i in range(len(row)-2):
							arr.append(float(row[i]))
						arr.append(int(row[-2]))
		except Error as e:
			print(e)
	except Error as e:
		raise e
		return ret

	return arr

def printSettingsAndUpdateArr(arr):
	print('settingsIteration: '+str(arr[-1]))
	names = ['minCooldown :  ', 'maxCooldown :  ', 'maxRunTime :  ', 'lowCutOff :  ', 'highCutOff :  ', 'cooldownTime :  ', 'runTime :  ', 'acRunningLowCutOffRaisePercent :  ', 'acRunningLowCutOffRaiseTimeMin :  ', 'acOffHighCutOffLowerPercent :  ', 'acOffHighCutOffLowerPercentNum2 :  ', 'acOffHighCutOffLowerTimeMin :  ', 'acOffHighCutOffLowerTimeMinNum2 :  '] #, 'settingsIteration']
	while 1:
		for i in [3,4]:
			print(i, names[i], arr[i])
			#print(i)
			#print(names[i])
			#print(arr[i])
		action = input('\nlimit delta, 99 to save changes and exit -  ')
		######need to add ability to change delta amount between low and high
		#print not a valid int error here...
		if action == '99':
			print('sending updates to db')
			return(arr)
		else:
			delta = float(action)
			oldLow = arr[3]
			oldHigh = arr[4]
			newLow = arr[3] + delta
			newHigh = arr[4] + delta
			print(oldLow, '==>', newLow)
			print(oldHigh, '==>', newHigh)
			###setup like this for ability to add confiormation easily like changeSettings has
			###also didn't put in check for data to be valid, but trying to add a non float()-able 'action' will fail before trying to write to db, and still have to type 99 & enter

			arr[3] = newLow
			arr[4] = newHigh
			print()

def main():
	#addSettingsID()
	#updateFirstSettingItteration()
	#return

	arr = getSettngsFromDB()
	#print(arr)
	#return
	newArr = printSettingsAndUpdateArr(arr)
	writeSettingsChanges(newArr, arr[-1]+1)

	#add check where if settings not changed the save is skipped


if __name__ == '__main__':
	main()
