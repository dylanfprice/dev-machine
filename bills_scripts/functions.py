import config
from datetime import date
from decimal import Decimal

def extract_owestrings(parse):
    emails = {}
    owe = extract_owe(parse)
    for name in owe.keys():
        emails[name] = {}
        emails[name]['total'] = owe[name]['total']
        emails[name]['owestring'] = ""
        for bill in owe[name]['bills']:
            emails[name]['owestring'] += config.OWESTRING % \
                (bill['amount'], bill['bill'], bill['due_date'].strftime("%A, %B %d"))
    return emails

def extract_owe(parse):
    owe = {}
    for bill in parse:
        timediff = bill['due_date'] - date.today()
        if timediff.days <= config.REMIND_INTERVAL:
            num_names = len(bill['names'])
            for name in bill['names'].keys():
                amount = Decimal(bill['names'][name][0])
                if amount == -1:
                    amount = Decimal(bill['amount']) / num_names
                amount = round(amount, 2)
                paid = bill['names'][name][1]
                if not paid:
                    if not name in owe:
                        owe[name] = {}
                        owe[name]['bills'] = []
                    owe[name]['bills'].append({'amount' : amount, 'bill' : bill['bill'], 'due_date' : bill['due_date']})
    for name in owe.keys():
        total = 0
        for bill in owe[name]['bills']:
            total = total + bill['amount']
        owe[name]['total'] = total
                    
    return owe


