opkg update
opkg install python pyOledExp pyRelayExp python-pip
pip install pyowm
insmod w1-gpio-custom bus0=0,19,0
python ./tools/createDB.py
python ./tools/populateDB.py
(crontab -l 2>/dev/null; echo "#") | crontab -
(crontab -l 2>/dev/null; echo "*/1 * * * * /root/ac.py") | crontab -
(crontab -l 2>/dev/null; echo "# Make sure you have this comment at the end of your crontab") | crontab -
/etc/init.d/cron restart
