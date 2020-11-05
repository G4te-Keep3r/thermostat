# thermostat
Onion omega 2+ with oled and relay expansion running ac.py on 1 minute cronjob being a thermostat. Not basic old on/off, not pattern learning from what you do with it. This is about optimizing and more intelligently tunring it on and off.

All the random helper tools are comming soon (being refined)

# config
git clone git@github.com:G4te-Keep3r/thermostat.git .

edit the following in thermostatFunctions.py
pyowm_api_key = 'yours here'
pyowm_location = yourshere

edit the following in thermostatFunctions.py ac.py (possibly elsewhere)
ip = '192.168.2.236'
t_id1 = "28-0516a02c71ff"
t_hall = "28-0516a06388ff"
t_door = "28-0516a3734cff"
t_attic = "28-0301a279034b"

*moving all this stuff to .env file so will be easier*
*working on a probe discovery script, and ways to edit probe number and names (if not obvious this project is EXTREAMLY custom designed)*

# install, from /root
chmod +x install.sh
./install.sh
