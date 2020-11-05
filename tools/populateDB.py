import urllib2, urllib, sqlite3, time

data_dir = '/root/'
db_name = 'db_v5.db'

def writeSettingsChanges(arr, settingsIteration):
	for i in range(len(arr)-1):
		arr[i] = str(arr[i])
	saveVar = 0
	while (saveVar < 6) and (saveVar != -1):
		try:
			conn = sqlite3.connect(data_dir+db_name)
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

def saveVarsToDB(arr, recordID):
	conn = sqlite3.connect(data_dir+db_name)
	conn.execute("INSERT INTO vars (minCooldown, maxCooldown, maxRunTime, lowCutOff, highCutOff, cooldownTime, runTime, acRunningLowCutOffRaisePercent, acRunningLowCutOffRaiseTimeMin, acOffHighCutOffLowerPercent, acOffHighCutOffLowerPercentNum2, acOffHighCutOffLowerTimeMin, acOffHighCutOffLowerTimeMinNum2, state, recordID) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7], arr[8], arr[9], arr[10], arr[11], arr[12], arr[13], recordID))
	conn.commit()
	conn.close()

def main():
	#955135 is last record in web db
	varsArr = ['5.0', '30.0', '30.0', '58.25', '60.25', '5', '0', '0.05', '10.0', '0.075', '0.1', '10.0', '25.0', 'OFF', 956000]
	saveVarsToDB(varsArr[:-1], varsArr[-1])
	print 'vars done'
	settings = ['5.0', '30.0', '30.0', '63.75', '65.75', '0.0', '0.0', '0.05', '10.0', '0.075', '0.1', '10.0', '25.0', 956000]
	writeSettingsChanges(settings[:-1], settings[-1])
	print 'settings done'

if __name__ == '__main__':
	main()

'''
todo:
	add check where it looks for a previous version and if finds one uses
		last vars entry
		last settings entry
		new recordID...maybe using rounding up to next thousand would generally be a good thing (unless already near that point in which case add a thousand maybe...?)
'''