#from thermostatFunctions import *
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

def getTemp(w1id):
	try:
		cmd = "cat /sys/devices/w1_bus_master1/"+w1id+"/w1_slave"
		result = os.popen(cmd).read()
		result = result[result.find('t=')+2:]
		t = int(result)/1000.0
		#C to F
		t *= 1.8
		t += 32
		return t
	except Exception as e:
		return -1

def main():
	for probe in getTempSensors():
		#print(probe)
		print probe[1], getTemp(probe[0])

if __name__ == '__main__':
	main()
