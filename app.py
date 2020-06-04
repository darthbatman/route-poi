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
    # TODO: implement
    pass


def filter_coordinates(coordinates, dist_apart):
    # TODO: implement
    pass


def get_first_route_towns(towns):
    if towns[0] in towns[2:]:
        return towns[:towns[2:].index(towns[0]) + 2]


def get_route_poi(start, dest):
    url = build_request_url(start, dest)
    res = requests.get(url)

    coordinates = get_directions_coordinates(res.text)
    coordinates = filter_coordinates(coordinates, 0.2)

    towns = get_towns(coordinates, dest)
    towns = get_first_route_towns(towns)
    towns = list(dict.fromkeys(towns))


if __name__ == '__main__':
    start = '58 Frost Avenue East, Edison, NJ'
    dest = '1008 W Main St, Urbana, IL 61801'
    get_route_poi(start, dest)
