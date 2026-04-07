"""IG ON(エンジンOFF)状態で残り3フレームをキャプチャ"""
import pyvisa
import os
import time
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "画像ファイル")
TEKTRONIX_VID = "0x0699"
TEMP_PATH_ON_SCOPE = "C:/temp_cap.png"

TARGETS = [
	("IDB1S01_0x31", "110001"),
	("IDT1S01_0x30", "110000"),
	("EIG1S01_0x22", "100010"),
]

rm = pyvisa.ResourceManager()
res = None
for r in rm.list_resources():
	if "USB" in r.upper() and TEKTRONIX_VID.upper() in r.upper():
		res = r
		break

inst = rm.open_resource(res)
inst.timeout = 60000
print(f"接続: {inst.query('*IDN?').strip()}")

for name, binary_str in TARGETS:
	print(f"\n--- {name} ---")
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
	filepath = os.path.join(IMAGE_DIR, f"igON_{name}_{ts}.png")
	with open(filepath, "wb") as f:
		f.write(img_data)
	print(f"  保存: {filepath} ({len(img_data):,} bytes)")

# 元に戻す
inst.write('TRIGger:A:BUS:B1:LIN:IDentifier:VALue "110011"')
inst.query("*OPC?")
print("\nトリガ復帰: 0x33")
inst.close()
print("全完了")
