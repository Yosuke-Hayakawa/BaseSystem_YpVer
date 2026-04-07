"""オシロスコープ LIN ID変更＋連続キャプチャスクリプト"""
import pyvisa
import os
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "画像ファイル")
TEKTRONIX_VID = "0x0699"
TEMP_PATH_ON_SCOPE = "C:/temp_cap.png"

# キャプチャ対象のLINフレーム
TARGETS = [
	# (名前, FrameID, 6bitバイナリ)
	("STL1S01_0x33", 0x33, "110011"),
	("IDB1S01_0x31", 0x31, "110001"),
	("IDT1S01_0x30", 0x30, "110000"),
]


def find_oscilloscope():
	rm = pyvisa.ResourceManager()
	resources = rm.list_resources()
	for res in resources:
		if "USB" in res.upper() and TEKTRONIX_VID.upper() in res.upper():
			return rm, res
	for res in resources:
		if "USB" in res.upper():
			try:
				inst = rm.open_resource(res)
				idn = inst.query("*IDN?").strip()
				if "TEKTRONIX" in idn.upper():
					inst.close()
					return rm, res
				inst.close()
			except Exception:
				pass
	return rm, None


def capture_and_save(inst, filename):
	"""画面キャプチャしてファイル保存"""
	inst.write(f'SAVe:IMAGe "{TEMP_PATH_ON_SCOPE}"')
	inst.query("*OPC?")
	inst.write(f'FILESystem:READFile "{TEMP_PATH_ON_SCOPE}"')
	img_data = inst.read_raw()
	inst.write(f'FILESystem:DELEte "{TEMP_PATH_ON_SCOPE}"')

	os.makedirs(IMAGE_DIR, exist_ok=True)
	filepath = os.path.join(IMAGE_DIR, filename)
	with open(filepath, "wb") as f:
		f.write(img_data)
	print(f"  保存: {filepath} ({len(img_data):,} bytes)")
	return filepath


def main():
	rm, res = find_oscilloscope()
	if res is None:
		print("[エラー] オシロスコープが見つかりません")
		return False

	inst = rm.open_resource(res)
	inst.timeout = 60000

	idn = inst.query("*IDN?").strip()
	print(f"接続: {idn}")

	# LINバス番号を特定
	lin_bus = None
	for i in range(1, 5):
		try:
			bus_type = inst.query(f"BUS:B{i}:TYPe?").strip()
			print(f"  B{i}: {bus_type}")
			if "LIN" in bus_type.upper():
				lin_bus = i
		except Exception:
			pass

	if lin_bus is None:
		print("[エラー] LINバスが見つかりません")
		inst.close()
		return False

	print(f"\nLINバス番号: B{lin_bus}")

	# 現在の設定を確認
	try:
		id_format = inst.query(f"BUS:B{lin_bus}:LIN:IDFORmat?").strip()
		print(f"IDフォーマット: {id_format}")
	except Exception as e:
		print(f"IDフォーマット確認エラー: {e}")

	try:
		current_cond = inst.query(f"TRIGger:A:BUS:B{lin_bus}:LIN:CONDition?").strip()
		print(f"トリガ条件: {current_cond}")
	except Exception as e:
		print(f"トリガ条件確認エラー: {e}")

	try:
		current_id = inst.query(f"TRIGger:A:BUS:B{lin_bus}:LIN:IDentifier:VALue?").strip()
		print(f"現在のID値: {current_id}")
	except Exception as e:
		print(f"ID値確認エラー: {e}")

	# まず現在の画面をそのままキャプチャ（0x33見えてるはず）
	timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
	print(f"\n--- 現在の画面をキャプチャ ---")
	capture_and_save(inst, f"engON_current_{timestamp}.png")

	# 各ターゲットIDに変更してキャプチャ
	for name, frame_id, binary_str in TARGETS:
		print(f"\n--- {name} (FrameID=0x{frame_id:02X}) ---")

		# トリガ条件をIdentifierに設定
		inst.write(f"TRIGger:A:BUS:B{lin_bus}:LIN:CONDition IDentifier")
		# IDを設定
		inst.write(f'TRIGger:A:BUS:B{lin_bus}:LIN:IDentifier:VALue "{binary_str}"')
		inst.query("*OPC?")

		# 少し待ってからキャプチャ（トリガがかかるのを待つ）
		import time
		time.sleep(2)

		ts = datetime.now().strftime("%Y%m%d_%H%M%S")
		capture_and_save(inst, f"engON_{name}_{ts}.png")

	print("\n=== 全キャプチャ完了 ===")
	inst.close()
	return True


if __name__ == "__main__":
	success = main()
	if not success:
		sys.exit(1)
