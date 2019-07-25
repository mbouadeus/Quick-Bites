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

    if filters == None: # If no filters applied
        for res in content['results']:
            restaurants.append(parse_info(res))
    else:
        for res in content['results']:
            if 'price_level' in res:
                if res['price_level'] <= filters['price_level'] and res['opening_hours']['open_now']: #filter based on price levle and if currently open
                    restaurants.append(parse_info(res))

    return restaurants
