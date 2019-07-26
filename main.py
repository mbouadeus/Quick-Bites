import webapp2
import os
import jinja2
from google.appengine.api import urlfetch, users
import json
from py import func
import datetime
import time
from google.appengine.ext import ndb

class User(ndb.Model):
  name = ndb.StringProperty()
  email = ndb.StringProperty()
  passw = ndb.StringProperty()


class UserPreference(ndb.Model):
    user_id = ndb.KeyProperty()
    is_set = ndb.BooleanProperty()
    likes_coffee = ndb.BooleanProperty()

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def main_page_input(filters):
    return { # retrieving all main page template parameters
        'login_msg': get_login_msg(),
        'login_url': get_login_url(),
        'login_status': get_login_status(),
        'restaurants': func.parse_restaurants(get_restaurants(get_coordinates(), filters), filters)
        }

def get_coordinates():
    api_key = 'AIzaSyBaL3Iw07VGFL5-PklkXrYas6lwi8NQQno'
    url = 'https://www.googleapis.com/geolocation/v1/geolocate?key=' + api_key

    response = json.loads(urlfetch.fetch(url, method="POST").content)

    print(response)

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


def get_user_query(filter):
    res = User.query().filter(User.email==filter).fetch()

    if len(res) == 0:
        return None
    else:
        return {
            'key': res[0].key,
            'name': res[0].name,
            'email': res[0].email,
            'passw': res[0].passw
        }

class MainHandler(webapp2.RequestHandler):
    def get(self):
        employee = User(name='Steve Mbouadeu',
                            email='mbouadeus@gmail.com',
                            passw='examplepass')

        employee.put()

        employee_pref = UserPreference(user_id=employee.key)
        employee_pref.is_set = True
        employee_pref.likes_coffee = True
        employee_pref.put()


        # time.sleep(2)
        # users = User.query().filter(User.first_name=='Steve').fetch()
        # last_user = users[len(users)-1]
        #
        # print(last_user)
        # time.sleep(2)
        # user_pref = UserPreference.query().filter(UserPreference.user_id == last_user.key).fetch()
        # print(user_pref[0].likes_coffee)

        self.response.write(jinja_env.get_template('templates/main.html').render(main_page_input(None)))

    def post(self):
        filters = {
            'price_level': self.request.get('price_level'),
            'radius': self.request.get('radius')
        }

        self.response.write(jinja_env.get_template('templates/main.html').render(main_page_input(filters)))

class BreakfastHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Breakfast Page')

class LunchHanlder(webapp2.RequestHandler):
    def get(self):
        self.response.write('Lunch Page')

class DinnerHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Dinner Page')

class SignUpHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(jinja_env.get_template('templates/signUp.html').render())

class SettingsHandler(webapp2.RequestHandler):
    def get(self):
        # self.response.write(restaurants.is_here)
        self.response.write(jinja_env.get_template('templates/settings.html').render())

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        login_template = jinja_env.get_template('templates/login.html')
        self.response.write(login_template.render())

    def post(self):
        user_email = self.request.get('email')
        user_pass = self.request.get('passw')

        res = get_user_query(user_email)
class HomePageHandler(webapp2.RequestHandler):
    def get(self):
        preference_template = jinja_env.get_template('templates/homePage.html')
        self.response.write(preference_template.render())

class preferenceHandler(webapp2.RequestHandler):
    def get(self):
        preference_template = jinja_env.get_template('templates/preferences.html')
        self.response.write(preference_template.render())




app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/homePage',HomePageHandler),
    ('/signUp',SignUpHandler),
    ('/breakfast', BreakfastHandler),
    ('/lunch', LunchHanlder),
    ('/dinner', DinnerHandler),
    ('/settings', SettingsHandler),
    ('/login', LoginHandler),
    # ('/logout', LogoutHandler),
    ('/preferences', preferenceHandler),


], debug=True)
