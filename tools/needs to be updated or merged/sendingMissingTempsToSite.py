from time import time, sleep
from os import popen, system, path
from OmegaExpansion import relayExp
from OmegaExpansion import oledExp
import urllib2, urllib, sqlite3
import datetime

data_dir = '/root/'
db_name = 'db_v5.db'

def sendToSite(recordID, temp, highCutOff, lowCutOff, temp_hall, outside, attic, state):
	if state == "ON":
		state = 65
	else:
		state = 75

	try:
		mydata=[('recordID',str(recordID)),('temp',str(temp)),('highCutOff',str(highCutOff)),('lowCutOff',str(lowCutOff)),('temp_hall',temp_hall),('outside',str(outside)),('attic',str(attic)), ('state',str(state))]
		mydata=urllib.urlencode(mydata)
		path='http://192.168.2.236/saveTempToDB.php'
		req=urllib2.Request(path, mydata)
		req.add_header("Content-type", "application/x-www-form-urlencoded")
		page=urllib2.urlopen(req).read()
	except Exception, e:
		raise e

def getX2Ytemps(x, y): #inclusive range
	arr = [] #[recordID, temp, highCutOff, lowCutOff, temp_hall]
	conn = sqlite3.connect(data_dir+db_name)
	#early on the order doesnt matter as much, but better to go ahead and do it that way for l8r
	#cur = conn.execute("SELECT recordID, temp FROM (SELECT recordID, temp FROM temps order by recordID DESC LIMIT "+str(x)+") tmp ORDER BY tmp.recordID")
	#cur = conn.execute("SELECT recordID, temp, highCutOff, lowCutOff, temp_hall FROM (SELECT recordID, temp, temp_hall FROM temps WHERE recordID BETWEEN "+str(x)+" AND "+str(y)+") NATURAL JOIN (SELECT recordID, temp, temp_hall FROM temps WHERE recordID BETWEEN "+str(x)+" AND "+str(y)+") USING ")
	#cur = conn.execute("SELECT recordID, temp, highCutOff, lowCutOff, temp_hall FROM temps NATURAL JOIN vars USING temps.recordID = vars.recordID WHERE recordID BETWEEN "+str(x)+" AND "+str(y))
	cur = conn.execute("SELECT temps.recordID, temp, highCutOff, lowCutOff, temp_hall, outside, attic, state FROM temps INNER JOIN vars ON temps.recordID = vars.recordID WHERE temps.recordID BETWEEN "+str(x)+" AND "+str(y))
	for row in cur:
		arr.append(list(row))
	conn.close()
	return arr

def main():
	#right now manually set first and last, later make it auto
	#firstToSend = 79749
	#lastToSend = 80163

	#send 447020 to 447416 (includisve) to site
	firstToSend = 590364+1
	lastToSend = 593648-1

	arr = getX2Ytemps(firstToSend, lastToSend)
	#print len(arr)
	done = 0
	#sendToSite(recordID, temp, highCutOff, lowCutOff, temp_hall)
	#SELECT temps.recordID, temp, highCutOff, lowCutOff, temp_hall

	#add print info
	print len(arr), 'records to send'
	print

	for rec in arr:
		#sendToSite(rec[0], rec[1], rec[2], rec[3], rec[4])

		#including outside
		print rec
		ret = sendToSite(rec[0], rec[1], rec[2], rec[3], rec[4], rec[5], rec[6], rec[7])
		done += 1
		print 'done:', done, '\tleft:', len(arr)-done, ret
		print

	print done, 'sent out of', len(arr)

if __name__ == '__main__':
	main()