import numpy as np
import pandas as pd
from tqdm import tqdm

tqdm.pandas()

import requests
from bs4 import BeautifulSoup

df = pd.DataFrame()  # 空のDataFrameを作成

# すべてのページにアクセスし情報を取得
for pageno in tqdm(range(1, 504)):
    url = 'https://www.minkou.jp/hischool/ranking/deviation/page=' + str(pageno) + '/'
    html = requests.get(url)

    # パース用オブジェクト作成
    soup = BeautifulSoup(html.text, "html.parser")

    # 偏差値を含む要素の抽出
    devi = soup.find_all("dd", class_="info-main")

    # 学校名を含む要素の抽出
    hsname = soup.find_all("div", class_="mod-listRanking-name")

    # 必要箇所の抽出
    devi_list = [int(d.text) for d in devi]
    hsname_list = [h.contents[1].text for h in hsname]

    # DataFrame化して結合
    df = pd.concat([df, pd.DataFrame({'hsname': hsname_list, 'devi': devi_list})])

# 以下でrankingに含む高校さんを剪定
df_ranking = df[df["devi"] > 60]

df.to_csv('highschool_all.csv')
df_ranking.to_csv('highschool2.csv')
