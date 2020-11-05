def getAdjDelta(hour, minute):
	if hour >= 3 and hour <= 15:
		#based on the latest adjDict
		#3-9 0.5 deg lower an hour (-0.5 to -3.5)
		#9-10 0.25 lower (-3.5 to -3.75)
		if hour < 10:
			if hour < 9:
				ret = (hour - 2) * 0.5
				ret += 0.5 * (minute / 60.0)
				return ret
			#else, so hour 9
			ret = 3.5
			ret += 0.25 * (minute / 60.0)
			return ret

		#10-11 0.25 higher (-3.75 to -3.5)
		#11-12 0.25 higher (-3.5 to -3)
		#***EXPERIMENT-diff than adjDict***
		#12-4 0.75 higher per hour (-3 to 0)
		else:
			if hour == 10:
				ret = 3.75
				#ret -= 0.25 * (hour - 10)
				ret -= 0.25 * (minute / 60.0)
				return ret
			if hour == 11:
				ret = 3.5
				#ret -= 0.25 * (hour - 10)
				ret -= 0.5 * (minute / 60.0)
				return ret

			#else, hour 12+
			ret = 3.0
			ret -= 0.75 * (hour - 12)
			ret -= 0.75 * (minute / 60.0)
			return ret
	else:
		return 0



for hour in range(3, 15+1):
	#print hour, getAdjDelta(hour, 0)
	print '='*int(10*getAdjDelta(hour, 0))
	for m in range(10, 60, 10):
		print '*'*int(10*getAdjDelta(hour, m))
'''
		adjDict = {3: 0.5,
	4: 1.0,
	5: 1.5,
	6: 2.0,
	7: 2.5,
	8: 3.0,
	9: 3.5,
	10: 3.75,
	11: 3.5,
	12: 3.25,
	13: 3.0,
	14: 2.5,
	15: 2.0,
	16: 1.25,
	17: 0.5}
'''