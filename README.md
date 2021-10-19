# thermostat
Raspberry Pi 4 with relay hat running ac.py on 1 minute cronjob being a thermostat. Not basic old on/off, not pattern learning from what you do with it. This is about optimizing and more intelligently turning it on and off.

The optimizations were found by hand tweaking stuff as this was developed over 3+ years. But application of machine learning to dynamically optimize is being investigated (dynamic so it adjusts seasonally).

Weather is currently updated every 10 minutes via cronjob. Mainly this is due to current owm one call API limits, but outside temperature doesn't tend to change fast enough that you would really need to update it more frequently anyways.


![in use](https://github.com/G4te-Keep3r/thermostat/blob/master/in-use.jpg)


# wiring / hardware
* 1 wire temp sensor such as https://www.amazon.com/gp/product/B00CHEZ250/
	* I used PWM extension cables (also commonly called 3 pin servo cables) for convenience with the Y splitters, extensions, and modularity for replacing a sensor. But I also had a bunch available to use.
	* data pin goes to GPIO4
	* ![wiring](https://github.com/G4te-Keep3r/thermostat/blob/master/wiring.jpg)
* relay hat such as https://www.amazon.com/gp/product/B07CZL2SKN/
	* any relay hat should work, just the GPIO pin might need to be changed
* GPIO expander not needed unless you are putting a screen on it. Currently all the screen is good for is having grafana up or a terminal tailing logs


# config
git clone https://github.com/G4te-Keep3r/thermostat.git

*working on a probe discovery script, and ways to edit the number of probes and their names (if not obvious this project is EXTREAMLY custom designed). The migration from omega2+/sqlite3 to rpi4/mysql simplified many parts of the code, so it should be pretty easy to add these. Table temps does make it less simple to make this dynamic.*


Install mariadb, grafana, python3, mysql python connector

Run createDB.py, populateDB.py, and init_tempSensors.py *** do not connect sensors until init_tempSensors.py tells you to. If you already did connect more than 1, you will probably need to edit init_tempSensors.py to manual mode ***

Before adding to cron, run ac.py and weatherLogger.py so you can see errors if there are any

Add ac.py as 1 minute cronjob and weatherLogger.py as 10 minute cronjob


# change settings
newSettings.py is to move the min/max temperature range easily

changeSettings.py is to tweak all the settings including size of temperature range (most of these should be part of the future ai part tho)


# grafana / mysql
to get grafana to play nice, there are 2 datetime columns-local and utc (recordDT and utccol). The way it is currently done, you have to update tzoffset twice a year. [INSERT RANT HERE ABOUT THE INSANTY OF STILL CHANGING CLOCKS]

<del>you will need to run '''set global time_zone='+00:00';''' from mysql console as well<del>

To fix timezone issues, add the following to /etc/mysql/conf.d/mysql.cnf
init_command="set global time_zone='+00:00'"


Without that being in cnf, it is messed up with every reboot. ***this fixes a reboot, but not a power loss it seems. Just fyi***


# MAIN TODOs
* update install.sh
* get forecast to know when to not precool
	* ![2 day graph](https://github.com/G4te-Keep3r/thermostat/blob/master/2day-example-graph-with-note.png)
	* before cool front, there is a bit of precooling
		* looks like there might be a good candidate hotter day next week, or will generate a graph from saved summer data to highlight the difference better
	* after the cool front came in, the forecast would have shown that the daily high did not need any precooling
* calibration function for temp probes
* more cleaning up code from migration - mostly done
* sensor replacement
	* replace_tempSensors.py
	* ***not tested***


# FUTURE PLANS
* heater functionality
	* mode (ac/off/heat) - so probably 2 relays (off being both off)
	* relay on heater wire
	* heater logic
		* feature like precooling probably not needing as adding heat is easy compared to removing, but would be investigated when looking for patterns
	* automated switch between ac/heat based on forecast, but start with manual only
* ai section optimization/learning house specific behavior
	* on/off cycle durration/frequency
	* precooling length/depth, and based on forecast
* add celsius option