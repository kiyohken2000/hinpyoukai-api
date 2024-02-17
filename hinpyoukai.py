import os
from flask import Flask, request
import face_recognition
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from imgurpython import ImgurClient
from flask_cors import CORS
from modules import functions
import uuid

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def main():
  try:
    print('関数の開始')
    
    # 受信したテキストを代入
    request_dict = request.get_json()
    recieved_image_url = str(request_dict['data'])
    recieved_number_position = request_dict['numberPosition']
    recieved_font_size = request_dict['fontSize']
    recieved_is_brackets = request_dict['isBrackets']
    print('受信したURL', recieved_image_url)
    print('受信した数字位置', recieved_number_position)
    print('受信したフォントサイズ', recieved_font_size)
    print('受信したカッコのオンオフ', recieved_is_brackets)

    # ここから画像処理

    # 数字の位置を決める
    if recieved_number_position == 0:
      # 0のときは顔の上
      offset_x = -50
      offset_y = -90
    elif recieved_number_position == 1:
      # 1のときは顔の右
      offset_x = 2
      offset_y = 2
    else:
      # 受信した数字の位置が0または1以外の場合は顔の上
      offset_x = -50
      offset_y = -90

    grid_width = 1
    grid_height = 200

    # URLから画像をダウンロード
    response = requests.get(recieved_image_url)
    image_data = response.content
    print('URLから画像をダウンロード完了')

    # 画像データをface_recognitionで処理する
    load_image = face_recognition.load_image_file(BytesIO(image_data))

    face_locations = face_recognition.face_locations(load_image)

    face_locations = sorted(face_locations, key=lambda x: (x[0] // grid_height, x[1] // grid_width))

    pil_image = Image.fromarray(load_image)
    draw = ImageDraw.Draw(pil_image)

    cnt = 0

    for (top, right, bottom, left) in face_locations:

      # 番号
      cnt = cnt + 1
      numberStrings = f'({cnt})' if recieved_is_brackets else f'{cnt}'

      # フォントサイズ
      font_size = functions.calculate_font_size((top, right, bottom, left), recieved_font_size)
      font = ImageFont.truetype("meiryo.ttc", font_size)

      # 番号を描画する
      draw.text((right + offset_x, top + offset_y), numberStrings, font=font, fill='black', stroke_fill='white', stroke_width=4)

    del draw

    # ユニークなファイル名を生成して保存
    image_filename = str(uuid.uuid4()) + ".jpg"
    pil_image.save(image_filename)
    print('解析完了、解析後の画像を保存した')

    # Imgurのクライアント情報を設定
    client_id = '7c34970b70aef09'
    client_secret = 'b8d5bee0d6e73c7b7a5145c8fd98342a378bffb2'

    # Imgurのクライアントを作成
    client = ImgurClient(client_id, client_secret)

    # アップロードする画像ファイルのパス
    image_path = image_filename

    # 画像をImgurにアップロード
    uploaded_image = client.upload_from_path(image_path, anon=True)

    # アップロードされた画像のURLを取得
    image_url = uploaded_image['link']
    print('アップロードした画像のURL', image_url)

    # アップロードした画像の削除
    os.remove(image_path)

    # 結果の出力
    return image_url

  except Exception as e:
    print('error', e)
    return f'Error: {e}'
  
if __name__ == "__main__":
  app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))