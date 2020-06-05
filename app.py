import sys

from route_poi import RoutePOI


def show_usage():
    print('usage: python app.py -s="start_address" -d="dest_address" -p="poi_1,...,poi_n"')


def start_route_poi(args):
    rp = RoutePOI()

    if len(args) == 4 and '-s=' in args[1] and '-d=' in args[2] \
       and '-p=' in args[3]:
        start = args[1].split('=')[1]
        dest = args[2].split('=')[1]
        req_poi = args[3].split('=')[1].split(',')
        r_p = rp.get_route_poi(start, dest, req_poi)
        with open('route_poi.txt', 'w') as f:
            f.write(str(r_p))
            f.close()
    elif len(args) == 3 and '-s=' in args[1] and '-d=' in args[2]:
        start = args[1].split('=')[1]
        dest = args[2].split('=')[1]
        req_poi = ['food', 'gas']
        r_p = rp.get_route_poi(start, dest, req_poi)
        with open('route_poi.txt', 'w') as f:
            f.write(str(r_p))
            f.close()
    else:
        show_usage()


if __name__ == '__main__':
    start_route_poi(sys.argv)
