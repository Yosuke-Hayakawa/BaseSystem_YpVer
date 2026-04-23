import cv2
import numpy as np
from PIL import Image

# OpenCVは日本語パスに対応していないのでnumpyバッファ経由で読む
img_pil = Image.open(r'C:\Users\CARAMAS4\Desktop\919D_CRAMAS自動結果解析\波形取得\screen_20260320_183001.png').convert('RGB')
img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
print(f'OpenCV 画像形状: {img.shape}')

# グレースケール変換
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Canny エッジ検出
edges = cv2.Canny(gray, 50, 150)
print(f'エッジピクセル数: {np.count_nonzero(edges)}')

# HSVに変換して黄色チャンネル波形を抽出
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# 黄色の範囲 (CH1想定)
yellow_lower = np.array([20, 100, 100])
yellow_upper = np.array([40, 255, 255])
yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
yellow_pixels = np.count_nonzero(yellow_mask)
print(f'黄色(CH1)マスク: {yellow_pixels} px')

# シアンの範囲 (CH2想定)
cyan_lower = np.array([80, 100, 100])
cyan_upper = np.array([100, 255, 255])
cyan_mask = cv2.inRange(hsv, cyan_lower, cyan_upper)
cyan_pixels = np.count_nonzero(cyan_mask)
print(f'シアン(CH2)マスク: {cyan_pixels} px')

# 黄色チャンネルの波形Y座標を列ごとに抽出
print('\n=== 黄色波形の数値化テスト ===')
# 波形エリアを推定（大体 x:50-1250, y:80-700 あたり）
wave_area = yellow_mask[80:700, 50:1250]
y_coords = []
for col in range(wave_area.shape[1]):
	col_data = wave_area[:, col]
	rows = np.where(col_data > 0)[0]
	if len(rows) > 0:
		y_coords.append((col + 50, rows.mean() + 80))

print(f'黄色波形データ点数: {len(y_coords)}')
if y_coords:
	xs = [p[0] for p in y_coords]
	ys = [p[1] for p in y_coords]
	print(f'X範囲: {min(xs)}-{max(xs)}')
	print(f'Y範囲: {min(ys):.1f}-{max(ys):.1f}')
	# 先頭10点のサンプル
	print('先頭10点:')
	for x, y in y_coords[:10]:
		print(f'  x={x}, y={y:.1f}')

# OCR精度向上用の前処理: 白テキスト部分を強調
print('\n=== OCR前処理テスト ===')
# 白い領域をマスク (テキスト部分)
white_lower = np.array([0, 0, 180])
white_upper = np.array([180, 50, 255])
white_mask = cv2.inRange(hsv, white_lower, white_upper)
white_enhanced = cv2.bitwise_and(img, img, mask=white_mask)
# 反転（黒背景→白背景）
white_text = cv2.cvtColor(white_enhanced, cv2.COLOR_BGR2GRAY)
_, white_binary = cv2.threshold(white_text, 50, 255, cv2.THRESH_BINARY)
white_inverted = cv2.bitwise_not(white_binary)
# 前処理画像を保存（numpy経由でエンコード→バイナリ出力）
success, encoded = cv2.imencode('.png', white_inverted)
if success:
	with open(r'C:\Users\CARAMAS4\Desktop\919D_CRAMAS自動結果解析\波形取得\_ocr_preprocessed.png', 'wb') as f:
		f.write(encoded.tobytes())
print('前処理画像を _ocr_preprocessed.png に保存')

# 前処理画像でEasyOCRテスト
import easyocr
reader = easyocr.Reader(['en'], gpu=False)
results = reader.readtext(white_inverted)
print(f'\n前処理後のOCR検出数: {len(results)}')
high_conf = [(t, c) for _, t, c in results if c > 0.5]
print(f'信頼度0.5以上: {len(high_conf)}件')
for text, conf in sorted(high_conf, key=lambda x: x[1], reverse=True)[:20]:
	print(f'  [{conf:.2f}] "{text}"')
