import cgi
import config
import datetime
import jinja2
import os
import urllib
import webapp2

from model import *

from google.appengine.ext import db
from google.appengine.api import users

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

BILLS_KEY = 'bills'

class SeeBills(webapp2.RequestHandler):
    def get(self):
        bills = Bills.get_or_insert(BILLS_KEY)
        template_values = {'bills': bills}

        template = jinja_env.get_template('templates/see_bills.html')
        self.response.out.write(template.render(template_values))

class EditBills(webapp2.RequestHandler):
    def get(self):
        bills = Bills.get_or_insert(BILLS_KEY)
        template_values = {'bills': bills}

        template = jinja_env.get_template('templates/edit_bills.html')
        self.response.out.write(template.render(template_values))

    def post(self):
        bills = Bills.get_or_insert(BILLS_KEY)
        bills.content = self.request.get('content')
        bills.put()
        self.redirect('/')

class Total(webapp2.RequestHandler):
    def get(self, name):
        bills = Bills.get_or_insert(BILLS_KEY)
        template_values = {
            'name' : name,
            'greeting' : '',
            'remind_interval': config.REMIND_INTERVAL,
            'host_url' : self.request.host_url,
            'bills': bills
        }

        template = jinja_env.get_template('templates/total_page.html')
        self.response.out.write(template.render(template_values))
        
app = webapp2.WSGIApplication([('/', SeeBills),
                               ('/edit', EditBills),
                               (r'/total', Total),
                               (r'/total/(.*)', Total)],
                              debug=True)
