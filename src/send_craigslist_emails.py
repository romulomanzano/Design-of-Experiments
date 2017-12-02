'''
send_craigslist_emails.py
by Ryan Delgado
This script reads in the CSV containing all of the lister metadata and email info, and sends out the emails.
It assumes that the email addresses are SMTP-enabled (confirmed 4:48 Nov 20). It's based heavily off of scripts written
by Rom and Boris.
'''

import time
import smtplib
from email.mime.text import MIMEText
import pandas as pd

# Read in the CSV containing all of the recipient details
email_df = pd.read_csv('Craigslist_Manhattan_Nov20_Rdy4Email.csv')
email_df = email_df[~(email_df['Sender Email'] == 'bernard.c.gibson@gmail.com')]

# Constants
FROM_PWD = "w241@ptRent1ng"
SMTL_SSL_HOST = 'smtp.gmail.com'  # smtp.mail.yahoo.com
SMTPL_SSL_PORT = 465
SUBJECT_TEMPLATE = 'Your listing "{}" on Craigslist'

# Send out an email for each row in email_df
# Subset to just the first 4 rows for now so I can test. We'll remove '.iloc[:4, :]' after we've confirmed everything
for _, row in email_df.iloc[:4, :].iterrows():
    # Set the sender, recipient, and message details
    sender = row['Sender Email']
    # recipient = row['Email Address'] # I'll uncomment this once I've confirmed it works
    recipient = 'ryandelgado8@gmail.com'  # I'll delete this row once I've confirmed it works
    print('Sending email to {recipient} from {sender}'.format(recipient=recipient, sender=sender))
    msg = MIMEText(row['Message'])
    msg['Subject'] = SUBJECT_TEMPLATE.format(row['Title'])
    msg['From'] = sender
    msg['To'] = recipient

    # Send out the email
    server = smtplib.SMTP_SSL(SMTL_SSL_HOST, SMTPL_SSL_PORT)
    server.login(sender, FROM_PWD)
    server.sendmail(sender, recipient, msg.as_string())
    server.quit()

    # Wait 15 seconds so we don't overload the SMTP server.
    # I don't know if 'overloading the SMTP server' is actually a thing, but I don't want to find out.
    # I'm patient
    print('Email successful. Waiting 15 seconds.')
    time.sleep(15)