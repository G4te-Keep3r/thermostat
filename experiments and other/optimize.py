import sqlite3

#week of minutes if 10080, so using that for now
#record 526277 - 10080 = start at record 516197
def getVarsFromDB():
	d={}
	conn = sqlite3.connect('db_v4.db')
	#minCooldown, maxCooldown, maxRunTime, lowCutOff, highCutOff, cooldownTime, runTime, acRunningLowCutOffRaisePercent, acRunningLowCutOffRaiseTimeMin, acOffHighCutOffLowerPercent, acOffHighCutOffLowerPercentNum2, acOffHighCutOffLowerTimeMin, acOffHighCutOffLowerTimeMinNum2, state, recordID
	cur = conn.execute("SELECT cooldownTime, runTime, state, recordID FROM vars WHERE recordID > 516197")# order by recordID ASC")
	for row in cur:
		d[int(row[3])] = [float(row[0]), float(row[1]), row[2]]
	conn.close()
	return d

def getTemps():
	d = {}
	conn = sqlite3.connect('db_v4.db')
	cur = conn.execute("SELECT temp, outside, attic, recordID FROM temps WHERE recordID > 516197")# order by recordID ASC")
	#outside not equal to 82.2882
	#attic not equal to 75.5775
	for row in cur:
		#print row
		if row[1] != None and row[2] != None:
			if float(row[1]) != 82.2882 and float(row[2]) != 75.5775:
				d[int(row[3])] = [float(row[0]), float(row[1]), float(row[2])]
	conn.close()
	return d

def getAvg(t, arr):
	t_arr = sorted(arr)[len(arr)/10:len(arr)-(len(arr)/10)]
	print t, sum(t_arr)/len(t_arr)

def printStats(t, arr):
	#print "range: "+str(max(arr)-min(arr))
	t_arr = sorted(arr)[len(arr)/10:len(arr)-(len(arr)/10)]
	print t, '#'*(int(((max(t_arr)-min(t_arr)))*10))

def getData():
	###### this whole things could be done with 1 query that includes a join, but doing it this way because for flexibility during development
	v_dict = getVarsFromDB()
	t_dict = getTemps()
	records = {}
	for k in v_dict.keys():
		if k in t_dict.keys():
			records[k] = []
			records[k].extend(v_dict[k])
			records[k].extend(t_dict[k])
			#recordID ==> cooldownTime, runTime, state, temp, outside, attic
	###### end of join could simplify

	#time (running or resting) ====> "0" is part of the previous data as 24:00 ends 23:59
	#	temp
	#		delta
	#		outside
	#		attic
	dataON = {}
	dataoff = {}

	for k in records.keys():
		try:
			records[k].append(records[k][3] - records[k-1][3])
		except:
			#print k
			a=5

	#remove the entries that do nhot have a delta
	for k in records.keys():
		if len(records[k]) == 6:
			records.pop(k)

	'''###*** for simplicity in early version of this, all temps are being rounded down  ***###'''
	for k in records.keys():
		#records[k][3] = int(records[k][3]) #temp to 1 deg
		records[k][3] = int(records[k][3])/2*2 #temp to 2 deg
		records[k][4] = int(records[k][4])/5*5 #outside to 5 deg
		records[k][5] = int(records[k][5])/5*5 #attic to 5 deg
		#this is bad....fix soon

	for k in records.keys():
		if records[k][0] == 0 and records[k][1] == 0:
			if records[k][2] == 'ON':
				state = 'OFF'
			else:
				state = 'ON'
			state = ':('
			#come back to because need to get runtime from previous record and add 1 to it
		else: #not switching state special case
			state = records[k][2]


		#recordID ==> cooldownTime, runTime, state, temp, outside, attic

		if state == 'ON':
			runTime = records[k][1]
			temp = records[k][3]
			#temp = records[k][4]
			if runTime not in dataON:
				dataON[runTime] = {}
			if temp not in dataON[runTime]:
				dataON[runTime][temp] = [[], [], []]
			dataON[runTime][temp][0].append(records[k][6]) #delta
			dataON[runTime][temp][1].append(records[k][4]) #outside
			dataON[runTime][temp][2].append(records[k][5]) #attic

		if state == 'OFF':
			cooldownTime = records[k][0]
			temp = records[k][3]
			if cooldownTime not in dataoff:
				dataoff[cooldownTime] = {}
			if temp not in dataoff[cooldownTime]:
				dataoff[cooldownTime][temp] = [[], [], []]
			dataoff[cooldownTime][temp][0].append(records[k][6]) #delta
			dataoff[cooldownTime][temp][1].append(records[k][4]) #outside
			dataoff[cooldownTime][temp][2].append(records[k][5]) #attic

	print "dataON"
	print '-'*25
	for t in dataON.keys():
		print '='*25
		print t
		print '='*25
		arr = []
		for temp in dataON[t]:
			arr.extend(dataON[t][temp][0])
			getAvg(temp, dataON[t][temp][0])
		#printStats(t, arr)
		print
		print

	print
	print
	print
	print "dataoff"
	print '-'*25
	for t in dataoff.keys():
		arr = []
		for temp in dataoff[t]:
			arr.extend(dataoff[t][temp][0])
		#printStats(t, arr)

'''
look at dict[runTime/coolDownTime]
	from similar inside and outside temps, get next delta
	use attic over outside as it should be a more direct factor on the cooling capabilities (future version can have outside and time predict attic maybe)
'''
def main():
	data = getData()

if __name__ == '__main__':
	main()
