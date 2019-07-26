from google.appengine.api import urlfetch, users

def get_login_msg(email, query):
    if email != "empty":
        res = query(email)
        return 'Welcome, ' + res.name #users.get_current_user().nickname()
    else:
        return 'Welcome, Guest'


def get_login_url(email):
    if email != "empty":
        # return users.create_logout_url('/')
        return '/logout'
    else:
        # return users.create_login_url('/') #Get time and pick (breakfast, lunch, or dinner)
        return '/login'

def get_login_status(email):
    if email != "empty":
        return 'logout'
    else:
        return 'login'
