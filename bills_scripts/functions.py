import config
from datetime import date

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


