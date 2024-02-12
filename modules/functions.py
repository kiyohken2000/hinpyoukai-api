def calculate_font_size(face_location, ratio):
  # 顔の幅と高さを計算します
  face_width = face_location[1] - face_location[3]
  face_height = face_location[2] - face_location[0]
  
  # フォントサイズを顔の大きさに基づいて計算します
  font_size = min(face_width, face_height) * ratio  # 任意の係数を掛けることで調整できます
  
  return max(font_size, 12)  # 最小フォントサイズを12とします