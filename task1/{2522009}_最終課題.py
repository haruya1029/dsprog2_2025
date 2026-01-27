import pandas as pd
import matplotlib.pyplot as plt

# 日本語文字化け解消のためのライブラリ
try:
    import japanize_matplotlib
except ImportError:
    # ライブラリがない場合は自動インストール
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "japanize-matplotlib"])
    import japanize_matplotlib

class EstateAnalyzer:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        print("CSVの読み込みに成功しました！")

    def calculate_metrics(self):
        # 建物面積(m2)を用いて平米単価を算出
        self.df['平米単価(万円)'] = self.df['販売価格(万円)'] / self.df['建物面積(m2)']
        return self.df

    def compare_by_walk_time(self, limit=10):
        self.calculate_metrics()
        near_station = self.df[self.df['徒歩(分)'] <= limit]
        far_station = self.df[self.df['徒歩(分)'] > limit]
        
        res = {
            f"{limit}分以内": near_station['平米単価(万円)'].mean(),
            f"{limit}分超え": far_station['平米単価(万円)'].mean()
        }
        return res

    def plot_comparison(self, limit=10):
        result = self.compare_by_walk_time(limit)
        
        # グラフのスタイル設定
        plt.figure(figsize=(8, 5))
        colors = ['#87CEEB', '#F08080'] # さわやかなスカイブルーとサーモンピンク
        bars = plt.bar(result.keys(), result.values(), color=colors, edgecolor='black', linewidth=0.5)
        
        # ラベルとタイトルの設定
        plt.ylabel('平米単価（万円/㎡）', fontsize=12)
        plt.title(f'駅徒歩{limit}分以内・超えの平米単価比較', fontsize=14, fontweight='bold')
        
        # 棒の上に数値を表示
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                     f'{height:.2f}', ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        # 見栄えの調整
        plt.ylim(0, max(result.values()) * 1.2)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        # 保存（スライド貼付用）
        # plt.savefig('comparison_result.png', dpi=300)
        plt.show()

# --- 実行部分 ---
# ファイルパスはご自身の環境に合わせて適宜変更してください
csv_path = '/Users/kuboharu/dsprog2_2025/dsprog2_2025/task1/estate_data.csv'

if __name__ == "__main__":
    try:
        analyzer = EstateAnalyzer(csv_path)
        result = analyzer.compare_by_walk_time(10)
        
        print("\n" + "="*30)
        print("【分析結果：平米単価の比較】")
        for key, value in result.items():
            print(f"{key}: {value:.2f} 万円/㎡")
        print("="*30)

        analyzer.plot_comparison(10)

    except FileNotFoundError:
        print(f"エラー：指定されたパスにCSVファイルが見つかりません。\nパス：{csv_path}")