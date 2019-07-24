import webapp2
import os
import jinja2
from google.appengine.api import urlfetch, users
import json

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def login_msg():
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

def get_coordinates(location):
    api_key = 'AIzaSyBaL3Iw07VGFL5-PklkXrYas6lwi8NQQno'
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + location.replace(' ', '+') + '&key=' + api_key

    response = json.loads(urlfetch.fetch(url).content)
    coordinates = response['results'][0]['geometry']['location']

    return [coordinates['lat'], coordinates['lng']]

def get_restaurants(coordinates):
    return json.loads(urlfetch.fetch('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + str(coordinates[0]) + ',' + str(coordinates[1]) + '&radius=500&type=restaurant&key=AIzaSyBaL3Iw07VGFL5-PklkXrYas6lwi8NQQno').content)

def parse_restaurants(content):
    print(content)
    restaurants = []

    for res in content['candidates']:
        restaurants.append(res['name'])

    return restaurants

class MainHandler(webapp2.RequestHandler):
    def get(self):
        main_tamplate = jinja_env.get_template('templates/main.html')
        self.response.write(main_tamplate.render({
            'login_msg': login_msg(),
            'login_url': get_login_url(),
            'login_status': get_login_status()

        }))

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

class ResultsHandler(webapp2.RequestHandler):
    def post(self):
        location = self.request.get('location')
        coordinates = get_coordinates(location)

        content = get_restaurants(coordinates)

        restaurants = parse_restaurants(content)

        results_template = jinja_env.get_template('templates/results.html')
        self.response.write(results_template.render({
            'location': str(coordinates[0]) + ', ' + str(coordinates[1]),
            'restaurants': restaurants
        }))





# class LoginHandler(webapp2.RequestHandler):
#     def get(self):
#         if users.get_current_user():
#             self.redirect('/')
#             print('Already logged in')
#         else:
#             print('Logging in')
#             login_url = users.create_login_url('/') #Get time and pick (breakfast, lunch, or dinner)
#
# class LogoutHandler(webapp2.RequestHandler):
#     def get(self):
#         if users.get_current_user():
#             print('Logging out')
#             logout_url = users.create_logout_url('/')
#         else:
#             print('Already logged out')
#             self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/breakfast', BreakfastHandler),
    ('/lunch', LunchHanlder),
    ('/dinner', DinnerHandler),
    ('/settings', SettingsHandler),
    ('/results', ResultsHandler)
    # ('/login', LoginHandler),
    # ('/logout', LogoutHandler),

], debug=True)
