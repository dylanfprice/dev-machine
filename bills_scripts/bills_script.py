#!/usr/local/bin/python

# Bills Script
# Last edited: 01/02/2011

# Parses bills.txt and sends e-mails to people who need to pay bills.

import bills_yacc
import sys
import shutil
import config
from datetime import date
from smtplib import SMTP
from email.MIMEText import MIMEText
from base64 import b64decode

class SmtpLoggedInConnection:

    def __init__(self, smtpserver, username, password, debuglevel):
        self.smtpserver = smtpserver
        self.username = username
        self.password = password
        self.debuglevel = debuglevel

    def __enter__(self):
        self.conn = SMTP(self.smtpserver)
        self.conn.set_debuglevel(self.debuglevel)
        self.conn.starttls()
        self.conn.login(self.username, self.password)
        return self.conn

    def __exit__(self, type, value, traceback):
        self.conn.close()
        return True

def extract_owestrings(parse):
    emails = {}
    for bill in parse:
        timediff = bill['due_date'] - date.today()
        if timediff.days <= config.REMIND_INTERVAL:
            num_names = len(bill['names'])
            for name in bill['names'].keys():
                amount = bill['names'][name][0]
                if amount == -1:
                    amount = bill['amount'] / num_names
                paid = bill['names'][name][1]
                if not paid:
                    if not name in emails:
                        emails[name] = ""
                    emails[name] += config.OWESTRING % \
                        (amount, bill['bill'], bill['due_date'].strftime("%A, %B %d"))
    return emails

def send_emails(emails):
    with SmtpLoggedInConnection(config.SMTP_SERVER, config.SMTP_USERNAME, \
                                b64decode(config.SMTP_PASSWORD), config.DEBUG_LEVEL) as conn:
        for name in emails.keys():
            send_email(conn, config.EMAILS['Dylan'], config.EMAILS[name], \
                       config.SUBJECT, config.MSG % (name, emails[name]))

def send_email(conn, sender, receiver, subject, msg):
    msg = MIMEText(msg, 'plain')
    msg['Subject'] = subject
    msg['From'] = sender
    conn.sendmail(sender, [receiver], msg.as_string())

def log(logfile, logmessage):
    with open(logfile, 'a+') as file:
        file.write(logmessage + "\n")

def backup(billsfile):
    shutil.copyfile(billsfile, billsfile + ".backup")

def main():
    logmessage = None
    parse = None
    emails = None
    try:
        if len(sys.argv) < 2:
            logmessage = "Did not receive a file argument."
            raise Exception("Did not receive a file argument.")
        billsfile = open(sys.argv[1], 'r')
        backup(sys.argv[1])
        parse = bills_yacc.parse(billsfile.read())
        emails = extract_owestrings(parse)
        send_emails(emails)
        logmessage = "[%s] Success!" % date.today()
    except Exception as exc:
        logmessage = "[%s] Failure. %s \n %s" % (date.today(), parse, emails)
        # try to send failure email
        try:
            with SmtpLoggedInConnection(config.SMTP_SERVER, config.SMTP_USERNAME, \
                                        b64decode(config.SMTP_PASSWORD), config.DEBUG_LEVEL) as conn:
                send_email(conn, config.EMAILS['Dylan'], config.EMAILS['Dylan'], \
                           config.ERRMSG_SUBJECT, config.ERRMSG % exc)
        except:
            pass

    if logmessage:
        log(config.LOGFILE, logmessage)

if __name__ == "__main__":
    main()
