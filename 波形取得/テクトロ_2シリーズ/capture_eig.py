"""追加キャプチャ: EIG1S01(0x22)"""
import pyvisa
import os
import time
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "画像ファイル")
TEKTRONIX_VID = "0x0699"
TEMP_PATH_ON_SCOPE = "C:/temp_cap.png"

rm = pyvisa.ResourceManager()
resources = rm.list_resources()
res = None
for r in resources:
	if "USB" in r.upper() and TEKTRONIX_VID.upper() in r.upper():
		res = r
		break

inst = rm.open_resource(res)
inst.timeout = 60000
print(f"接続: {inst.query('*IDN?').strip()}")

# EIG1S01 (FrameID=0x22 = 100010)
binary_str = "100010"
print(f"EIG1S01 (0x22) に変更: {binary_str}")
inst.write(f'TRIGger:A:BUS:B1:LIN:CONDition IDentifier')
inst.write(f'TRIGger:A:BUS:B1:LIN:IDentifier:VALue "{binary_str}"')
inst.query("*OPC?")
time.sleep(2)

inst.write(f'SAVe:IMAGe "{TEMP_PATH_ON_SCOPE}"')
inst.query("*OPC?")
inst.write(f'FILESystem:READFile "{TEMP_PATH_ON_SCOPE}"')
img_data = inst.read_raw()
inst.write(f'FILESystem:DELEte "{TEMP_PATH_ON_SCOPE}"')

ts = datetime.now().strftime("%Y%m%d_%H%M%S")
os.makedirs(IMAGE_DIR, exist_ok=True)
filepath = os.path.join(IMAGE_DIR, f"engON_EIG1S01_0x22_{ts}.png")
with open(filepath, "wb") as f:
	f.write(img_data)
print(f"保存: {filepath} ({len(img_data):,} bytes)")

# 元に戻す（0x33）
inst.write('TRIGger:A:BUS:B1:LIN:IDentifier:VALue "110011"')
inst.query("*OPC?")
print("トリガを0x33に復帰")

inst.close()
print("完了")
