import json
import math
import argparse


def load_data(file_path='bars.json'):
    with open(file_path, 'r', encoding='utf-8') as data_file:
        try:
            bar_data = json.load(data_file)
            return bar_data
        except json.decoder.JSONDecodeError:
            return None


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


def get_console_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'latitude',
        type=float,
        help='Введите широту в формате DD.DDD, чтобы узнать название '
             'самого близкого бара.'
    )
    parser.add_argument(
        'longitude',
        type=float,
        help='Введите долготу в формате DD.DDD, чтобы узнать название '
             'самого близкого бара.'
    )
    parser.add_argument(
        '--file',
        default='bars.json',
        help='Если файл с данными называется не "bars.json" и/или файл не лежит'
             ' в папке скрипта, то используйте этот параметр, чтобы указать'
             ' путь к файлу с данными о барах.'
    )
    args = parser.parse_args()
    return args


def print_results(bar_description, bar):
    bar_name = bar['properties']['Attributes']['Name']
    print(bar_description, bar_name)


if __name__ == '__main__':
    console_arguments = get_console_arguments()
    user_file_path = console_arguments.file
    try:
        bar_info = load_data(user_file_path)
    except FileNotFoundError:
        exit('Не удалось найти файл с данными о барах.')
    if not bar_info:
        exit('Указанный файл не содержит данные в формате json.')
    bars = bar_info['features']
    biggest_bar_info = get_biggest_bar(bars)
    smallest_bar_info = get_smallest_bar(bars)
    print_results('Самый большой бар Москвы: ', biggest_bar_info)
    print_results('Самый маленький бар Москвы: ', smallest_bar_info)
    lat = console_arguments.latitude
    long = console_arguments.longitude
    nearest_bar_info = get_closest_bar(bars, long, lat)
    print_results('Ближайший к Вам бар: ', nearest_bar_info)
