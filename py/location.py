
from google.appengine.api import urlfetch
import json

def get_coordinates():
    api_key = 'AIzaSyBaL3Iw07VGFL5-PklkXrYas6lwi8NQQno'
    url = 'https://www.googleapis.com/geolocation/v1/geolocate?key=' + api_key

    response = json.loads(urlfetch.fetch(url, method="POST").content)

    return [response['location']['lat'], response['location']['lng']]
    # return coordinates
