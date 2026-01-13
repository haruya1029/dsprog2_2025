import streamlit as st
import requests
import sqlite3
from datetime import datetime


# DB 初期化

conn = sqlite3.connect("weather.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS areas (
    area_code TEXT PRIMARY KEY,
    area_name TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS forecasts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    area_code TEXT,
    date TEXT,
    weather TEXT
)
""")

conn.commit()


# タイトル

st.title("☀️ 気象庁 天気予報アプリ（DB対応）")


# エリア情報取得 & DB保存

AREA_URL = "https://www.jma.go.jp/bosai/common/const/area.json"
area_data = requests.get(AREA_URL).json()
offices = area_data["offices"]

for code, info in offices.items():
    cur.execute(
        "INSERT OR IGNORE INTO areas VALUES (?, ?)",
        (code, info["name"])
    )
conn.commit()


# 地域選択

areas = cur.execute("SELECT area_name, area_code FROM areas").fetchall()
area_dict = {name: code for name, code in areas}

selected_area = st.selectbox("地域を選択してください", area_dict.keys())
area_code = area_dict[selected_area]


# 天気予報取得 & DB保存

if st.button("天気予報を取得・保存"):
    FORECAST_URL = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"
    forecast_data = requests.get(FORECAST_URL).json()

    time_series = forecast_data[0]["timeSeries"][0]
    dates = time_series["timeDefines"]
    weathers = time_series["areas"][0]["weathers"]

    for d, w in zip(dates, weathers):
        date = d[:10]
        cur.execute("""
            INSERT INTO forecasts (area_code, date, weather)
            VALUES (?, ?, ?)
        """, (area_code, date, w))

    conn.commit()
    st.success("DBに保存しました")


# 天気予報表示（DBから）

st.subheader(f"📍 {selected_area} の天気予報（DB）")

rows = cur.execute("""
    SELECT date, weather
    FROM forecasts
    WHERE area_code = ?
    ORDER BY date
""", (area_code,)).fetchall()

if rows:
    for date, weather in rows:
        st.write(f"**{date}**：{weather}")
else:
    st.info("まだ天気予報が保存されていません")