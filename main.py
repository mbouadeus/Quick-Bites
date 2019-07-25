import webapp2
import os
import jinja2
from google.appengine.api import urlfetch, users
import json
from py import apis, handlers


jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def main_page_input(filters):
    return { # retrieving all main page template parameters
        'login_msg': get_login_msg(),
        'login_url': get_login_url(),
        'login_status': get_login_status(),
        'restaurants': parse_restaurants(get_restaurants(get_coordinates(), filters), filters)
}

def get_coordinates():
    api_key = 'AIzaSyBaL3Iw07VGFL5-PklkXrYas6lwi8NQQno'
    url = 'https://www.googleapis.com/geolocation/v1/geolocate?key=' + api_key

    response = json.loads(urlfetch.fetch(url, method="POST").content)

    return [response['location']['lat'], response['location']['lng']]

def get_login_msg():
    if users.get_current_user():
        return 'Welcome, ' + users.get_current_user().nickname()
    else:
        return 'Welcome, Guest'

def get_login_url():
    if users.get_current_user():
        return users.create_logout_url('/')
    else:
        return users.create_login_url('/') #Get time and pick (breakfast, lunch, or dinner)

def get_login_status():
    if users.get_current_user():
        return 'logout'
    else:
        return 'login'


def get_restaurants(coordinates, filters):
    if filters:
        radius = str(int(filters['radius']) * 1610) # converting meters to miles
    else:
        radius = '8047' # default radius

    return json.loads(urlfetch.fetch('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + str(coordinates[0]) + ',' + str(coordinates[1]) + '&radius=' + radius + '&type=cafe&key=AIzaSyBaL3Iw07VGFL5-PklkXrYas6lwi8NQQno').content)

def parse_restaurants(content, filters):
    restaurants = []

    if filters == None: # If no filters applied
        for res in content['results']:
            restaurants.append(res['name'])
    else:
        for res in content['results']:
            if 'price_level' in res:
                if res['price_level'] <= filters['price_level'] and res['opening_hours']['open_now']: #filter based on price levle and if currently open
                    restaurants.append(res['name'])

    return restaurants

import webapp2

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(jinja_env.get_template('templates/main.html').render(main_page_input({
            'price_level': 3,
            'radius': '10',
        })))

    def post(self):
        filters = {
            'price_level': '2',
            'radius': '100',
        }

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
        # self.response.write(restaurants.is_here)
        self.response.write(jinja_env.get_template('templates/settings.html').render())

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(jinja_env.get_template('templates/login.html').render())



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/breakfast', BreakfastHandler),
    ('/lunch', LunchHanlder),
    ('/dinner', DinnerHandler),
    ('/settings', SettingsHandler),
    ('/login', LoginHandler),
    # ('/logout', LogoutHandler),

], debug=True)
