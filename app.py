from geopy.geocoders import Nominatim
import requests


def most_common(lst):
    '''
    https://stackoverflow.com/a/1518632
    '''
    return max(set(lst), key=lst.count)


def build_request_url(start, dest):
    api_url = 'https://www.google.com/maps/dir/'
    start = start.replace(' ', '+')
    dest = dest.replace(' ', '+')
    return api_url + start + '/' + dest + '/'


def get_directions_coordinates(html):
    coordinates = []
    tokens = []
    keys = []
    for tok in html.split('[[['):
        tok = tok.split(']')[0]
        if len(tok) > 12 and len(tok) < 100 and \
           tok.count('.') == 3 and ',' in tok and \
           not any(c.isalpha() for c in tok):
            tokens.append(tok)
            keys.append(tok[:tok.index('.')])
    key = most_common(keys)
    for tok in tokens:
        if tok[:len(key)] == key:
            lon = tok.split(',')[1]
            lat = tok.split(',')[2]
            coordinates.append((lat, lon))
    return coordinates


def get_towns(coordinates, dest):
    towns = []
    for c in coordinates:
        locator = Nominatim(user_agent='geocoder')
        coords = str(c[0]) + ', ' + str(c[1])
        location = locator.reverse(coords)
        city_keys = ['town', 'city', 'township', 'hamlet']
        for key in city_keys:
            if key in location.raw['address']:
                city = location.raw['address'][key].lower()
                state = location.raw['address']['state'].lower()
                towns.append(city + ', ' + state)
                break
    return towns


def distance(c1, c2):
    x1 = float(c1[0])
    y1 = float(c1[1])
    x2 = float(c2[0])
    y2 = float(c2[1])
    return ((x2 - x1) ** 2) + ((y2 - y1) ** 2) ** 0.5


def filter_coordinates(coordinates, dist_apart):
    filtered = []
    i = 0
    j = 1
    for _ in coordinates:
        if j < len(coordinates):
            if distance(coordinates[i], coordinates[j]) < dist_apart:
                j += 1
            else:
                filtered.append(coordinates[i])
                i = j
                j += 1
        else:
            if filtered[-1] != coordinates[i]:
                filtered.append(coordinates[i])
            return filtered


def get_first_route_towns(towns):
    if towns[0] in towns[2:]:
        return towns[:towns[2:].index(towns[0]) + 2]


def find_poi(html, poi, town):
    found_poi = []

    tok_1 = '[[\\\"' + poi + ' near ' + town
    tok_2 = '[\\\"' + poi + '\\\"]\\n]'
    tok_3 = ', '
    tok_4 = ',[[\\\"'
    tok_5 = '\\\"]\\n'
    tok_6 = '[\\\"'
    tok_7 = ','

    for tok in html.split(tok_1)[1].split(tok_2)[0].lower() \
                   .split(town.split(tok_3)[0] + tok_3):
        if len(tok) > 200 and len(tok[-200:].split(tok_4)) > 1:
            place = tok[-200:].split(tok_4)[1].split(tok_7)[0].split(tok_5)[0]
            address = tok[-200:].split(tok_4)[1].split(tok_7)[1] \
                                .split(tok_5)[0] \
                                .replace(tok_6, '') + tok_3 + town
            found_poi.append({'name': place, 'address': address})

    return found_poi


def get_poi(towns, req_poi):
    api_url = 'https://www.google.com/maps/search/'
    town_pois = {}

    for town in towns:
        town_poi = {}
        for poi in req_poi:
            url = api_url + poi + '+near+' + town.replace(' ', '+') + '/'
            res = requests.get(url)
            found = find_poi(res.text, poi, town)
            town_poi[poi] = found
        town_pois[town] = town_poi

    return town_pois


def get_route_poi(start, dest, req_poi):
    url = build_request_url(start, dest)
    res = requests.get(url)

    coordinates = get_directions_coordinates(res.text)
    coordinates = filter_coordinates(coordinates, 0.2)

    towns = get_towns(coordinates, dest)
    towns = get_first_route_towns(towns)
    towns = list(dict.fromkeys(towns))

    return get_poi(towns, req_poi)


if __name__ == '__main__':
    start = '58 Frost Avenue East, Edison, NJ'
    dest = '1008 W Main St, Urbana, IL 61801'
    req_poi = ['food', 'gas']
    route_poi = get_route_poi(start, dest, req_poi)
    print(route_poi)
