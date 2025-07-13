import requests
from bs4 import BeautifulSoup
import json
import sys
import base64
import re

def _get_session_details(race_url):
    """
    Fetches a race detail page and attempts to extract session information.

    *** IMPORTANT: THIS IS A TEMPORARY IMPLEMENTATION. ***
    The exact HTML structure of the F1 race detail pages could not be fully
    inspected due to API quota limits. This function uses a heuristic approach
    to extract session data. It will need to be refined and made more robust
    once the full HTML content can be analyzed.
    ********************************************************
    """
    sessions = {
        "practice1": "TBD",
        "practice2": "TBD",
        "practice3": "TBD",
        "qualifying": "TBD",
        "race": "TBD"
    }
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        }
        response = requests.get(race_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Refined regex to capture date and time more precisely
        # It looks for a date (e.g., "04Jul"), then optionally "Chequered Flag",
        # then the session name, then the time (e.g., "11:30-12:30" or "11:30").
        # The regex is made more flexible to handle variations in spacing and optional text.
        session_pattern = re.compile(
            r"(\d{2}[A-Za-z]{3})\s*(?:Chequered Flag)?\s*(Practice [1-3]|Qualifying|Race)\s*(\d{2}:\d{2}(?:-\d{2}:\d{2})?)"
        )

        # Search for elements that are likely to contain session information.
        # Based on previous outputs, session details often appear within <p>, <span>, or <div> tags.
        # We'll iterate through all such tags and apply the regex.
        for tag in soup.find_all(['p', 'span', 'div', 'li']):
            text = tag.get_text(strip=True)
            match = session_pattern.search(text)
            if match:
                date_str = match.group(1)
                session_name_raw = match.group(2)
                time_str = match.group(3)

                full_session_info = f"{date_str} {time_str}"

                if "Practice 1" in session_name_raw:
                    sessions["practice1"] = full_session_info
                elif "Practice 2" in session_name_raw:
                    sessions["practice2"] = full_session_info
                elif "Practice 3" in session_name_raw:
                    sessions["practice3"] = full_session_info
                elif "Qualifying" in session_name_raw:
                    sessions["qualifying"] = full_session_info
                elif "Race" in session_name_raw:
                    sessions["race"] = full_session_info

    except requests.exceptions.RequestException as e:
        print(f"WARNING: Could not fetch session details for {race_url}: {e}", file=sys.stderr)
    except Exception as e:
        print(f"WARNING: An error occurred while parsing session details for {race_url}: {e}", file=sys.stderr)
    return sessions

def scrape_f1_calendar():
    """
    F1公式サイトから年間のレースカレンダーと各レースの詳細なセッション情報を取得する。
    成功した場合はJSON形式で標準出力に情報を出力し、
    失敗した場合はエラーメッセージを標準エラー出力に出力して終了する。
    """
    try:
        base_url = "https://www.formula1.com"
        calendar_url = f"{base_url}/en/racing/2025"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        }

        # 年間カレンダーページから各レースへのリンクを取得
        response = requests.get(calendar_url, headers=headers)
        response.raise_for_status()  # HTTPエラーがあれば例外を発生させる
        soup = BeautifulSoup(response.content, 'html.parser')

        all_races_data = []

        # data-f1rd-a7s-click="event_tile_click"属性を持つ<a>タグをすべて見つける
        race_links = soup.find_all('a', attrs={'data-f1rd-a7s-click': 'event_tile_click'})

        for link in race_links:
            race_path = link.get('href')
            if not race_path or "pre-season-testing" in race_path: # プレシーズンテストは除外
                continue

            race_full_url = f"{base_url}{race_path}"

            context_json_str_encoded = link.get('data-f1rd-a7s-context')
            race_name_from_context = "Unknown Race"
            if context_json_str_encoded:
                try:
                    # Base64デコード
                    decoded_bytes = base64.b64decode(context_json_str_encoded)
                    context_json_str = decoded_bytes.decode('utf-8')
                    context_data = json.loads(context_json_str)
                    race_name_from_context = context_data.get('raceName', 'Unknown Race')
                except (json.JSONDecodeError, base64.binascii.Error):
                    pass # JSONパースエラーまたはBase64デコードエラーはスキップ

            # 各レースの詳細ページをスクレイピングしてセッション情報を取得
            sessions = _get_session_details(race_full_url)

            race_data = {
                "raceName": race_name_from_context,
                "url": race_full_url,
                "sessions": sessions
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
