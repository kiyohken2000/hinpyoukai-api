import requests
import json

ENDPOINT = "https://hinpyoukai-api-omc3n2et7a-an.a.run.app"

payload = {
    "data": "https://i.imgur.com/UmM20hL.png",
    "numberPosition": 0,
    "fontSize": 0.5,
    "isBrackets": True,
}

headers = {
    "Content-Type": "application/json",
}

print(f"エンドポイント: {ENDPOINT}")
print(f"リクエストボディ: {json.dumps(payload, ensure_ascii=False)}")
print("リクエスト送信中...")

try:
    response = requests.post(ENDPOINT, json=payload, headers=headers, timeout=120)
    print(f"\nステータスコード: {response.status_code}")
    print(f"レスポンス: {response.text}")

    if response.status_code == 200 and response.text.startswith("https://"):
        print("\n[OK] エンドポイント正常稼働")
    else:
        print("\n[NG] 異常レスポンス")

except requests.exceptions.Timeout:
    print("\n[NG] タイムアウト（120秒）")
except requests.exceptions.ConnectionError as e:
    print(f"\n[NG] 接続エラー: {e}")
except Exception as e:
    print(f"\n[NG] 予期しないエラー: {e}")
