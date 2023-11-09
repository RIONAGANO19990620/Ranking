import json

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ranking.settings')

from django import setup

setup()
from highschool.models import HighSchool


def create_model_from_json(path: str):
    with open(path) as f:
        data = json.load(f)
    for item in data:
        name_list = data[item]
        for name in name_list:
            model, created = HighSchool.objects.get_or_create(name=name, value=item)
            if not created:
                model.value = item
                model.save()


if __name__ == '__main__':
    path = '/Users/taguchinaoki/Ranking/Data/high_school2.json'
    create_model_from_json(path)
