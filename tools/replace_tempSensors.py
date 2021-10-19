from mysql.connector import connect, Error
import os

def getTempSensors():
	ret = []
	try:
		try:
			with connect(
				host="localhost",
				user="ac",
				password="",
				database="ac",
			) as connection:
				with connection.cursor() as cursor:
					cursor.execute("SELECT * FROM tempsensors order by priority+0 asc")
					records = cursor.fetchall()
					for row in records:
						#print(row[0], row[1], row[2])
						ret.append([row[1], row[2]])
						#ret.append(row[1]) #name (row[2]) will be needed in future versions
		except Exception as e:
			print(e)
	except Error as e:
		raise e
	return ret

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

def getAllTempSensors():
	knownSensors = ['w1_bus_master1']

	try:
		ret = []
		cmd = "ls /sys/bus/w1/devices"
		result = os.popen(cmd).read()
		for line in result.split():
			if line not in knownSensors:
				ret.append(line)
		return ret
	except Exception as e:
		return -1

def updateTempSensors(oldSensor, newSensor):
	try:
		try:
			with connect(
				host="localhost",
				user="ac",
				password="",
				database="ac",
			) as connection:
				with connection.cursor() as cursor:
					cursor.execute("UPDATE tempsensors SET id = "+newSensor+" WHERE id = "+oldSensor)
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

def main():
	#get list of current db
	savedSensors = getTempSensors()
	knownSensors_db = []
	for s in savedSensors:
		knownSensors_db.append(s[0])
	#get new
	newSensor = getNewTempSensors(knownSensors_db)
	allSensors = getAllTempSensors()
	#update based on
	oldSensor = None
	for sdb in knownSensors_db:
		if sdb not in allSensors:
			oldSensor = sdb
	print("missing:", oldSensor)
	print("new replacement:", newSensor)
	updateTempSensors(oldSensor, newSensor)
	print()
	printTempSensors()

if __name__ == '__main__':
	main()