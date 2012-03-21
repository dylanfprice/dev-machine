from google.appengine.ext import db

class Bill(db.Model):
  """Models a set of bills."""
  content = db.TextProperty(default='No Bills!')
  last_updated = db.DateTimeProperty(auto_now=True)

def bills_key(bills_name=None):
  """Constructs a datastore key for a Bill entity with bills_name."""
  return db.Key.from_path('Bill', bills_name or 'default_bill')

