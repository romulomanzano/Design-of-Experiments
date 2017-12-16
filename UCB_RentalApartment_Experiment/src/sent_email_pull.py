#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 12:15:20 2017

@author: romulo
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

@author: romulo
@Python 3.6

"""

import imaplib
import email
import pandas as pd

ORG_EMAIL   = "@gmail.com"
FROM_PWD    = ""
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993


def extract_key(msg,ky):
    if (ky in msg.keys()):
        return str(msg[ky])
    return ''

def extract_emails(mail):
    relevantMeta =[ 'Date', 'Subject', 'From', 'To'] 
    emailList = []
    result, data = mail.uid('search', None, "ALL") # search all email and return uids
    if result == 'OK':
        readEmail = {}
        for num in data[0].split():
            result, data = mail.uid('fetch', num, '(RFC822)')
            if result == 'OK':
                email_message = email.message_from_bytes(data[0][1])    # raw email text including headers
                for k in relevantMeta:
                    readEmail[k] = extract_key(email_message,k)
                readEmail['Body'] = ''
                txtParts = []
                for part in email_message.walk():
                    # each part is a either non-multipart, or another multipart message
                    # that contains further parts... Message is organized like a tree
                    if part.get_content_type() == 'text/plain':
                        if part.get_content_charset() is None:
                        # We cannot know the character set, so return decoded "something"
                            body = part.get_payload(decode=True)
                        else:
                            body = part.get_payload(decode=True).decode(part.get_content_charset())
                        txtParts.append(body)
                #override
                if (len(txtParts)):
                    readEmail['Body'] = txtParts[0]
                emailList.append(readEmail.copy())
        
    
    return emailList

"""To be able to pull emails with this script we need to go to the account 
    and turn this setting 'ON' Allow less secure apps: ON
    https://myaccount.google.com -> security"
"""
accounts = ["alej.gonzalez.37","alej.gonzalez.47","bernie.j.smith.37","bernie.j.smith.47","ramirezjalej","bernard.c.gibson"]
dfSet = []

for act in accounts:
    FROM_EMAIL  =  act + ORG_EMAIL
    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(FROM_EMAIL,FROM_PWD)
    mail.select('"[Gmail]/Sent Mail"')
    extracted = extract_emails(mail)
    results = pd.DataFrame.from_dict(extracted.copy())
    results['inbox'] = FROM_EMAIL
    dfSet.append(results)
    
report = pd.concat(dfSet)
report.to_csv('./data/w241_Apt_Renting_emails_sent.csv')

