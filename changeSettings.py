from mysql.connector import connect, Error
from thermostatFunctions import getTZoffset

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
					#print('inserted')
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
					for row in records:
						for i in range(len(row)-2):
							arr.append(float(row[i]))
						arr.append(int(row[-2]))
		except Error as e:
			print(e)
	except Error as e:
		raise e
		return ret
	#return ret

	return arr

def printSettingsAndUpdateArr(arr):
	names = ['minCooldown :  ', 'maxCooldown :  ', 'maxRunTime :  ', 'lowCutOff :  ', 'highCutOff :  ', 'cooldownTime :  ', 'runTime :  ', 'acRunningLowCutOffRaisePercent :  ', 'acRunningLowCutOffRaiseTimeMin :  ', 'acOffHighCutOffLowerPercent :  ', 'acOffHighCutOffLowerPercentNum2 :  ', 'acOffHighCutOffLowerTimeMin :  ', 'acOffHighCutOffLowerTimeMinNum2 :  '] #, 'settingsIteration']
	while 1:
		for i in range(len(names)):
			print(i, names[i], arr[i])
		action = input('\n# of setting to change, 99 to save changes and exit -  ')
		#print not a valid int error here...
		if action == '99':
			print('sending updates to db')
			return arr
		elif int(action) >= len(names):
			print("not a valid choice")
		else:
			action = int(action)
			print('current '+names[action]+str(arr[action]))
			newVal = input('enter new value  ')
			confirm = input('is '+newVal+' correct [Y / N] ')
			if confirm == 'Y' or confirm == 'y':
				arr[action] = float(newVal)
				print()
			else:
				print('try again\n')

def main():
	arr = getSettngsFromDB()
	newArr = printSettingsAndUpdateArr(arr)
	writeSettingsChanges(newArr, arr[-1]+1)

if __name__ == '__main__':
	main()
