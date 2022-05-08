# openvpn-clients-geo-location
Getting openvpn client's IP addresses location

01-form-logfile.sh  gathers logs during the day until 23:58 every day (cron job)
02-main.py          parses the log file and ask for IP location at 23:59 (cron job)
