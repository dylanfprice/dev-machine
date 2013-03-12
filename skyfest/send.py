#! /usr/bin/python

from msg import TEXT, HTML, SUBJECT

from csv import DictReader
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getpass
import smtplib


def send_message(smtp_conn, fromEmail, company, email):
  # create message
  msg = MIMEMultipart('alternative')
  msg['Subject'] = SUBJECT.format(company=company)
  msg['From'] = fromEmail
  msg['To'] = email

  text = TEXT.format(company=company)
  html = HTML.format(company=company)

  part1 = MIMEText(text, 'plain')
  part2 = MIMEText(html, 'html')

  msg.attach(part1)
  msg.attach(part2)

  # send messages
  smtp_conn.sendmail(fromEmail, email, msg.as_string())


if __name__ == "__main__":
  fromAddr = "deanej@uw.edu"
  fromEmail = "Janelle Deane <deanej@uw.edu>"

  s = smtplib.SMTP('smtp.washington.edu', 587)
  s.starttls()
  pw = getpass.getpass()
  s.login(fromAddr, pw)

  csvfile = open('companies.csv', 'r')
  reader = DictReader(csvfile)
  for values in reader:
    company = values['Company']
    email = "{company} <{email}>".format(company=company, email=values['Email'])
    try:
      send_message(s, fromEmail, company, email)
      print("Successfully sent message to {email}".format(email=email))
    except Exception as e:
      print("ERROR: Failure for {email}. Error: {error}".format(email=email, error=e))

  s.quit()
