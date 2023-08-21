import json
import unittest
from pathlib import Path


class TestDataGetter(unittest.TestCase):

    def setUp(self) -> None:
        self.hensachi = 65
        self.path = '/Users/taguchinaoki/Ranking/Data/corporation.json'

    def test_data_getter(self):
        with open(self.path) as f:
            data = json.load(f)
        print(data[str(self.hensachi)])
