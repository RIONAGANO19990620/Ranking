import json
from pathlib import Path

import pandas as pd
from numpy import nan


class DataManager:
    start_num = 80
    end_num = 55

    @classmethod
    def corporation_manager(cls, input_path: Path, output_path: Path):
        output_dict = {}
        output_dict['81'] = ['Point72', 'CapitalGroup']
        f = open(input_path, 'r', encoding='UTF-8')
        data = f.read()
        data = data.replace('\n', '')
        num = cls.start_num
        while num > cls.end_num:
            st = data.find(str(int(num)))
            end = data.find(str(int(num - 1)))
            target = data[st+3: end-1].split()
            output_dict[str(int(num))] = target
            data = data[end:]
            num -= 1
        with open(output_path, mode="wt", encoding="utf-8") as f:
            json.dump(output_dict, f, ensure_ascii=False, indent=2)

    @classmethod
    def high_school_manager(cls, input_path: Path, output_path: Path):
        output_dict = {}
        data = pd.read_csv(input_path, encoding="utf-8")
        data = data.fillna('')
        for index, row in data.iterrows():
            name = row['関東']
            if name == '':
                name = row['近畿']
            if name == '':
                name = row['その他']
            try:
                output_dict[int(float(row['偏差値']))].append(name)
            except:
                try:
                    output_dict[int(float(row['偏差値']))] = [name]
                except:
                    pass
        with open(output_path, mode="wt", encoding="utf-8") as f:
            json.dump(output_dict, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    input_path = Path('/Users/naganorio/Desktop/Ranking/Data/highschool.csv')
    output_path = Path('/Users/naganorio/Desktop/Ranking/Data/high_school.json')
    DataManager.high_school_manager(input_path, output_path)
