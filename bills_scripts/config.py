# If a bill is due within REMIND_INTERVAL days, then an email will be sent
REMIND_INTERVAL = 7

# A dictionary from names to email addresses
EMAILS = {
}

# SMTP server config
# SMTP_PASSWORD is base64 encoded
SMTP_SERVER = 'smtp.gmail.com'
SMTP_USERNAME = None
SMTP_PASSWORD = None

SUBJECT = 'Bills'
# Parameters are (name, formatted_owestring)
MSG = '''\
Hey %s,

You owe:
%s
Thanks,
'''
# Parameters are (amount, billname, due_date_string)
OWESTRING = "    $%.2f for %s which is due on %s \n"

ERRMSG_SUBJECT = 'Error in bills script!'
# Parameters are (error)
ERRMSG = '''\
Error:
    %s
'''

# Set to true to print smtp debug info
DEBUG_LEVEL = False

# Location of log file
LOGFILE = None

# Uncomment when debugging to prevent sending out emails to people
#EMAILS = {
#}
