from time import time, sleep
from os import popen, system, path
from OmegaExpansion import relayExp
from OmegaExpansion import oledExp
import urllib2, urllib, sqlite3
import datetime

data_dir = '/root/'
db_name = 'db_v5.db'

def sendStateToSite(recordID, state):
	if state == "ON":
		state = 65
	else:
		state = 75
	mydata=[('recordID',str(recordID)),('state',str(state))]
	mydata=urllib.urlencode(mydata)
	path='http://192.168.2.236/saveStateToDB.php'    #the url you want to POST to
	req=urllib2.Request(path, mydata)
	req.add_header("Content-type", "application/x-www-form-urlencoded")
	page=urllib2.urlopen(req).read()

def getStates(recordID):
	ret = []
	conn = sqlite3.connect(data_dir+db_name)
	cur = conn.execute("SELECT recordID, state FROM vars WHERE recordID >= "+str(recordID))
	for row in cur:
		ret.append([row[0], str(row[1])])
	conn.close()
	return ret

def main():
	recordID = 537203
	ret = getStates(recordID)
	print ret
	count = 0
	total = len(ret) * 1.0
	for record in ret:
		#sendStateToSite(recordID, state)
		print record,
		sendStateToSite(record[0], record[1])
		count += 1
		percent = str((count*100.0) / total)
		print percent+' done'

if __name__ == '__main__':
	main()