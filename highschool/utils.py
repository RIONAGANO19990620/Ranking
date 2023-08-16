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
            model = HighSchool(name=name, value=item)
            model.save()


if __name__ == '__main__':
    path = '/Users/naganorio/Desktop/Ranking/Data/high_school.json'
    create_model_from_json(path)
