import json

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ranking.settings')

from django import setup

setup()

from city_bus.models import Sale, CityBus, Course


def create_model_from_json(path: str):
    with open(path) as f:
        data = json.load(f)

    for sale_value, citybus in data.items():
        sale, _ = Sale.objects.get_or_create(sale=sale_value)

        for system_number, course_name in citybus.items():
            course, _ = Course.objects.get_or_create(name=course_name)
            CityBus.objects.get_or_create(sale=sale, number=system_number, course=course)


if __name__ == '__main__':
    path = '/Users/taguchinaoki/Ranking/Data/CityBus.json'
    create_model_from_json(path)
