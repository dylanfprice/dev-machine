import jinja2
import os
import cgi
import datetime
import urllib
import webapp2

from model import *

from google.appengine.ext import db
from google.appengine.api import users

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

BILL_KEY = 'bill'

class SeeBill(webapp2.RequestHandler):
    def get(self):
        bill = Bill.get_or_insert(BILL_KEY)
        template_values = {'bill': bill}

        template = jinja_env.get_template('templates/index.html')
        self.response.out.write(template.render(template_values))

class EditBill(webapp2.RequestHandler):
    def get(self):
        bill = Bill.get_or_insert(BILL_KEY)
        template_values = {'bill': bill}

        template = jinja_env.get_template('templates/edit_bill.html')
        self.response.out.write(template.render(template_values))

    def post(self):
        bill = Bill.get_or_insert(BILL_KEY)
        bill.content = self.request.get('content')
        bill.put()
        self.redirect('/')

app = webapp2.WSGIApplication([('/', SeeBill),
                               ('/edit', EditBill)],
                              debug=True)
