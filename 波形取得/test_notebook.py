import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from IPython.display import display

# テスト画像読み込み
img = Image.open(r'C:\Users\CARAMAS4\Desktop\919D_CRAMAS自動結果解析\波形取得\screen_20260320_183001.png')
arr = np.array(img)
print(f"画像サイズ: {img.size}, モード: {img.mode}")

# 画像を表示
plt.figure(figsize=(12, 7.5))
plt.imshow(arr)
plt.title("Oscilloscope Screenshot")
plt.axis('off')
plt.tight_layout()
plt.show()
