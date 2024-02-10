import face_recognition
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from imgurpython import ImgurClient
import os

def hinpyoukai():
  font = ImageFont.truetype("meiryo.ttc", 32)
  offset_x = -50
  offset_y = -70

  grid_width = 1
  grid_height = 200

  # URLから画像をダウンロード
  url = "https://i.imgur.com/Ya8yuBf.jpg"
  response = requests.get(url)
  image_data = response.content

  # 画像データをface_recognitionで処理する
  load_image = face_recognition.load_image_file(BytesIO(image_data))

  face_locations = face_recognition.face_locations(load_image)

  face_locations = sorted(face_locations, key=lambda x: (x[0] // grid_height, x[1] // grid_width))

  pil_image = Image.fromarray(load_image)
  draw = ImageDraw.Draw(pil_image)

  cnt = 0

  for (top, right, bottom, left) in face_locations:
    cnt = cnt + 1
    draw.text((right + offset_x, top + offset_y), f'({cnt})', font=font, fill='black', stroke_fill='white', stroke_width=4)

  del draw

  pil_image.save("output_image.jpg")

  # Imgurのクライアント情報を設定
  client_id = '7c34970b70aef09'
  client_secret = 'b8d5bee0d6e73c7b7a5145c8fd98342a378bffb2'

  # Imgurのクライアントを作成
  client = ImgurClient(client_id, client_secret)

  # アップロードする画像ファイルのパス
  image_path = "output_image.jpg"

  # 画像をImgurにアップロード
  uploaded_image = client.upload_from_path(image_path, anon=True)

  # アップロードされた画像のURLを取得
  image_url = uploaded_image['link']

  # アップロードした画像の削除
  os.remove(image_path)

  print("Uploaded Image URL:", image_url)