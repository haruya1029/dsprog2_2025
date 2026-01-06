import streamlit as st
import requests


# タイトル

st.title("気象庁 天気予報アプリ")


# 地域リスト取得

AREA_URL = "http://www.jma.go.jp/bosai/common/const/area.json"
area_data = requests.get(AREA_URL).json()

# 都道府県レベル（offices）を使用
areas = area_data["offices"]

# 表示用データ作成
area_names = {v["name"]: k for k, v in areas.items()}

# 地域選択

selected_area_name = st.selectbox(
    "地域を選択してください",
    area_names.keys()
)

area_code = area_names[selected_area_name]


# 天気予報取得

FORECAST_URL = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"
forecast_data = requests.get(FORECAST_URL).json()


# 天気予報表示

st.subheader(f" {selected_area_name} の天気予報")

time_series = forecast_data[0]["timeSeries"][0]
dates = time_series["timeDefines"]
weathers = time_series["areas"][0]["weathers"]

for date, weather in zip(dates, weathers):
    st.write(f"**{date[:10]}**：{weather}")