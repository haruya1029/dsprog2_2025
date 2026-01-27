import requests
from bs4 import BeautifulSoup
import time
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib

# ==========================================
# 1. データの取得（Webスクレイピング）
# ==========================================
def fetch_and_save_data():
    print("Webサイトからデータを取得中...")
    # 例：統計ダミーサイトや実際の公開ページを想定
    # 実際には requests.get(url) を使用
    time.sleep(1) # サーバ負荷への配慮
    
    # 取得したデータ（路線の混雑率データ）
    raw_data = [
        ('JR山手線', 158),
        ('JR中央線', 182),
        ('東京メトロ東西線', 199),
        ('都営三田線', 156),
        ('東急田園都市線', 184)
    ]
    
    # DB保存
    conn = sqlite3.connect('traffic.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS congestion (line TEXT, rate INTEGER)')
    cursor.execute('DELETE FROM congestion') # データをリセット
    cursor.executemany('INSERT INTO congestion VALUES (?, ?)', raw_data)
    conn.commit()
    conn.close()
    print("データベースへの保存が完了しました。")

# ==========================================
# 2. クラスを用いた分析（動的な出力）
# ==========================================
class TrafficAnalyzer:
    def __init__(self, db_name):
        self.db_name = db_name

    def analyze_limit(self, limit):
        """指定した混雑率を超える路線を抽出"""
        conn = sqlite3.connect(self.db_name)
        # SQLでクエリ発行
        df = pd.read_sql(f"SELECT * FROM congestion WHERE rate > {limit}", conn)
        conn.close()
        return df

# ==========================================
# 3. メイン処理
# ==========================================
if __name__ == "__main__":
    # データ取得
    fetch_and_save_data()
    
    # 分析
    analyzer = TrafficAnalyzer('traffic.db')
    user_limit = 160  # 例えば160%以上の路線を調べたい
    result_df = analyzer.analyze_limit(user_limit)
    
    print(f"\n--- 混雑率が{user_limit}%を超えている路線 ---")
    print(result_df)
    
    # 可視化
    plt.figure(figsize=(10, 6))
    plt.bar(result_df['line'], result_df['rate'], color='orange')
    plt.axhline(y=180, color='red', linestyle='--', label='非常に激しい混雑')
    plt.title(f"Congestion Rate Analysis (Over {user_limit}%)")
    plt.ylabel("Rate (%)")
    plt.legend()
    plt.show()
