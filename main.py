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
    email = ndb.StringProperty()
    is_set = ndb.BooleanProperty()
    likes_coffee = ndb.BooleanProperty()

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def main_page_input(filters, coordinates, email):
    res_input = { # retrieving all main page template parameters
        'login_msg': login.get_login_msg(email, get_user_query),
        'login_url': login.get_login_url(email),
        'login_status': login.get_login_status(email),
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
        return res[0]

def get_pref_query(filter):
    res = UserPreference.query().filter(UserPreference.email==filter).fetch()

    return res[0]




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
        email = self.request.cookies.get('email')

        if (self.request.get('radius')):
            filters = {
                'price_level': self.request.get('price_level'),
                'radius': self.request.get('radius')
            }
            coordinates = []
            coordinates.append(self.request.get('lat'))
            coordinates.append(self.request.get('lng'))
            self.response.write(jinja_env.get_template('templates/main.html').render(main_page_input(filters, coordinates, email)))
        else:
            coordinates = []
            coordinates.append(self.request.get('lat'))
            coordinates.append(self.request.get('lng'))
            self.response.write(jinja_env.get_template('templates/main.html').render(main_page_input(None, coordinates, email)))

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

        if res:
            self.response.headers.add_header('Set-Cookie','email=' + str(res.email)) #Setting email in cookie
            self.redirect('/')
        else:
            self.redirect('/login') # Should be rendering user not found message

class LogoutHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers.add_header("Set-Cookie", 'email=empty')
        print('logging out')
        self.redirect('/')

class SignUpHandler(webapp2.RequestHandler):
    def get(self):
        signup_template = jinja_env.get_template('templates/signup.html')
        self.response.write(signup_template.render())
    def post(self):
        name = self.request.get('first_name') + " " + self.request.get('last_name')
        email = self.request.get('email')
        passw = self.request.get('passw1')

        user = User(name=name, email=email, passw=passw)
        user.put()

        UserPreference(email=user.email, is_set=False).put() # Create UserPreference for user

        pref_template = jinja_env.get_template('templates/preferences.html')
        self.response.write(pref_template.render({
            'email': user.email
        }))

class PreferencesHandler(webapp2.RequestHandler):
    def post(self):
        email = str(self.request.get('email'))

        self.response.headers.add_header('Set-Cookie','email=' + email) #Setting email in cookie

        user_pref = get_pref_query(email)
        user_pref.is_set = True
        user_pref.likes_coffee = False # set preferences
        user_pref.put()

        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/signup',SignUpHandler),
    ('/preferences', PreferencesHandler),
    ('/breakfast', BreakfastHandler),
    ('/lunch', LunchHanlder),
    ('/dinner', DinnerHandler),
    ('/settings', SettingsHandler),
    ('/login', LoginHandler),
    ('/setlocation', SetLocationHandler),
    ('/logout', LogoutHandler),


], debug=True)
