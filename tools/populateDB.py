from mysql.connector import connect, Error

def writeSettingsChanges(arr, settingsIteration):
	try:
		try:
			with connect(
				host="localhost",
				user="ac",
				password="",
				database="ac",
			) as connection:
				with connection.cursor() as cursor:
					cursor.execute("INSERT INTO settings (minCooldown, maxCooldown, maxRunTime, lowCutOff, highCutOff, cooldownTime, runTime, acRunningLowCutOffRaisePercent, acRunningLowCutOffRaiseTimeMin, acOffHighCutOffLowerPercent, acOffHighCutOffLowerPercentNum2, acOffHighCutOffLowerTimeMin, acOffHighCutOffLowerTimeMinNum2, settingsIteration) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7], arr[8], arr[9], arr[10], arr[11], arr[12], settingsIteration))
					connection.commit()
					print('\nsettings saved')
		except Error as e:
			print(e)
	except Error as e:
		raise e

def saveVarsToDB(arr):
	try:
		try:
			with connect(
				host="localhost",
				user="ac",
				password="",
				database="ac",
			) as connection:
				with connection.cursor() as cursor:
					cursor.execute("INSERT INTO vars (minCooldown, maxCooldown, maxRunTime, lowCutOff, highCutOff, cooldownTime, runTime, acRunningLowCutOffRaisePercent, acRunningLowCutOffRaiseTimeMin, acOffHighCutOffLowerPercent, acOffHighCutOffLowerPercentNum2, acOffHighCutOffLowerTimeMin, acOffHighCutOffLowerTimeMinNum2, state, recordDT) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())", (arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7], arr[8], arr[9], arr[10], arr[11], arr[12], arr[13]))
					connection.commit()
					print('\nsettings saved')
		except Error as e:
			print(e)
	except Error as e:
		raise e

def main():
	varsArr = ['5.0', '30.0', '30.0', '58.25', '60.25', '5', '0', '0.05', '10.0', '0.075', '0.1', '10.0', '25.0', 'OFF']
	saveVarsToDB(varsArr)
	print('vars done')
	settings = ['5.0', '30.0', '30.0', '63.75', '65.75', '0.0', '0.0', '0.05', '10.0', '0.075', '0.1', '10.0', '25.0', 0]
	writeSettingsChanges(settings[:-1], settings[-1])
	print('settings done')

if __name__ == '__main__':
	main()
