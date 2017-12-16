#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 10:32:05 2017

@author: romulo
"""

import pandas as pd

"""
Email responses analysis section

mainly transformations on the received email data set and functions needed to do so
"""

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


def clean_email_address(txt):
    emailTxt = find_between(txt,"<",">")
    if emailTxt == "":
        return txt
    return emailTxt

def is_bounced_email(emailFrom):
    return (emailFrom == "mailer-daemon@googlemail.com")

def is_google_email(emailFrom):
    return (emailFrom in ["no-reply@accounts.google.com","inbox+noreply@google.com"] )

def is_experiment_test_email(emailFrom):
    accounts = ["alej.gonzalez.37@gmail.com","alej.gonzalez.47@gmail.com","bernie.j.smith.37@gmail.com","bernie.j.smith.47@gmail.com","ramirezjalej@gmail.com","bernard.c.gibson@gmail.com"]
    return (emailFrom in accounts)

def extract_email_from_bounced_msg(msg):
    if msg == "":
        return ""
    bc = (find_between(str(msg),"There was a problem delivering your message to ",". See the technical details below, or try resending in a few minutes."))
    if bc == "":
        bc = (find_between(str(msg),"Your message to "," has been blocked. See technical details below for more information."))
    return bc

def ignore_email(row):
    return (row['isBounced'] | row['isGoogleNotification'] | row['isTestReply'] )

def assign_experiment_email(row):
    if row["isBounced"]:
        return row["emailFromBounced"]
    return row["fromEmail"]

#Sourcing the raw emails and doing some enrichments
receivedEmails = pd.read_csv("./data/w241_Apt_Renting_emails.csv")
#extracting the exact email address of the response
receivedEmails['fromEmail'] = receivedEmails.apply (lambda row: clean_email_address(row['From']),axis=1)
#
receivedEmails['isBounced'] = receivedEmails.apply (lambda row: is_bounced_email(row['fromEmail']),axis=1)
#
receivedEmails['isGoogleNotification'] = receivedEmails.apply (lambda row: is_google_email(row['fromEmail']),axis=1)
#
receivedEmails['isTestReply'] = receivedEmails.apply (lambda row: is_experiment_test_email(row['fromEmail']),axis=1)
#
receivedEmails['ignoreEmail'] = receivedEmails.apply (lambda row: ignore_email(row),axis=1)
#emailFromBounced
receivedEmails['emailFromBounced'] = receivedEmails.apply (lambda row: extract_email_from_bounced_msg(row['Body']),axis=1)
#treatmentEmail
receivedEmails['treatmentEmail'] = receivedEmails.apply (lambda row: assign_experiment_email(row),axis=1)
#ignore list
ignoreList = list(receivedEmails[receivedEmails['ignoreEmail']]['treatmentEmail'].unique())
#Unique Respondents:
listOfRespondents = list(receivedEmails['treatmentEmail'].unique())
#how many emails were received from this respondent per each treatment inbox
numberOfExchanges =  pd.DataFrame({'numberOfResponsesToThisTreatment' : receivedEmails.groupby(['treatmentEmail', 'inbox']).size()}).reset_index()
#how many different treatment inboxes interacted with the respondent
numberOfTreatmentInboxes =  pd.DataFrame({'numberOfTreatmentsRespondedTo' : numberOfExchanges.groupby(['treatmentEmail']).size()}).reset_index()
#multiple treatment list
multTreatList = list(numberOfTreatmentInboxes[numberOfTreatmentInboxes['numberOfTreatmentsRespondedTo'] >1]['treatmentEmail'].unique())


receivedEmailsEnriched =  receivedEmails.merge(numberOfExchanges, left_on=['treatmentEmail','inbox'], right_on=['treatmentEmail','inbox'], how='inner')
#
receivedEmailsEnriched =  receivedEmailsEnriched.merge(numberOfTreatmentInboxes , left_on='treatmentEmail', right_on='treatmentEmail', how='inner')

#saving interim file
receivedEmailsEnriched.to_csv('./data/w241_Apt_Renting_received_emails_enriched.csv')
#there were 6 cases where we applied multiple treatments to the same posting (i.e. contacted from different treatment accounts)

receivedEmailsEnrichedIgnoreRemoved = receivedEmailsEnriched[receivedEmailsEnriched['ignoreEmail'] == False].reset_index()
receivedEmailsEnrichedIgnoreRemoved.to_csv('./data/w241_Apt_Renting_received_emails_enriched_removed_ignore.csv')



"""
Email sent analysis section

mainly transformations on the treatment emails sent and functions needed to do so
"""

#load actual emails sent
sentEmails = pd.read_csv("./data/w241_Apt_Renting_emails_sent.csv")
sentEmails['treatmentEmail'] = sentEmails['To']
numberOfEmailsSentFromInbox=  pd.DataFrame({'numberOfEmailsSentForThisTreatment' : sentEmails.groupby(['treatmentEmail', 'inbox']).size()}).reset_index()
#how many different treatments were actually applied
numberOfTreatmentApplied =  pd.DataFrame({'numberOfDiffTreatmentsApplied' : numberOfEmailsSentFromInbox.groupby(['treatmentEmail']).size()}).reset_index()
#applied
multTreatAppliedList = list(numberOfTreatmentApplied[numberOfTreatmentApplied['numberOfDiffTreatmentsApplied'] >1]['treatmentEmail'].unique())



"""
Reconciliation against treatment tracker


"""

##Now will load the sent email tracker
treatmentTracker = pd.read_csv("./data/w241_Email_sent_tracker_missings_removed.csv")

#defining functions needed to join the data

def assign_treatment_inbox(row):
    if(row['Nonwhite'] == 1):
        if (row['Child'] == 1):
            return 'alej.gonzalez.47@gmail.com'
        else:
            return 'ramirezjalej@gmail.com'
    else:
        if (row['Child'] == 1):
            return 'bernie.j.smith.37@gmail.com'
        else:
            return 'bernard.c.gibson@gmail.com'


def assign_ignore_flag(mail,ignoreList):
    return (mail in ignoreList)

def assign_respond_multiple_treatments_flag(mail,multTreatList):
    return (mail in multTreatList)

def assign_multiple_treatments_applied_flag(mail,multTreatAppliedList):
    return (mail in multTreatAppliedList)

#assigning the inbox treatment
treatmentTracker['inbox'] = treatmentTracker.apply(lambda row: assign_treatment_inbox(row),axis=1)
#adding a column for consitency (names):
treatmentTracker['treatmentEmail'] = treatmentTracker['Email Address']
#adding a column for ignore list (names):
treatmentTracker['ignore'] = treatmentTracker.apply(lambda row: assign_ignore_flag(row['treatmentEmail'],ignoreList),axis=1)
#adding a column for mult treat list (names):
treatmentTracker['multipleTreatmentResponses'] = treatmentTracker.apply(lambda row: assign_respond_multiple_treatments_flag(row['treatmentEmail'],multTreatList),axis=1)
#adding a column for mult treat applied list (names):
treatmentTracker['multipleTreatmentApplied'] = treatmentTracker.apply(lambda row: assign_multiple_treatments_applied_flag(row['treatmentEmail'],multTreatAppliedList),axis=1)

#merge with responses details
treatmentTrackerEnriched =  treatmentTracker.merge(numberOfExchanges, left_on=['treatmentEmail','inbox'], right_on=['treatmentEmail','inbox'], how='left')
treatmentTrackerEnriched['numberOfResponsesToThisTreatment'].fillna(value=0,inplace=True)

#merge with email sent details
treatmentTrackerEnriched =  treatmentTrackerEnriched.merge(numberOfEmailsSentFromInbox, left_on=['treatmentEmail','inbox'], right_on=['treatmentEmail','inbox'], how='left')
treatmentTrackerEnriched['numberOfEmailsSentForThisTreatment'].fillna(value=0,inplace=True)
#Saving the data for analysis
treatmentTrackerEnriched.to_csv('./data/w241_Enriched_Tracker_Based_on_Emails.csv')