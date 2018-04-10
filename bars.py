import json
import os
import math


def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        bar_data = json.load(f)
    return bar_data


def get_bar_attributes(bar_data):
    for bar in bar_data:
        try:
            attributes = bar['properties']['Attributes']
        except KeyError:
            print('В файле с данными нет атрибутов "properties" '
                  'и/или "Attributes"')
            attributes = None
        yield attributes


def get_seats_count(list_of_bar_attributes):
    seats_count_dictionary = {}
    for bar_attributes in get_bar_attributes(list_of_bar_attributes):
        try:
            bar_seats_count = bar_attributes.pop('SeatsCount')
        except KeyError:
            print('В файле с данными нет атрибута "SeatsCount"')
            bar_seats_count = None
        seats_count_dictionary.update({bar_seats_count: bar_attributes})
    return seats_count_dictionary


def get_biggest_bar(seats_based_dict):
    seats_count_list = seats_based_dict.keys()
    biggest_seats_number = max(seats_count_list)
    try:
        biggest_bar_name = seats_based_dict[biggest_seats_number]['Name']
    except KeyError:
        print('В файле с данными нет атрибута "Name"')
        biggest_bar_name = None
    print('Самый большой бар Москвы: ', biggest_bar_name)


def get_smallest_bar(seats_based_dict):
    seats_count_list = seats_based_dict.keys()
    smallest_seats_number = min(seats_count_list)
    try:
        smallest_bar_name = seats_based_dict[smallest_seats_number]['Name']
    except KeyError:
        print('В файле с данными нет атрибута "Name"')
        smallest_bar_name = None
    print('Самый маленький бар Москвы: ', smallest_bar_name)


def get_bar_address(bar_features):
    try:
        bar_address = bar_features['properties']['Attributes']['Address']
    except KeyError:
        bar_address = None
    return bar_address


def get_closest_bar(bar_data, longitude, latitude):
    first_loop = True
    closest_bar = None
    closest_bar_address = None
    minimal_distance = 0
    for bar in bar_data:
        try:
            coordinates = bar['geometry']['coordinates']
        except KeyError:
            continue
        distance = math.hypot(coordinates[0] - longitude,
                              coordinates[1] - latitude)
        if first_loop:
            minimal_distance = distance
            closest_bar = bar['properties']['Attributes']['Name']
            closest_bar_address = get_bar_address(bar)
            first_loop = False
        if distance < minimal_distance:
            minimal_distance = distance
            closest_bar = bar['properties']['Attributes']['Name']
            closest_bar_address = get_bar_address(bar)
    print('Ближайший к Вам бар: ', closest_bar,
          '. Он находится по адресу:', closest_bar_address)


if __name__ == '__main__':
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(absolute_path, 'bars.json')
    bar_info = load_data(json_path)
    bar_list = bar_info['features']
    seats_dictionary = get_seats_count(bar_list)
    get_biggest_bar(seats_dictionary)
    get_smallest_bar(seats_dictionary)
    try:
        lat = float(input('Чтобы узнать название самого близкого бара, '
                          'введите свои gps координаты в формате '
                          'DD.DDD.\nШирота: '))
        long = float(input('Долгота: '))
    except ValueError:
        print('Широта и долгота должны быть числами')
        raise
    get_closest_bar(bar_list, long, lat)
