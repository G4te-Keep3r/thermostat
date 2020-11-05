import sqlite3

data_dir = '/root/'
db_name = 'db_v5.db'

def createTableDB():
	conn = sqlite3.connect(data_dir+db_name)
	conn.execute('''CREATE TABLE temps (temp TEXT NOT NULL,
											temp_door TEXT NOT NULL,
											temp_hall TEXT NOT NULL,
											attic TEXT NOT NULL,
											outside TEXT NOT NULL,
											recordID INT NOT NULL);''')
	#conn.execute("ALTER TABLE temps ADD outside TEXT")
	conn.execute('''CREATE TABLE weather (obj TEXT NOT NULL,
											wind TEXT NOT NULL,
											humidity TEXT NOT NULL,
											temperature TEXT NOT NULL,
											outside DOUBLE NOT NULL,
											recordID INT NOT NULL);''')
	conn.execute('''CREATE TABLE datetime (datetime TEXT NOT NULL,
											recordID INT NOT NULL);''')
	conn.execute('''CREATE TABLE vars (minCooldown TEXT NOT NULL,
											maxCooldown TEXT NOT NULL,
											maxRunTime TEXT NOT NULL,
											lowCutoff TEXT NOT NULL,
											highCutoff TEXT NOT NULL,
											cooldownTime TEXT NOT NULL,
											runTime TEXT NOT NULL,
											acRunningLowCutOffRaisePercent TEXT NOT NULL,
											acRunningLowCutOffRaiseTimeMin TEXT NOT NULL,
											acOffHighCutOffLowerPercent TEXT NOT NULL,
											acOffHighCutOffLowerPercentNum2 TEXT NOT NULL,
											acOffHighCutOffLowerTimeMin TEXT NOT NULL,
											acOffHighCutOffLowerTimeMinNum2 TEXT NOT NULL,
											state TEXT NOT NULL,
											recordID INT NOT NULL);''') #l8r this will be date and time based
	#settings table...or could be different db so that less likely of a collision of access attemps...
	conn.execute('''CREATE TABLE settings (minCooldown TEXT NOT NULL,
											maxCooldown TEXT NOT NULL,
											maxRunTime TEXT NOT NULL,
											lowCutoff TEXT NOT NULL,
											highCutoff TEXT NOT NULL,
											cooldownTime TEXT NOT NULL,
											runTime TEXT NOT NULL,
											acRunningLowCutOffRaisePercent TEXT NOT NULL,
											acRunningLowCutOffRaiseTimeMin TEXT NOT NULL,
											acOffHighCutOffLowerPercent TEXT NOT NULL,
											acOffHighCutOffLowerPercentNum2 TEXT NOT NULL,
											acOffHighCutOffLowerTimeMin TEXT NOT NULL,
											acOffHighCutOffLowerTimeMinNum2 TEXT NOT NULL,
											settingsIteration TEXT NOT NULL);''')
	conn.close()
	print "Success"

def main():
	createTableDB()

if __name__ == '__main__':
	main()