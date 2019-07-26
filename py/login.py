from google.appengine.api import urlfetch, users

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
