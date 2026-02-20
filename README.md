# hinpyoukai-api

画像URLを受け取り、顔認識で検出した顔に番号を付けた画像を返す Web API。

## エンドポイント

```
POST https://hinpyoukai-api-omc3n2et7a-an.a.run.app
```

## リクエスト

**Headers**

```
Content-Type: application/json
```

**Body**

| パラメータ | 型 | 説明 |
|---|---|---|
| `data` | string | 処理対象の画像URL |
| `numberPosition` | number | 番号の描画位置（`0`: 顔の上, `1`: 顔の右） |
| `fontSize` | number | フォントサイズ係数（`0.8`: 大, `0.5`: 中, `0.3`: 小） |
| `isBrackets` | boolean | `true`: カッコ付き `(1)`、`false`: カッコなし `1` |

**例**

```json
{
  "data": "https://i.imgur.com/UmM20hL.png",
  "numberPosition": 0,
  "fontSize": 0.5,
  "isBrackets": true
}
```

## レスポンス

処理済み画像の Imgur URL を文字列で返す。

```
https://i.imgur.com/xxxxxxx.jpeg
```

## 処理フロー

1. 画像URLからダウンロード
2. `face_recognition` で顔を検出・ソート（上から順に番号付け）
3. 各顔に番号を描画（Meiryo フォント使用）
4. Imgur にアップロードしてURLを返却

## ローカル実行

```bash
pip install -r requirements.txt
python hinpyoukai.py
```

## テスト

```bash
# ローカルテスト（Imgur へのアップロードまで実行）
python -c "import test; test.hinpyoukai()"

# エンドポイントの疎通確認
python health_check.py
```

## デプロイ (GCP Cloud Run)

```bash
# Docker イメージをビルドして Container Registry にプッシュ
gcloud builds submit --tag asia-northeast1-docker.pkg.dev/hey-abe/mygpt-repo/hinpyoukai-api --project hey-abe
```

コマンド実行後、Cloud Run コンソールから新しいリビジョンのデプロイを行う。

## 構成

```
hinpyoukai-api/
├── hinpyoukai.py       # Flask アプリ本体
├── modules/
│   └── functions.py    # フォントサイズ計算ユーティリティ
├── test.py             # ローカルテスト用スクリプト
├── health_check.py     # エンドポイント疎通確認スクリプト
├── Dockerfile          # Cloud Run 用コンテナ定義
└── requirements.txt    # 依存パッケージ
```
