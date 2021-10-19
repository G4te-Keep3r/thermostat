import pyowm

from mysql.connector import connect, Error

def getPersonal():
	lables = ['pyowm_api_key', 'pyowm_location', 'pyowmlat', 'pyowmlon', 'tzoffset']
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
					cursor.execute("SELECT * FROM personal")
					records = cursor.fetchall()
					for row in records:
						for i in range(len(row)):
							ret.append(row[i])
		except Error as e:
			print(e)
	except Error as e:
		raise e
	return ret

def getWeather():
	#tzoffset = getTZoffset()
	personal = getPersonal()
	try:
		owm = pyowm.OWM(personal[0])
		mgr = owm.weather_manager()
		one_call = mgr.one_call(lat=float(personal[2]), lon=float(personal[3]), units='imperial')

		wind = one_call.current.wind()
		wind = 'speed:'+str(wind['speed'])+'_deg:'+str(wind['deg'])
		humidity = str(one_call.current.humidity)
		temperature = one_call.current.temperature()
		temp = temperature['temp']
		temperature = 'temp:'+str(temperature['temp'])+'_feels_like:'+str(temperature['feels_like'])
		try:
			with connect(
				host="localhost",
				user="ac",
				password="",
				database="ac",
			) as connection:
				with connection.cursor() as cursor:
					cursor.execute("INSERT INTO weather (obj, wind, humidity, temperature, outside, recordDT, utccol) VALUES (%s, %s, %s, %s, %s, CONVERT_TZ(now(), '+00:00', "+personal[4]+"), now())", ("", wind, str(humidity), temperature, str(temp)))
					connection.commit()
		except Error as e:
			print(e)
	except Error as e:
		raise e
		return ret
	print(temp)
	print(str(temp))
	return temp


def main():
	getWeather()

if __name__ == '__main__':
	main()