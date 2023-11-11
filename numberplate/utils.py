import json

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ranking.settings')

from django import setup

setup()
from numberplate.models import NumberPlate


def create_model_from_json(path: str):
    with open(path) as f:
        data = json.load(f)

    for score, names in data.items():
        for name in names:
            NumberPlate.objects.create(name=name, value=int(score))


if __name__ == '__main__':
    path = '/Users/taguchinaoki/Ranking/Data/NumberPlate.json'
    create_model_from_json(path)
