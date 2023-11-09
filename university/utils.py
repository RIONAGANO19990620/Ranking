import json

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ranking.settings')

from django import setup

setup()
from university.models import University


def create_model_from_json(path: str):
    with open(path) as f:
        data = json.load(f)
    for item in data:
        name_list = data[item]
        for name in name_list:
            model = University(name=name, value=item)
            model.save()


if __name__ == '__main__':
    path = '/Users/taguchinaoki/Ranking/Data/university.json'
    create_model_from_json(path)
