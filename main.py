import csv
import datetime
import itertools


paths = []


def myDFS(graph, start, end, path=[]):
    global paths
    path = path + [start]
    if start == end:
        paths.append(path)
    for node in graph[start]:
        if node not in path:
            myDFS(graph, node, end, path)


def check_flight_date(flights: list, less=1, more=6):
    less = less * 3600
    more = more * 3600
    for number, flight in enumerate(flights):
        n_n = number + 1
        if n_n == len(flights):
            break
        ar = flight['arrival']
        dep = flights[n_n]['departure']
        ar_datetime = datetime.datetime.strptime(
            ar,
            '%Y-%m-%dT%H:%M:%S',
        )
        dep_datetime = datetime.datetime.strptime(
            dep,
            '%Y-%m-%dT%H:%M:%S',
        )
        delta = dep_datetime - ar_datetime
        if delta.total_seconds() < less or delta.total_seconds() > more:
            return None
    return flights


def sort_by_price(flight):
    return flight['total_price']

if __name__ == '__main__':
    file = 'example/example1.csv'

    origin = 'DHE'
    destination = 'NRX'
    bags_count = 0

    all_flights = list()
    with open(file, 'r') as csv_file:
        for row in csv.DictReader(csv_file):
            all_flights.append(row)

    result = list()

    for flight in all_flights.copy():
        if flight['origin'] == origin and flight['destination'] == destination:
            result.append([flight])
            all_flights.remove(flight)

    graf = dict()

    for flight in all_flights:
        if not graf.get(flight['origin']):
            graf[flight['origin']] = set()
        graf[flight['origin']].add(flight['destination'])


    print(origin, 'to', destination)

    myDFS(graf, origin, destination)

    for path in paths:
        print('path:', path)
        temp_a = []
        for ind in range(len(path)-1):
            temp_b = []
            for flight in all_flights:
                if flight['origin'] == path[ind] and flight['destination'] == path[ind+1]:
                    temp_b.append(flight)
            temp_a.append(temp_b)
        av_flights = list(itertools.product(*temp_a))
        for av in av_flights:
            app = check_flight_date(list(av))
            if app:
                result.append(app)
    total_result = list()

    for el in result:
        element = dict()
        element['flights'] = el
        departure = el[0]['departure']
        total_f_price = 0.0
        arrival = None
        bags_allowed = list()
        for x in el:
            arrival = x['arrival']
            total_f_price += float(x['base_price'])
            bags_allowed.append(int(x['bags_allowed']))

        element['total_price'] = float(total_f_price)
        element['origin'] = origin
        element['destination'] = destination
        total_bags = min(bags_allowed)
        element['bags_allowed'] = total_bags
        dep_datetime = datetime.datetime.strptime(
            departure,
            '%Y-%m-%dT%H:%M:%S',
        )
        ar_datetime = datetime.datetime.strptime(
            arrival,
            '%Y-%m-%dT%H:%M:%S',
        )
        delta = ar_datetime - dep_datetime
        element['travel_time'] = str(delta)
        element['bags_count'] = bags_count
        if bags_count:
            if bags_count > total_bags:
                continue
            bags_price = 0.0
            for x in el:
                bags_price += float(x['bag_price'])*bags_count
            element['total_price'] = total_f_price + bags_price

        total_result.append(element)

    total_result = sorted(total_result, key=sort_by_price)

