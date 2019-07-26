from py import login, location
import json
from google.appengine.api import urlfetch

def parse_info(res):
    content = {}

    content['name'] = res['name']


    if 'vicinity' in res:
        content['address'] = res['vicinity']
    else:
        content['address'] = None

    if 'icon' in res:
        content['icon'] = res['icon']
    else:
        content['icon'] = None

    if 'rating' in res:
        content['rating'] = res['rating']
    else:
        content['rating'] = None

    return content

def parse_restaurants(content, filters):
    restaurants = []

    print(content)
    if filters is None: # If no filters applied
        print("This is something else")
        for res in content['results']:
            restaurants.append(parse_info(res))
    else:
        print(content)
        for res in content['results']:
            if 'price_level' in res:
                if res['price_level'] <= filters['price_level'] and res['opening_hours']['open_now']: #filter based on price levle and if currently open
                    restaurants.append(parse_info(res))

    return restaurants

def get_restaurants(coordinates, filters):
    print("this is from get_restaurants method")
    if filters:
        radius = str(int(filters['radius']) * 1610) # converting meters to miles
    else:
        radius = '8047' # default radius



    res = json.loads(urlfetch.fetch('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + str(coordinates[0]) + ',' + str(coordinates[1]) + '&radius=' + radius + '&type=cafe&key=AIzaSyBaL3Iw07VGFL5-PklkXrYas6lwi8NQQno').content)
    print(res)
    return res
