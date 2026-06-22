import streamlit as st
import requests
import json

from datetime import date
from dateutil.relativedelta import relativedelta

# 関数
## サーバー側の読み込み
def get_user_id(family_name, first_name):
    #ファイルの読み込み、パスは作業ディレクトリの相対パス
    with open("C:\\Users\\koyama\\OneDrive\\Desktop\\st_app\\assets\\known_poeple.json", "r",
              encoding="utf-8") as f:
        people = json.load(f)
    matched = filter(
        lambda d: d["first_name"] == first_name and
        d["family_name"] == family_name, people
    )
    matched = list(matched)
    if len (matched) > 0:
        return matched[0]["id"]
    else:
        return None
    #照合結果idを返す
    
## Web リソース

### 名前から年齢の予測
@st.cache_data
def agify(first_name):
    url = f"https://api.agify.io/"
    params = {"name": first_name}
    response = requests.get(url, params=params)
    result = json.loads(response.content)
    #resultの例 :　{"count":1, "name": "John", "age": 30}
    
    age = result["age"]
    return age

### 名前から性別の予測
@st.cache_data
def genderize(first_name):
    url = f"https://api.genderize.io/"
    params = {"name": first_name}
    response = requests.get(url, params=params)
    result = json.loads(response.content)
    #resultの例 :　{"count":1, "name": "John", "gender": "male", "probability": 0.93}
    
    gender = result["gender"]
    probability = result["probability"]
    return gender, probability

### 名前から国籍の予測
@st.cache_data
def nationalize(first_name):
    url = f"https://api.nationalize.io/"
    params = {"name": first_name}
    response = requests.get(url, params=params)
    result = json.loads(response.content)
    #resultの例 :　{"count":1, "name": "John", "country": [{"country_id": "US", "probability": 0.429728}]}
    
    country = result["country"][0]["country_id"]
    probability = result["country"][0]["probability"]
    return country, probability

# 以下、表示
st.markdown("# プロファイル予測アプリ")
## ユーザー入力の受け取り
### 名前の入力
family_name = st.text_input("姓を入力してください。")
first_name = st.text_input("名を入力してください。")


## ユーザーへの情報表示
if st.button("入力完了"):
    ### ユーザーIDの確認
    user_id = get_user_id(family_name, first_name)
    user_id_text = f"ユーザーID: {user_id}" if user_id else "ゲスト"
    ### フルネームの計算
    full_name = family_name + first_name
    ### 予測結果の取得
    age = agify(first_name)
    gender = genderize(first_name)
    country = nationalize(first_name)
    ### 結果の表示
    st.text(f"{full_name}({user_id_text})さんの予測結果")
    st.table(
        {
            "年齢": age,
            "性別": gender,
            "国籍": country
        }
    )
