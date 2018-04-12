import json
import math
import argparse


def load_data(file_path='bars.json'):
    with open(file_path, 'r', encoding='utf-8') as data_file:
        bar_data = json.load(data_file)
    return bar_data


def get_biggest_bar(bars_info):
    biggest_bar_info = max(bars_info, key=lambda x:
                           x['properties']['Attributes']['SeatsCount']
                           )
    biggest_bar_name = biggest_bar_info['properties']['Attributes']['Name']
    return biggest_bar_name


def get_smallest_bar(bars_info):
    smallest_bar_info = min(bars_info, key=lambda x:
                            x['properties']['Attributes']['SeatsCount']
                            )
    smallest_bar_name = smallest_bar_info['properties']['Attributes']['Name']
    return smallest_bar_name


def get_bar_address(bar_features):
    try:
        bar_address = bar_features['properties']['Attributes']['Address']
    except KeyError:
        bar_address = None
    return bar_address


def get_distance(bar_info, longitude, latitude):
    bar_longitude, bar_latitude = bar_info['geometry']['coordinates']
    distance = math.hypot(bar_longitude - longitude,
                          bar_latitude - latitude)
    return distance

def get_closest_bar(bar_data, longitude, latitude):
    # closest_bar = min(bar_data, key=get_distance(__getitem__,longitude, latitude))
    closest_bar = min(bar_data, key=lambda x: get_distance(x, longitude, latitude))
    return closest_bar
    # first_loop = True
    # closest_bar = None
    # closest_bar_address = None
    # minimal_distance = 0
    # for bar in bar_data:
    #     try:
    #         coordinates = bar['geometry']['coordinates']
    #     except KeyError:
    #         continue
    #     distance = math.hypot(coordinates[0] - longitude,
    #                           coordinates[1] - latitude)
    #     if first_loop:
    #         minimal_distance = distance
    #         closest_bar = bar['properties']['Attributes']['Name']
    #         closest_bar_address = get_bar_address(bar)
    #         first_loop = False
    #     if distance < minimal_distance:
    #         minimal_distance = distance
    #         closest_bar = bar['properties']['Attributes']['Name']
    #         closest_bar_address = get_bar_address(bar)
    # return closest_bar, closest_bar_address


def get_user_coordinates():
    latitude = float(input('Чтобы узнать название самого близкого бара, '
                           'введите свои gps координаты в формате '
                           'DD.DDD.\nШирота: '))
    longitude = float(input('Долгота: '))
    return latitude, longitude


def get_console_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file',
                        help='Если файл с данными называется не "bars.json"'
                             ' и/или файл не лежит в папке скрипта, то '
                             'используйте этот параметр, чтобы указать путь '
                             'к файлу с данными о барах.'
                        )
    args = parser.parse_args()
    return args.file


if __name__ == '__main__':
    path = 'bars.json'
    user_path = get_console_arguments()
    if user_path:
        path = user_path
    bar_info = load_data(path)
    bar_list = bar_info['features']
    biggest_bar = get_biggest_bar(bar_list)
    smallest_bar = get_smallest_bar(bar_list)
    print('Самый большой бар Москвы ', biggest_bar)
    print('Самый маленький бар Москвы: ', smallest_bar)
    while True:
        try:
            lat, long = get_user_coordinates()
            break
        except ValueError:
            print('Широта и долгота должны быть числами')
            continue
    nearest_bar = get_closest_bar(bar_list, long, lat)
    nearest_bar_name = nearest_bar['properties']['Attributes']['Name']
    nearest_bar_address = nearest_bar['properties']['Attributes']['Address']
    print('Ближайший к Вам бар: ', nearest_bar_name,
          '. Он находится по адресу:', nearest_bar_address)
