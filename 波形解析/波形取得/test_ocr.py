import easyocr
from PIL import Image
import numpy as np

print('=== EasyOCR テスト ===')
print('モデル読み込み中...')
reader = easyocr.Reader(['en'], gpu=False)

# 画像全体からテキスト検出
print('画像全体のOCR実行中...')
results = reader.readtext('screen_20260320_183001.png')

print(f'\n検出テキスト数: {len(results)}')
print('--- 検出結果 ---')
for bbox, text, conf in sorted(results, key=lambda x: x[2], reverse=True):
	if conf > 0.1:
		y_center = (bbox[0][1] + bbox[2][1]) / 2
		x_center = (bbox[0][0] + bbox[2][0]) / 2
		print(f'  [{conf:.2f}] ({int(x_center):4d},{int(y_center):3d}) "{text}"')

# 特定領域（上部のチャンネル情報）を切り出してOCR
print('\n=== 上部領域（チャンネル情報）のOCR ===')
img = Image.open('screen_20260320_183001.png')
top_region = img.crop((0, 0, 1280, 120))
top_arr = np.array(top_region)
results_top = reader.readtext(top_arr)
for bbox, text, conf in sorted(results_top, key=lambda x: x[2], reverse=True):
	if conf > 0.1:
		print(f'  [{conf:.2f}] "{text}"')

# 下部領域（時間軸情報）
print('\n=== 下部領域（時間軸情報）のOCR ===')
bottom_region = img.crop((0, 700, 1280, 800))
bottom_arr = np.array(bottom_region)
results_bottom = reader.readtext(bottom_arr)
for bbox, text, conf in sorted(results_bottom, key=lambda x: x[2], reverse=True):
	if conf > 0.1:
		print(f'  [{conf:.2f}] "{text}"')

# 左側領域（電圧スケール）
print('\n=== 左側領域（電圧スケール）のOCR ===')
left_region = img.crop((0, 100, 80, 700))
left_arr = np.array(left_region)
results_left = reader.readtext(left_arr)
for bbox, text, conf in sorted(results_left, key=lambda x: x[2], reverse=True):
	if conf > 0.1:
		print(f'  [{conf:.2f}] "{text}"')
