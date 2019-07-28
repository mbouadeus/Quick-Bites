from py import login, location
import json
from google.appengine.api import urlfetch

def parse_info(res):
    content = {}

    content['name'] = res['name']
    content['place_id'] = res['place_id']

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

    if filters is None: # If no filters applied
        for res in content['results']:
            restaurants.append(parse_info(res))
    else:
        for res in content['results']:
            # if 'price_level' in res:
            #     if res['price_level'] <= filters['price_level'] and res['opening_hours']['open_now']: #filter based on price levle and if currently open
            if restaurant_match_filters(res, filters):
                restaurants.append(parse_info(res))

    return restaurants

def restaurant_match_filters(res, filters):
    flag = True

    if not (flag and 'price_level' in res and res['price_level'] <= int(filters['price_level'])):
        flag = False
    if not (flag and 'opening_hours' in res and res['opening_hours']['open_now']):
        flag = False
    if not (flag and 'rating' in res and res['rating'] <= int(filters['rating'])):
        flag = False

    return flag

def merge_restaurants(res_ary):
    results = []
    for res in res_ary:
        results += res['results']

    res = {'results': []}
    ids = []

    for restaurant in results:
        if restaurant['place_id'] not in ids:
            res['results'].append(restaurant)
            ids.append(restaurant['place_id'])

    return res

def get_restaurants(coordinates, filters, res_filter):
    print(filters)
    if filters:
        radius = str(int(filters['radius']) * 1610) # converting meters to miles
    else:
        radius = '8047' # default radius

    if res_filter == 'featured':
        res1 = json.loads(urlfetch.fetch('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + str(coordinates[0]) + ',' + str(coordinates[1]) + '&radius=' + radius + '&type=cafe&key=AIzaSyBaL3Iw07VGFL5-PklkXrYas6lwi8NQQno').content)
        res2 = json.loads(urlfetch.fetch('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + str(coordinates[0]) + ',' + str(coordinates[1]) + '&radius=' + radius + '&type=restaurant&key=AIzaSyBaL3Iw07VGFL5-PklkXrYas6lwi8NQQno').content)

        if filters and filters['cuisine'] != 'any':
            res3 = json.loads(urlfetch.fetch('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + str(coordinates[0]) + ',' + str(coordinates[1]) + '&radius=' + radius + '&type=cafe&keyword' + filters['cuisine'] + '&key=AIzaSyBaL3Iw07VGFL5-PklkXrYas6lwi8NQQno').content)
            res4 = json.loads(urlfetch.fetch('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + str(coordinates[0]) + ',' + str(coordinates[1]) + '&radius=' + radius + '&type=restaurant&keyword' + filters['cuisine'] + '&key=AIzaSyBaL3Iw07VGFL5-PklkXrYas6lwi8NQQno').content)
            return merge_restaurants([res3, res4, res1, res2])
        else:
            return merge_restaurants([res1, res2])
    else:
        res1 = json.loads(urlfetch.fetch('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + str(coordinates[0]) + ',' + str(coordinates[1]) + '&radius=' + radius + '&type=cafe&keyword=' + res_filter + '&key=AIzaSyBaL3Iw07VGFL5-PklkXrYas6lwi8NQQno').content)
        res2 = json.loads(urlfetch.fetch('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + str(coordinates[0]) + ',' + str(coordinates[1]) + '&radius=' + radius + '&type=restaurant&keyword=' + res_filter + '&key=AIzaSyBaL3Iw07VGFL5-PklkXrYas6lwi8NQQno').content)

        if filters and filters['cuisine'] != 'any':
            res3 = json.loads(urlfetch.fetch('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + str(coordinates[0]) + ',' + str(coordinates[1]) + '&radius=' + radius + '&type=cafe&keyword=' + filters['cuisine'] + '&key=AIzaSyBaL3Iw07VGFL5-PklkXrYas6lwi8NQQno').content)
            res4 = json.loads(urlfetch.fetch('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + str(coordinates[0]) + ',' + str(coordinates[1]) + '&radius=' + radius + '&type=restaurant&keyword=' + filters['cuisine'] + '&key=AIzaSyBaL3Iw07VGFL5-PklkXrYas6lwi8NQQno').content)
            return merge_restaurants([res3, res4, res1, res2])
        else:
            return merge_restaurants([res1, res2])
