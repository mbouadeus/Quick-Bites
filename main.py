import webapp2
import os
import jinja2
from google.appengine.api import urlfetch
import json

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Featured Page')

class BreakfastHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Breakfast Page')

class LunchHanlder(webapp2.RequestHandler):
    def get(self):
        self.response.write('Lunch Page')

class DinnerHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Dinner Page')

class SettingsHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Settings Page')


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/breakfast', BreakfastHandler),
    ('/lunch', LunchHanlder),
    ('/dinner', DinnerHandler),
    ('/settings', SettingsHandler)
], debug=True)
