import webapp2
import os
import jinja2
from google.appengine.api import urlfetch, users
import json
from py import restaurant, login
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

def main_page_input(filters, coordinates):
    res_input = { # retrieving all main page template parameters
        'login_msg': login.get_login_msg(),
        'login_url': login.get_login_url(),
        'login_status': login.get_login_status(),
        'lat': coordinates[0],
        'lng': coordinates[1],
        'restaurants': restaurant.parse_restaurants(restaurant.get_restaurants(coordinates, filters), filters)
        }

    if filters: # To refill the filter from when page reload
        res_input['price_level'] = filters['price_level']
        res_input['radius'] = filters['radius']

    return res_input




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

def get_pref_query(filter):
    res = UserPreference.query().filter(UserPreference.user_id==filter).fetch()

    if res[0].is_set:
        return {
            'user_id': res[0].user_id,
            'likes_coffee': res[0].likes_coffee,
        }
    else:
        return None

class MainHandler(webapp2.RequestHandler):
    def get(self):
        # employee = User(name='Steve Mbouadeu',
        #                     email='mbouadeus@gmail.com',
        #                     passw='examplepass')
        #
        # employee.put()
        #
        # employee_pref = UserPreference(user_id=employee.key)
        # employee_pref.is_set = True
        # employee_pref.likes_coffee = True
        # employee_pref.put()


        # time.sleep(2)
        # users = User.query().filter(User.first_name=='Steve').fetch()
        # last_user = users[len(users)-1]
        #
        # print(last_user)
        # time.sleep(2)
        # user_pref = UserPreference.query().filter(UserPreference.user_id == last_user.key).fetch()
        # print(user_pref[0].likes_coffee)

        # if (self.request.get('lat')):
        #     coordinates = []
        #     coordinates.append(self.request.get('lat'))
        #     coordinates.append(self.request.get('lng'))
        #     self.response.write(jinja_env.get_template('templates/main.html').render(main_page_input(None, coordinates)))
        #
        # else:
        self.response.write(jinja_env.get_template('templates/getlocation.html').render())

    def post(self):
        if (self.request.get('radius')):
            filters = {
                'price_level': self.request.get('price_level'),
                'radius': self.request.get('radius')
            }
            coordinates = []
            coordinates.append(self.request.get('lat'))
            coordinates.append(self.request.get('lng'))
            self.response.write(jinja_env.get_template('templates/main.html').render(main_page_input(filters, coordinates)))
        else:
            coordinates = []
            coordinates.append(self.request.get('lat'))
            coordinates.append(self.request.get('lng'))
            self.response.write(jinja_env.get_template('templates/main.html').render(main_page_input(None, coordinates)))

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

class SetLocationHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect('/?lat=' + self.request.get('lat') + "&lng=" + self.request.get('lng'))


class LoginHandler(webapp2.RequestHandler):
    def get(self):
        login_template = jinja_env.get_template('templates/login.html')
        self.response.write(login_template.render())

    def post(self):
        user_email = self.request.get('email')
        user_pass = self.request.get('passw')

        res = get_user_query(user_email)





app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/breakfast', BreakfastHandler),
    ('/lunch', LunchHanlder),
    ('/dinner', DinnerHandler),
    ('/settings', SettingsHandler),
    ('/login', LoginHandler),
    ('/setlocation', SetLocationHandler)
    # ('/logout', LogoutHandler),

], debug=True)
