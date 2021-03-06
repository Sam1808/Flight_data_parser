import argparse
import csv
import datetime
import itertools
import os

FLIGHT_PATHS = list()


def parce_csv_file(filepath: str):
    catalog = list()
    with open(filepath, 'r') as csv_file:
        for row in csv.DictReader(csv_file):
            catalog.append(row)
    return catalog


def get_direct_flights(
        flights: list,
        origin: str,
        destination: str,
):
    origins = set()
    destinations = set()
    direct_flights = list()
    for flight in flights.copy():
        origins.add(flight['origin'])
        destinations.add(flight['destination'])
        if flight['origin'] == origin and flight['destination'] == destination:
            direct_flights.append([flight])
            flights.remove(flight)

    origin_error = True if origin not in origins else False
    destination_error = True if destination not in destinations else False

    return direct_flights, flights, origin_error, destination_error


def create_flights_graf(flights: list):
    graf = dict()
    for flight in flights:
        if not graf.get(flight['origin']):
            graf[flight['origin']] = set()
        graf[flight['origin']].add(flight['destination'])
    return graf


def dfs_search(graph, start, end, path=[]):
    global FLIGHT_PATHS
    path = path + [start]
    if start == end:
        FLIGHT_PATHS.append(path)
    for node in graph[start]:
        if node not in path:
            dfs_search(graph, node, end, path)


def select_comfort_flights(connecting_flights: list):
    comfort_flights = list()

    for flight_path in FLIGHT_PATHS:
        path_flights = list()
        for number in range(len(flight_path)-1):
            all_flights = list()
            for flight in connecting_flights:
                if flight['origin'] == flight_path[number] and flight['destination'] == flight_path[number + 1]:
                    all_flights.append(flight)
            path_flights.append(all_flights)
        possible_flights = list(itertools.product(*path_flights))
        for flight in possible_flights:
            comfort_flight = check_flight_date(list(flight))
            if comfort_flight:
                comfort_flights.append(comfort_flight)

    return comfort_flights


def check_flight_date(flights: list, less=1, more=6):
    less = less * 3600
    more = more * 3600
    for number, flight in enumerate(flights):
        next_number = number + 1
        if next_number == len(flights):
            break
        arrival_time = flight['arrival']
        departure_time = flights[next_number]['departure']
        arrival_datetime = datetime.datetime.strptime(
            arrival_time,
            '%Y-%m-%dT%H:%M:%S',
        )
        departure_datetime = datetime.datetime.strptime(
            departure_time,
            '%Y-%m-%dT%H:%M:%S',
        )
        delta = departure_datetime - arrival_datetime
        if delta.total_seconds() < less or delta.total_seconds() > more:
            return None
    return flights


def generate_total_result(
        flights: list,
        origin: str,
        destination: str,
        bags_count: int,
):
    total_result = list()
    for flight_set in flights:
        trip = dict()
        trip['flights'] = flight_set
        departure = flight_set[0]['departure']
        flight_set_price = float()
        arrival = None
        bags_allowed = list()
        for segment in flight_set:
            arrival = segment['arrival']
            flight_set_price += float(segment['base_price'])
            bags_allowed.append(int(segment['bags_allowed']))
        trip['total_price'] = float(flight_set_price)
        trip['origin'] = origin
        trip['destination'] = destination
        total_bags = min(bags_allowed)
        trip['bags_allowed'] = total_bags
        departure_datetime = datetime.datetime.strptime(
            departure,
            '%Y-%m-%dT%H:%M:%S',
        )
        arrival_datetime = datetime.datetime.strptime(
            arrival,
            '%Y-%m-%dT%H:%M:%S',
        )
        delta = arrival_datetime - departure_datetime
        trip['travel_time'] = str(delta)
        trip['bags_count'] = bags_count
        if bags_count:
            if bags_count > total_bags:
                continue
            bags_price = 0.0
            for segment in flight_set:
                bags_price += float(segment['bag_price']) * bags_count
            trip['total_price'] = flight_set_price + bags_price

        total_result.append(trip)
    return total_result


def sort_by_price(flight):
    return flight['total_price']


def main(
        origin: str,
        destination: str,
        file: str,
        bags_count: int,
):
    all_flights = parce_csv_file(file)
    direct_flights, connecting_flights, origin_error, destination_error = get_direct_flights(
        all_flights,
        origin,
        destination
    )

    if origin_error:
        print(f'''
                Cannot find origin airport: {origin}
                Please check and try again
                ''')
        raise KeyError
    elif destination_error:
        print(f'''
                Cannot find destination airport: {destination}
                Please check and try again
                ''')
        raise KeyError

    graf = create_flights_graf(connecting_flights)

    dfs_search(graf, origin, destination)

    comfort_flights = select_comfort_flights(connecting_flights)
    total_flights = direct_flights + comfort_flights

    total_result = generate_total_result(
        total_flights,
        origin,
        destination,
        bags_count
    )

    total_result = sorted(total_result, key=sort_by_price)
    print(f'Trip from {origin} to {destination}')
    print(total_result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Process options for flight parcer'
    )
    parser.add_argument(
        'ORG',
        type=str,
        help='Origin airport')
    parser.add_argument(
        'DST',
        type=str,
        help='Destination airport')
    parser.add_argument(
        'PATH',
        type=str,
        help='Input path to data csv file')
    parser.add_argument(
        '--bags',
        default=0,
        type=int,
        help='Input bags count')
    parser.add_argument(
        '--return',
        dest='back',
        help='Do you want to return?',
        default=False,
        action='store_true'
    )
    options = parser.parse_args()

    origin = str(options.ORG).upper()
    destination = str(options.DST).upper()
    file = options.PATH
    bags_count = options.bags
    is_back = options.back

    if not os.path.exists(file):
        print(f'''
            Something wrong with filepath: {file}
            Please check and try again
    ''')
        raise FileExistsError

    main(origin, destination, file, bags_count)
    if is_back:
        origin, destination = destination, origin
        main(origin, destination, file, bags_count)
