# thermostat
Raspberry Pi 4 with relay hat running ac.py on 1 minute cronjob being a thermostat. Not basic old on/off, not pattern learning from what you do with it. This is about optimizing and more intelligently turning it on and off.

The optimizations were found by hand tweaking, but application of machine learning to dynamically optimize is being investigated (dynamic so it adjusts seasonally).

Weather is currently updated every 10 minutes via cronjob. Mainly this is due to current owm one call API limits.


# config
git clone https://github.com/G4te-Keep3r/thermostat.git

*working on a probe discovery script, and ways to edit the number of probes and their names (if not obvious this project is EXTREAMLY custom designed). The migration from omega2+/sqlite3 to rpi4/mysql simplified many parts of the code, so it should be pretty easy to add these. Table temps does make it less simple to make this dynamic.*


TLDR install mariadb, grafana, python3, mysql python connector

Edit init_tempSensors.py for your sensors, and createDB.py with your openweathermap.org info.

Run createDB.py, populateDB.py, init_tempSensors.py

Before cron, run ac.py and weatherLogger.py so you can see errors if there are any.

Add ac.py as 1 minute cronjob and weatherLogger.py as 10 minute cronjob.


# grafana / mysql

to get grafana to play nice, there are 2 datetime columns-local and utc (recordDT and utccol). The way it is currently done, you have to update tzoffset twice a year. [INSERT RANT HERE ABOUT THE INSANTY OF STILL CHANGING CLOCKS]

<del>you will need to run '''set global time_zone='+00:00';''' from mysql console as well<del>

To fix timezone issues, add the following to /etc/mysql/conf.d/mysql.cnf
init_command="set global time_zone='+00:00'"


Without that being in cnf, it is messed up with every reboot. ***this fixes a reboot, but not a power loss it seems. Just fyi***


# MAIN TODOs
* make scanner to init temp sensors/probes and update when failed ones are replaced
* script asking for info for writePersonal()
* more cleaning up code from migration
* update install.sh
* add example picture of hardware and grafana
* wiring section (gpio pin and about 1 wire/resistor)
* wiring relay/ac unit
* hardware list/links to buy
