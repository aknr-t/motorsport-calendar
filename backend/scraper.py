import requests
from bs4 import BeautifulSoup
import json
import sys

def scrape_f1_calendar():
    """
    F1公式サイトから年間のレースカレンダーと各レースの詳細なセッション情報を取得する。
    成功した場合はJSON形式で標準出力に情報を出力し、
    失敗した場合はエラーメッセージを標準エラー出力に出力して終了する。
    """
    try:
        # 年間カレンダーページのURL
        base_url = "https://www.formula1.com"
        calendar_url = f"{base_url}/en/racing/2025"

        # 年間カレンダーページから各レースへのリンクを取得
        response = requests.get(calendar_url)
        response.raise_for_status()  # HTTPエラーがあれば例外を発生させる
        soup = BeautifulSoup(response.content, 'html.parser')

        # (ここにカレンダーから各レースのリンクを抽出するロジックを実装する)
        # 現時点では、調査済みのレース名をリストとして使用する
        race_names = ["Australia", "China", "Japan", "Bahrain", "Saudi-Arabia", "Miami", "Emilia-Romagna", "Monaco", "Spain", "Canada", "Austria", "Great-Britain", "Belgium", "Hungary", "Netherlands", "Italy", "Azerbaijan", "Singapore", "United-States", "Mexico", "Brazil", "Las-Vegas", "Qatar", "Abu-Dhabi"]

        all_races_data = []

        for race_name in race_names:
            race_url = f"{base_url}/en/racing/2025/{race_name}"
            
            # 各レースの詳細ページをスクレイピング
            race_response = requests.get(race_url)
            race_response.raise_for_status()
            race_soup = BeautifulSoup(race_response.content, 'html.parser')

            # (ここに各レースページからセッション情報を抽出するロジックを実装する)
            # 現時点ではダミーデータを使用
            race_data = {
                "raceName": race_name.replace('-', ' ').title(),
                "url": race_url,
                "sessions": {
                    "practice1": "TBD",
                    "practice2": "TBD",
                    "practice3": "TBD",
                    "qualifying": "TBD",
                    "race": "TBD"
                }
            }
            all_races_data.append(race_data)

        # 成功した場合は、結果をJSONとして標準出力に出力
        print(json.dumps(all_races_data, indent=2))

    except requests.exceptions.RequestException as e:
        # ネットワーク関連のエラー
        print(f"ERROR: F1 scraping failed due to a network error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        # その他の予期せぬエラー
        print(f"ERROR: An unexpected error occurred during F1 scraping: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    scrape_f1_calendar()
