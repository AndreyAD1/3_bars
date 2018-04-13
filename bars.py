import json
import math
import argparse


def load_data(file_path='bars.json'):
    with open(file_path, 'r', encoding='utf-8') as data_file:
        try:
            bar_data = json.load(data_file)
        except json.decoder.JSONDecodeError:
            bar_data = None
    return bar_data


def get_biggest_bar(bars_info):
    biggest_bar = max(
        bars_info,
        key=lambda x: x['properties']['Attributes']['SeatsCount']
    )
    return biggest_bar


def get_smallest_bar(bars_info):
    smallest_bar = min(
        bars_info,
        key=lambda x: x['properties']['Attributes']['SeatsCount']
    )
    return smallest_bar


def get_distance(bar, longitude, latitude):
    bar_longitude, bar_latitude = bar['geometry']['coordinates']
    distance = math.hypot(bar_longitude - longitude,
                          bar_latitude - latitude)
    return distance


def get_closest_bar(bar_data, longitude, latitude):
    closest_bar = min(
        bar_data,
        key=lambda x: get_distance(x, longitude, latitude)
    )
    return closest_bar


def get_user_coordinates():
    latitude = float(input('Чтобы узнать название самого близкого бара, '
                           'введите свои gps координаты в формате '
                           'DD.DDD.\nШирота: '))
    longitude = float(input('Долгота: '))
    return latitude, longitude


def get_console_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--file',
        default='bars.json',
        help='Если файл с данными называется не "bars.json" и/или файл не лежит'
             ' в папке скрипта, то используйте этот параметр, чтобы указать'
             ' путь к файлу с данными о барах.'
    )
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    user_file_path = get_console_arguments().file
    try:
        bar_info = load_data(user_file_path)
    except FileNotFoundError:
        exit('Не удалось найти файл с данными о барах.')
    if not bar_info:
        exit('Указанный файл не содержит данные в формате json.')
    biggest_bar_info = get_biggest_bar(bar_info['features'])
    smallest_bar_info = get_smallest_bar(bar_info['features'])
    biggest_bar_name = biggest_bar_info['properties']['Attributes']['Name']
    smallest_bar_name = smallest_bar_info['properties']['Attributes']['Name']
    print('Самый большой бар Москвы ', biggest_bar_name)
    print('Самый маленький бар Москвы: ', smallest_bar_name)
    try:
        lat, long = get_user_coordinates()
    except ValueError:
        exit('Широта и долгота должны быть числами')
    nearest_bar = get_closest_bar(bar_info['features'], long, lat)
    nearest_bar_name = nearest_bar['properties']['Attributes']['Name']
    nearest_bar_address = nearest_bar['properties']['Attributes']['Address']
    print('Ближайший к Вам бар: ', nearest_bar_name,
          '. Он находится по адресу:', nearest_bar_address)
