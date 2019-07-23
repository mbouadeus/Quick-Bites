import webapp2
import os
import jinja2
from google.appengine.api import urlfetch
import json

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def loginStatus()
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

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.redirect('/')
        else:
            login_url = users.create_login_url('/') #Get time and pick (breakfast, lunch, or dinner)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/breakfast', BreakfastHandler),
    ('/lunch', LunchHanlder),
    ('/dinner', DinnerHandler),
    ('/settings', SettingsHandler),
    ('/login', LoginHandler),
    ('/logout', LogoutHandler),

], debug=True)
