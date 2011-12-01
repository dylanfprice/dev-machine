import config
from datetime import date

def extract_owestrings(parse):
    emails = {}
    owe = extract_owe(parse)
    for name in owe.keys():
        emails[name] = {}
        emails[name]['owestring'] = ""
        total = 0
        for bill in owe[name]:
            total = total + bill['amount']
            emails[name]['owestring'] += config.OWESTRING % \
                (bill['amount'], bill['bill'], bill['due_date'].strftime("%A, %B %d"))
        emails[name]['total'] = total
    return emails

def extract_owe(parse):
    owe = {}
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
                    if not name in owe:
                        owe[name] = []
                    owe[name].append({'amount' : amount, 'bill' : bill['bill'], 'due_date' : bill['due_date']})
    return owe


