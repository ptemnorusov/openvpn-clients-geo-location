import datetime as dt
import smtplib
import requests

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

#make logfile name
now = dt.datetime.now()
timestamp = now.strftime("%Y-%m-%d")
vpn_connection_filename = f"vpnlog-{timestamp}.log"


mail_string :str = ""

#open file and read log strings one by one
with open(vpn_connection_filename, 'r') as log:
    while True:
        logstring = log.readline()
        if logstring:
            logstring = logstring.split()
            conn_date = dt.datetime.strptime(logstring[1], "%Y-%m-%dT%H:%M:%S.%f%z")
            conn_username = logstring[7].split('/')[0]
            conn_source_ip = logstring[7].split('/')[1].split(':')[0]
            #form url address to get info from ipinfo
            url = f"https://ipinfo.io/{conn_source_ip}/json?token=tokenshmoken"
            #getting results in json format
            conn_source_ip_details = requests.get(url).json()

            conn_source_ip_location = f"{conn_source_ip_details['country']}/{conn_source_ip_details['city']} Organization: {conn_source_ip_details['org']}"
            conn_vpn_ip = logstring[14]
            #making string to put into a email
            mail_string = mail_string + f"Вчера {dt.datetime.strftime(conn_date, u'%Y-%m-%d')} в {dt.datetime.strftime(conn_date, u'%H:%M')} к нам подключался клиент {conn_username} из {conn_source_ip_location} и получил адрес {conn_vpn_ip} " + "<br>"

        else:
            break

#Sending an email
sender = "Jarvis <user@domain.ru>"
receiver = "Petr Temnorusov <user@domain.ru>"
subject = "Подключения к openvpn за вчерашний день"

msg = MIMEMultipart()
msg['From'] = sender
msg['To'] = receiver
msg['Subject'] = subject
body = f"""
<html><head><style> body {{ font-family: calibri, arial, serif; }} </style></head><body>
Здравствуйте, Петр,<br><br> {mail_string}<br> Хорошего дня </body></html>
"""
msg.attach(MIMEText(body, "html"))
server = smtplib.SMTP('mail.domain.ru', 25, )
text = msg.as_string()
server.sendmail(sender, receiver, text)
server.quit()
