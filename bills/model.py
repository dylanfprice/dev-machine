from bills_parser import bills_yacc
import config

from datetime import date
from google.appengine.ext import db

class Bills(db.Model):
    """Models a set of bills."""
    content = db.TextProperty(default='No Bills!')
    last_updated = db.DateTimeProperty(auto_now=True)

    def parse(self):
        return bills_yacc.parse(self.content)

    def total(self, name):
        total = 0
        parse = self.parse()
        for bill in parse:
            if self.is_due(bill):
                names = bill['names']
                if name in names:
                    paid = names[name]['paid']
                    if not paid:
                        total += names[name]['amount']
        return total

    def is_due(self, bill):
        timediff = bill['due_date'] - date.today()
        return timediff.days <= config.REMIND_INTERVAL

def bills_key(bills_name=None):
    """Constructs a datastore key for a Bill entity with bills_name."""
    return db.Key.from_path('Bill', bills_name or 'default_bill')

