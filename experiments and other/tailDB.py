import sqlite3

def printEverything():
	#conn = sqlite3.connect('/tmp/mounts/USB-B/db_v2/db_v2.db')
	conn = sqlite3.connect('/root/db_v5.db')
	#cur = conn.execute("SELECT * FROM vars order by recordID DESC")
	print 'vars'
	cur = conn.execute("SELECT * FROM vars order by recordID DESC LIMIT 7")
	for row in cur: print row
	print '\n\n\nsettings'
	cur = conn.execute("SELECT * FROM settings order by settingsIteration DESC LIMIT 5")
	for row in cur: print row
	print '\n\n\ntemps'
	#cur = conn.execute("SELECT * FROM temps order by recordID DESC LIMIT 10")
	cur = conn.execute("SELECT * FROM temps INNER JOIN datetime ON temps.recordID = datetime.recordID order by recordID DESC LIMIT 10")
	for row in cur: print row
	conn.close()

def main():
	printEverything()

if __name__ == '__main__':
	main()

'''
DELETE FROM `table`
WHERE recordID NOT IN (
  SELECT recordID
  FROM (
    SELECT recordID
    FROM `table`
    ORDER BY recordID DESC
    LIMIT 60 -- keep this many records
  ) foo
);
'''
