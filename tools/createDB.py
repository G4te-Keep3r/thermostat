from mysql.connector import connect, Error

def makedb():
	try:
		with connect(
			host="localhost",
			user="ac",
			password="",
		) as connection:
			create_db_query = "CREATE DATABASE ac"
			with connection.cursor() as cursor:
				cursor.execute(create_db_query)


			show_db_query = "SHOW DATABASES"
			with connection.cursor() as cursor:
				cursor.execute(show_db_query)
				for db in cursor:
					print(db)
	except Error as e:
		print(e)

def infod():
	show_db_query = "SHOW tables"
	try:
		with connect(
			host="localhost",
			user="ac",
			password="",
			database="ac",
		) as connection:
			with connection.cursor() as cursor:
				cursor.execute(show_db_query)
				for db in cursor:
					print(db)
	except Error as e:
		print(e)


def writePersonal(arr):
	try:
		try:
			with connect(
				host="localhost",
				user="ac",
				password="",
				database="ac",
			) as connection:
				with connection.cursor() as cursor:
					cursor.execute("INSERT INTO personal (pyowm_api_key, pyowm_location, pyowmlat, pyowmlon, tzoffset) VALUES (%s, %s, %s, %s, %s)", (arr[0], arr[1], arr[2], arr[3], arr[4]))
					connection.commit()
					print('\nsettings saved')
		except Error as e:
			print(e)
	except Error as e:
		raise e


def printPersonal():
	labels = ['pyowm_api_key', 'pyowm_location', 'pyowmlat', 'pyowmlon', 'tzoffset']
	try:
		try:
			with connect(
				host="localhost",
				user="ac",
				password="",
				database="ac",
			) as connection:
				with connection.cursor() as cursor:
					cursor.execute("SELECT * FROM personal")
					records = cursor.fetchall()
					for row in records:
						for i in range(len(row)):
							print(labels[i], row[i])
		except Error as e:
			print(e)
	except Error as e:
		raise e

def createTablesDB():
	try:
		with connect(
			host="localhost",
			user="ac",
			password="",
			database="ac",
		) as connection:
			#create_db_query = "CREATE DATABASE ac"
			with connection.cursor() as cursor:
				#cursor.execute(create_db_query)

				q1 = '''CREATE TABLE temps (temp TEXT NOT NULL,
														temp_2 TEXT NOT NULL,
														temp_3 TEXT NOT NULL,
														attic TEXT NOT NULL,
														recordDT datetime NOT NULL,
														utccol datetime NOT NULL);'''
				cursor.execute(q1)
				q2 = '''CREATE TABLE weather (obj TEXT NOT NULL,
														wind TEXT NOT NULL,
														humidity TEXT NOT NULL,
														temperature TEXT NOT NULL,
														outside decimal(10,7) NOT NULL,
														recordDT datetime NOT NULL,
														utccol datetime NOT NULL);'''
				cursor.execute(q2)
				q3 = '''CREATE TABLE vars (minCooldown TEXT NOT NULL,
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
														recordDT datetime NOT NULL,
														utccol datetime NOT NULL);'''
				cursor.execute(q3)
				q4 = '''CREATE TABLE settings (minCooldown TEXT NOT NULL,
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
														settingsIteration TEXT NOT NULL,
														recordDT datetime NOT NULL);'''
				cursor.execute(q4)
				q5 = '''CREATE TABLE personal (pyowm_api_key TEXT NOT NULL,
														pyowm_location TEXT NOT NULL,
														pyowmlat TEXT NOT NULL,
														pyowmlon TEXT NOT NULL,
														tzoffset TEXT NOT NULL);'''
				cursor.execute(q5)
				q6 = '''CREATE TABLE tempsensors (priority TEXT NOT NULL,
														id TEXT NOT NULL,
														name TEXT NOT NULL);'''
				cursor.execute(q6)

	except Error as e:
		print(e)

	print ("Success")

def main():
	makedb()
	createTablesDB()

	#labels = ['pyowm_api_key', 'pyowm_location', 'pyowmlat', 'pyowmlon', 'tzoffset']
	pyowm_api_key = input('pyowm_api_key\n')
	latitude = input('latitude (how weather is found)\n')
	longitude = input('longitude (how weather is found)\n')
	tzoffset =tzoffset input('your timezone UTC value (such as -05:00 for CDT)\n')
	while len(tzoffset.split('-')[-1].split('+')[-1]) != 5:
		print('error in formatting or something')
		print('you must enter + or - followed by ##:00 where ## corresponds to your timezone')
		tzoffset =tzoffset input('your timezone UTC value (such as -05:00 for CDT)\n')
	writePersonal([pyowm_api_key, 'not currently used', latitude, longitude, "'"+tzoffset+"'"])
	print()
	printPersonal()

if __name__ == '__main__':
	main()
