import webapp2
import os
import jinja2
from google.appengine.api import urlfetch, users
import json
from py import restaurant, login
import datetime #being used
import time #being used
from google.appengine.ext import ndb

class User(ndb.Model):
  name = ndb.StringProperty()
  email = ndb.StringProperty()
  passw = ndb.StringProperty()
  icon = ndb.IntegerProperty()


class UserPreference(ndb.Model):
    email = ndb.StringProperty()
    is_set = ndb.BooleanProperty()
    likes_coffee = ndb.BooleanProperty()

class Restaurant(ndb.Model):
    restaurant_id = ndb.StringProperty()
    comments_reviewer = ndb.StringProperty(repeated=True)
    comments_rating = ndb.StringProperty(repeated=True)
    comments_time = ndb.DateTimeProperty(repeated=True)
    comments_message = ndb.StringProperty(repeated=True)

class ProfileImages(ndb.Model):
    image_id = ndb.IntegerProperty()
    url = ndb.StringProperty()

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def main_page_input(filters, coordinates, email, page):
    res_input = { # retrieving all main page template parameters
        'login_msg': login.get_login_msg(email, get_user_query),
        'login_url': login.get_login_url(email),
        'login_status': login.get_login_status(email),
        'lat': coordinates[0],
        'lng': coordinates[1],
        'restaurants': restaurant.parse_restaurants(restaurant.get_restaurants(coordinates, filters, page), filters),
        'page': page,
        }

    if filters: # To refill the filter from when page reload
        res_input['price_level'] = filters['price_level']
        res_input['radius'] = filters['radius']
        res_input['cuisine'] = filters['cuisine']
        res_input['rating'] = filters['rating']
        res_input['hours'] = filters['hours']

    return res_input

def get_user_query(filter):
    res = User.query().filter(User.email==filter).fetch()

    if len(res) == 0:
        return None
    else:
        return res[0]

def get_pref_query(filter):
    res = UserPreference.query().filter(UserPreference.email==filter).fetch()

    if len(res) == 0:
        return None
    else:
        return res[0]

def get_res_reviews_query(filter):
    res = Restaurant.query().filter(Restaurant.restaurant_id==filter).fetch()

    if res:
        return res[0]
    else:
        return None

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(jinja_env.get_template('templates/getlocation.html').render({
            'page_url': '/'
        }))

    def post(self):
        email = self.request.cookies.get('email')

        if (self.request.get('radius')):
            filters = {
                'price_level': self.request.get('price_level'),
                'radius': self.request.get('radius'),
                'cuisine': self.request.get('cuisine'),
                'rating': self.request.get('rating'),
                'hours': self.request.get('hours')
            }
            coordinates = []
            coordinates.append(self.request.get('lat'))
            coordinates.append(self.request.get('lng'))
            self.response.write(jinja_env.get_template('templates/main.html').render(main_page_input(filters, coordinates, email, 'featured')))
        else:
            coordinates = []
            coordinates.append(self.request.get('lat'))
            coordinates.append(self.request.get('lng'))
            self.response.write(jinja_env.get_template('templates/main.html').render(main_page_input(None, coordinates, email, 'featured')))

class BreakfastHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(jinja_env.get_template('templates/getlocation.html').render({
            'page_url': '/breakfast'
        }))

    def post(self):
        email = self.request.cookies.get('email')

        if (self.request.get('radius')):
            filters = {
                'price_level': self.request.get('price_level'),
                'radius': self.request.get('radius'),
                'cuisine': self.request.get('cuisine'),
                'rating': self.request.get('rating'),
                'hours': self.request.get('hours')
            }
            coordinates = []
            coordinates.append(self.request.get('lat'))
            coordinates.append(self.request.get('lng'))
            self.response.write(jinja_env.get_template('templates/main.html').render(main_page_input(filters, coordinates, email, 'breakfast')))
        else:
            coordinates = []
            coordinates.append(self.request.get('lat'))
            coordinates.append(self.request.get('lng'))
            self.response.write(jinja_env.get_template('templates/main.html').render(main_page_input(None, coordinates, email, 'breakfast')))

class LunchHanlder(webapp2.RequestHandler):
    def get(self):
        self.response.write(jinja_env.get_template('templates/getlocation.html').render({
            'page_url': '/lunch'
        }))

    def post(self):
        email = self.request.cookies.get('email')

        if (self.request.get('radius')):
            filters = {
                'price_level': self.request.get('price_level'),
                'radius': self.request.get('radius'),
                'cuisine': self.request.get('cuisine'),
                'rating': self.request.get('rating'),
                'hours': self.request.get('hours')
            }
            coordinates = []
            coordinates.append(self.request.get('lat'))
            coordinates.append(self.request.get('lng'))
            self.response.write(jinja_env.get_template('templates/main.html').render(main_page_input(filters, coordinates, email, 'lunch')))
        else:
            coordinates = []
            coordinates.append(self.request.get('lat'))
            coordinates.append(self.request.get('lng'))
            self.response.write(jinja_env.get_template('templates/main.html').render(main_page_input(None, coordinates, email, 'lunch')))

class DinnerHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(jinja_env.get_template('templates/getlocation.html').render({
            'page_url': '/dinner'
        }))

    def post(self):
        email = self.request.cookies.get('email')

        if (self.request.get('radius')):
            filters = {
                'price_level': self.request.get('price_level'),
                'radius': self.request.get('radius'),
                'cuisine': self.request.get('cuisine'),
                'rating': self.request.get('rating'),
                'hours': self.request.get('hours')
            }
            coordinates = []
            coordinates.append(self.request.get('lat'))
            coordinates.append(self.request.get('lng'))
            self.response.write(jinja_env.get_template('templates/main.html').render(main_page_input(filters, coordinates, email, 'dinner')))
        else:
            coordinates = []
            coordinates.append(self.request.get('lat'))
            coordinates.append(self.request.get('lng'))
            self.response.write(jinja_env.get_template('templates/main.html').render(main_page_input(None, coordinates, email, 'dinner')))

class RestaurantHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect('/')

    def post(self):
        email = self.request.cookies.get('email')

        res_info = self.request.get('restaurant_info')
        res_info = res_info.split('~')

        template_vars = {
            'id': res_info[0],
            'icon': res_info[1],
            'name': res_info[2],
            'address': res_info[3],
            'rating': res_info[4]
        }

        user = get_user_query(email)
        if user:
            template_vars['user'] = user.name

        res_comments = Restaurant.query().filter(Restaurant.restaurant_id==res_info[0]).fetch()

        if res_comments:
            template_vars['comments'] = res_comments[0]
            template_vars['amount_comments'] = len(res_comments[0].comments_message)

        self.response.write(jinja_env.get_template('templates/restaurant.html').render(template_vars))

class ReviewHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect('/')
    def post(self):
        id = self.request.get('id')
        user = self.request.get('user')
        print(user)
        name = self.request.get('name')
        print(name)
        message = self.request.get('review_message')
        rating = self.request.get('review_rating')
        date = datetime.datetime.now()

        res = get_res_reviews_query(id)

        if res: #add review to restaurant
            res.comments_reviewer.append(user)
            res.comments_rating.append(rating)
            res.comments_time.append(date)
            res.comments_message.append(message)
            res.put()
        else: #create restaurant
            Restaurant(restaurant_id=id, comments_reviewer=[name], comments_rating=[rating], comments_time=[date], comments_message=[message]).put()
            print('restaurant review created')

        #redirect to same page
        self.response.write(jinja_env.get_template('templates/reviewredirect.html').render({
            'place_id': id,
            'icon': self.request.get('icon'),
            'name': name,
            'address': self.request.get('address'),
            'rating': rating
        }))


class SignUpHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(jinja_env.get_template('templates/signUp.html').render())

class SettingsHandler(webapp2.RequestHandler):
    def get(self):
        email = self.request.cookies.get('email')

        if email and email != 'empty':
            res = get_user_query(email)


            icon = ProfileImages.query().filter(ProfileImages.image_id==res.icon).fetch()[0].url

            user = get_user_query(email)
            user_pref = get_pref_query(email)


            template_vars = {
                'login_msg': login.get_login_msg(email, get_user_query),
                'login_status': login.get_login_status(email),
                'login_url': login.get_login_url(email),
                'first_name': res.name.split(' ')[0],
                'profile_pic': icon,
                'user': user,
                'user_pref': user_pref
            }

            self.response.write(jinja_env.get_template('templates/settings.html').render(template_vars))
        else:
            self.redirect('/')

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

        if res and res.passw == user_pass:
            self.response.headers.add_header('Set-Cookie','email=' + str(user_email)) #Setting email in cookie
            self.redirect('/')
        else:
            self.response.write(jinja_env.get_template('templates/login.html').render({
                'form_invalid': True
            }))

class HomePageHandler(webapp2.RequestHandler):
    def get(self):
        preference_template = jinja_env.get_template('templates/homePage.html')
        self.response.write(preference_template.render())

class GLoginHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            email = str(user.email())
            res = get_user_query(email)
            print(res)
            print('google user found')
            if res:
                self.response.headers.add_header('Set-Cookie','email=' + email) #Setting email in cookie
                print('google user registered')
                self.redirect('/')
            else:
                print('google user not registered')
                print(email)
                self.redirect('/signup')
        else:
            print('google user not found')
            glogin = users.create_login_url('/glogin')
            self.redirect(glogin)

class GSignUpHandler(webapp2.RequestHandler):
    def get(self):
        pass

class LogoutHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers.add_header("Set-Cookie", 'email=empty') #Delete cookie

        # user = users.get_current_user() # if google logged in
        print('logging out')
        self.redirect('/')

class SignUpHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user() # Get user if logged in

        if user:
            template_vars = {
                'email': user.nickname() + '@gmail.com',
            }

        signup_template = jinja_env.get_template('templates/signup.html')
        self.response.write(signup_template.render())

    def post(self):
        name = self.request.get('first_name').replace(' ', '') + " " + self.request.get('last_name').replace(' ', '')

        email = self.request.get('email')
        passw = self.request.get('passw1')

        user = User(name=name, email=email, passw=passw, icon=1)
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

class UpdateProfileHandler(webapp2.RequestHandler):
    def get(self):
        self.redirect('/settings')

    def post(self):
        email = self.request.cookies.get('email')

        user = get_user_query(email)

        if user:
            user.email = self.request.get('email')
            user.name = self.request.get('first_name').replace(' ', '') + ' ' + self.request.get('last_name').replace(' ', '')
            user.passw = self.request.get('passw')
            user.put()
            time.sleep(1)
            self.redirect('/settings')
        else:
            self.redirect('/settings')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/homepage', HomePageHandler),
    ('/breakfast', BreakfastHandler),
    ('/lunch', LunchHanlder),
    ('/dinner', DinnerHandler),
    ('/restaurant', RestaurantHandler),
    ('/review', ReviewHandler),
    ('/settings', SettingsHandler),
    # ('/setlocation', SetLocationHandler),
    ('/login', LoginHandler),
    ('/glogin', GLoginHandler),
    ('/logout', LogoutHandler),
    ('/signup', SignUpHandler),
    ('/gsignup', GSignUpHandler),
    ('/preferences', PreferencesHandler),
    ('/updateprofile', UpdateProfileHandler),
], debug=True)
