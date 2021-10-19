from mysql.connector import connect, Error
import os

def getNewTempSensors(knownSensors):
	'''
	the idea is to return the 1 newly added sensor
	if multiple are added at once, idk what order it will grab them in
	'''
	knownSensors.append('w1_bus_master1') #cleaner than if below

	try:
		cmd = "ls /sys/bus/w1/devices"
		result = os.popen(cmd).read()
		for line in result.split():
			if line not in knownSensors:
				return line
		return "missing"
	except Exception as e:
		return -1

def writeTempSensors(arr):
	try:
		try:
			with connect(
				host="localhost",
				user="ac",
				password="",
				database="ac",
			) as connection:
				with connection.cursor() as cursor:
					cursor.execute("INSERT INTO tempsensors (priority, id, name) VALUES (%s, %s, %s)", (arr[0], arr[1], arr[2]))
					connection.commit()
					print('\nsettings saved')
		except Exception as e:
			print(e)
	except Error as e:
		raise e

def printTempSensors():
	try:
		try:
			with connect(
				host="localhost",
				user="ac",
				password="",
				database="ac",
			) as connection:
				with connection.cursor() as cursor:
					cursor.execute("SELECT * FROM tempsensors")
					records = cursor.fetchall()
					for row in records:
						print(row[0], row[1], row[2])
		except Exception as e:
			print(e)
	except Error as e:
		raise e

def addingSensors():
	print('connect your primary sensor')
	print('if you have others connected, disconnect them')
	input('ENTER when done')

	knownSensors = [] #init, so new, so none yet
	sensorNames = []
	newtemp = getNewTempSensors(knownSensors)
	if newtemp == -1:
		print("error")
		return newtemp
	if newtemp == "missing":
		print("No temp sensors found.")
		return newtemp

	#when it is made dynamic to handle more/less than 4 sensors, this will NEED to be updated
	#main
	knownSensors.append[newtemp]
	sensorNames.append(input("name for primary sensor: "))

	#secondary
	print('plug in your secondary sensor. Primarily this serves as a backup/failover, but is also logged/graphed')
	input("ENTER when done")
	newtemp = getNewTempSensors(knownSensors)
	while newtemp in [-1, "missing"]:
		if newtemp == -1:
			print("error")
		if newtemp == "missing":
			print("No temp sensors found.")
		print("disconnect and reconnect the sensor")
		input("ENTER when done")
		newtemp = getNewTempSensors(knownSensors)

	knownSensors.append[newtemp]
	sensorNames.append(input("name for secondary sensor: "))

	#tertiary
	print('plug in your tertiary sensor. Primarily this serves as a backup/failover if main and secondary both fail/error, but is also logged/graphed')
	input("ENTER when done")
	newtemp = getNewTempSensors(knownSensors)
	while newtemp in [-1, "missing"]:
		if newtemp == -1:
			print("error")
		if newtemp == "missing":
			print("No temp sensors found.")
		print("disconnect and reconnect the sensor")
		input("ENTER when done")
		newtemp = getNewTempSensors(knownSensors)

	knownSensors.append[newtemp]
	sensorNames.append(input("name for tertiary sensor: "))

	#attic
	print('plug in your attic sensor. This is mainly for future use with optiomizations, but is also logged/graphed')
	input("ENTER when done")
	newtemp = getNewTempSensors(knownSensors)
	while newtemp in [-1, "missing"]:
		if newtemp == -1:
			print("error")
		if newtemp == "missing":
			print("No temp sensors found.")
		print("disconnect and reconnect the sensor")
		input("ENTER when done")
		newtemp = getNewTempSensors(knownSensors)

	knownSensors.append[newtemp]
	sensorNames.append("attic")

	#save to db
	for i in range (3):
		writeTempSensors([str(i), knownSensors[i], sensorNames[i]])
	writeTempSensors(['99', knownSensors[-1], sensorNames[-1]])

def main():
	# change mode for manual run
	mode = 'auto'

	if mode == 'auto':
		results = addingSensors()
		if results == -1 or results == "missing":
			print("Make sure you have your sensor wired correctly with data/power/ground and with resistor. After checking, run this again. If problem persists, might need a reboot and/or updates.")
		else:
			print()
			print("sensors added")
			print()
			printTempSensors()

	else:
		############################################################
		# use below code to manually add                           #
		# replace 28-... with your sensor info and sensor names    #
		############################################################

		printTempSensors()

		writeTempSensors(['0', "28-0516a02c71ff", 'main'])
		writeTempSensors(['1', "28-0516a3734cff", 'secondary_sensor_name'])
		writeTempSensors(['2', "28-0516a06388ff", 'tertiary_sensor_name'])
		writeTempSensors(['99', "28-0301a279034b", 'attic'])


	printTempSensors()
if __name__ == '__main__':
	main()

