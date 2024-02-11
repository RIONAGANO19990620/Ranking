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
            target = data[st + 3: end - 1].split()
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
            name = row['hsname'].replace("高等学校", "")
            try:
                output_dict[int(float(row['devi']))].append(name)
            except:
                try:
                    output_dict[int(float(row['devi']))] = [name]
                except:
                    pass
        with open(output_path, mode="wt", encoding="utf-8") as f:
            json.dump(output_dict, f, ensure_ascii=False, indent=2)

    @classmethod
    def university_manager(cls, input_path: Path, output_path: Path):
        first_dict = {}
        data = pd.read_csv(input_path, encoding="utf-8")

        for i in range(len(data)):
            for j in range(len(data.columns) - 1):
                if data.iloc[(i, 0)] not in first_dict:
                    first_dict[data.iloc[(i, 0)]] = [data.iloc[(i, 1)]]
                else:
                    first_dict[data.iloc[(i, 0)]].append(data.iloc[(i, j + 1)])

        output_dict = {key: [value for value in values if not pd.isna(value)] for key, values in first_dict.items()}

        output = []
        for rank, names in output_dict.items():
            for name in names:
                output.append({
                    "model": "university.university",
                    "fields": {
                        "name": name,
                        "rank": rank
                    }
                })

        with open(output_path, mode="wt", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

    @classmethod
    def number_plate_manager(cls, input_path: Path, output_path: Path):
        output_dict = {}
        data = pd.read_csv(input_path, encoding='utf-8')
        for index, row in data.iterrows():
            name = row['number']
            try:
                output_dict[int(float(row['devi']))].append(name)
            except:
                try:
                    output_dict[int(float(row['devi']))] = [name]
                except:
                    pass
        with open(output_path, mode="wt", encoding="utf-8") as f:
            json.dump(output_dict, f, ensure_ascii=False, indent=2)

    @classmethod
    def city_bus_manager(cls, input_path: Path, output_path: Path):
        output_dict = {}
        data = pd.read_csv(input_path, encoding='utf-8')
        for index, row in data.iterrows():
            name = row['number']
            course = row['course']
            try:
                # スコアを整数に変換し、既存のキーのリストに新しい{番号: コース}の辞書を追加
                if int(float(row['score'])) in output_dict:
                    output_dict[int(float(row['score']))].update({name: course})
                else:
                    # 存在しないキーの場合は新しいキーと値を追加
                    output_dict[int(float(row['score']))] = {name: course}
            except ValueError:
                # スコアが不正な値の場合は無視
                pass
        with open(output_path, mode="wt", encoding="utf-8") as f:
            json.dump(output_dict, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    input_path = Path('/Users/taguchinaoki/Ranking/Data/highschool2.csv')
    output_path = Path('/Users/taguchinaoki/Ranking/Data/high_school2.json')
    DataManager.high_school_manager(input_path, output_path)

    input_path = Path('/Users/taguchinaoki/Ranking/Data/university.csv')
    output_path = Path('/Users/taguchinaoki/Ranking/Data/university.json')
    DataManager.university_manager(input_path, output_path)

    input_path = Path('/Users/taguchinaoki/Ranking/Data/NumberPlate.csv')
    output_path = Path('/Users/taguchinaoki/Ranking/Data/NumberPlate.json')
    DataManager.number_plate_manager(input_path, output_path)

    input_path = Path('/Users/taguchinaoki/Ranking/Data/CityBus.csv')
    output_path = Path('/Users/taguchinaoki/Ranking/Data/CityBus.json')
    DataManager.city_bus_manager(input_path, output_path)
