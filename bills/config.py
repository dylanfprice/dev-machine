# If a bill is due within REMIND_INTERVAL days, then an email will be sent
REMIND_INTERVAL = 21

# A dictionary from names to email addresses
EMAILS = {
    'dylan': 'the.dylan.price@gmail.com',
}

# SMTP server config
# SMTP_PASSWORD is base64 encoded
#SMTP_SERVER = 'smtp.gmail.com'
#SMTP_USERNAME = 
#SMTP_PASSWORD = 

SUBJECT = 'Bills'
GREETING = 'Hey'
SENDER = 'Dylan Price <the.dylan.price@gmail.com>'
