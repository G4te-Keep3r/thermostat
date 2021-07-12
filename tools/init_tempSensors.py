'''
need to plan this out...

for now it just adds them to db
'''

from mysql.connector import connect, Error

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

def main():
	'''
	t_id1 = "28-0516a02c71ff"
	t_door = "28-0516a3734cff"
	t_hall = "28-0516a06388ff"
	t_attic = "28-0301a279034b"
	'''

	printTempSensors()

	#'''
	writeTempSensors(['0', "28-0516a02c71ff", 'main']) #previously known as t_id1
	writeTempSensors(['1', "28-0516a3734cff", 'door'])
	writeTempSensors(['2', "28-0516a06388ff", 'hall'])
	writeTempSensors(['99', "28-0301a279034b", 'attic'])
	#'''

	printTempSensors()

if __name__ == '__main__':
	main()