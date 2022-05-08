#!/usr/local/bin/bash

#make a filename string
timestamp=$(date +"%Y-%m-%d")
daylog_filename="vpnlog-$timestamp.log"

#create today's log file
touch $daylog_filename


while true
do
    #Watch openvpn string for a string
    vpnlog_str=$( tail -F /var/log/openvpn.log | grep -m1 "primary virtual IP for" )
    echo $vpnlog_str >> $daylog_filename
    
    #exit if it is the end of the day
    if [ $(date +%H) -gt 23 ] && [ $(date +%M) -ge 58 ] ; then break ; fi
    
    #exit if admin wants
    script_stop=$(<script-stop)
	  if [ "$script_stop" = "1" ]; then break ; fi
done

#clear 'stop' file
echo > script-stop
