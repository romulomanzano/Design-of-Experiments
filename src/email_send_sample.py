# -*- coding: utf-8 -*-
"""
Spyder Editor

@author: romulo
@Python 3.6

"""

"""To be able to send emails with this script we need to go to the account 
    and turn this setting 'ON' Allow less secure apps: ON
    https://myaccount.google.com -> security"
"""
import smtplib
from email.mime.text import MIMEText


#Treatment Text#
child = """Hi,
My wife and I (plus our 4 month old baby) are looking for a larger apartment and your posting looks great.  When are you available to schedule a viewing?
Thanks,
Alejandro"""
noChild = """Hi,

My wife and I are looking for a larger apartment and your posting looks great.  When are you available to schedule a viewing?

Thanks,
Alejandro"""

#
ORG_EMAIL   = "@gmail.com"
FROM_PWD    = "w241@ptRent1ng"
act = "alej.gonzalez.37"
FROM_EMAIL  =  act + ORG_EMAIL
smtp_ssl_host = 'smtp.gmail.com'  # smtp.mail.yahoo.com
smtp_ssl_port = 465
username = FROM_EMAIL
password = FROM_PWD    
sender = FROM_EMAIL
targets = ["alej.gonzalez.37@gmail.com","alej.gonzalez.47@gmail.com","bernie.j.smith.37@gmail.com","bernie.j.smith.47@gmail.com","ramirezjalej@gmail.com","bernard.c.gibson@gmail.com"]

msg = MIMEText(child)
msg['Subject'] = '[TEST] Your apartment listing on craigslist'
msg['From'] = sender
msg['To'] = ', '.join(targets)

server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
server.login(username, password)
server.sendmail(sender, targets, msg.as_string())
server.quit()



