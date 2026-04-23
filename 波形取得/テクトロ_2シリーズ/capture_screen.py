# オシロスコープ(MSO22/MSO24) 画面キャプチャスクリプト
import pyvisa
import os
import sys
from datetime import datetime


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(SCRIPT_DIR, "画像ファイル")
TEKTRONIX_VID = "0x0699"
TEMP_PATH_ON_SCOPE = "C:/temp_cap.png"


def find_oscilloscope():
	"""USB接続のTektronixオシロスコープを自動検出"""
	rm = pyvisa.ResourceManager()
	resources = rm.list_resources()

	# USB TMCデバイスからTektronix製を探す
	for res in resources:
		if "USB" in res.upper() and TEKTRONIX_VID.upper() in res.upper():
			return rm, res

	# 見つからなければ全USBデバイスを試す
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


def capture_screen(resource_string=None):
	"""オシロの画面をキャプチャしてPNG保存"""
	rm, auto_res = find_oscilloscope()

	res = resource_string or auto_res
	if res is None:
		print("[エラー] オシロスコープが見つかりません。USB接続を確認してください。")
		print(f"  検出されたVISAリソース: {rm.list_resources()}")
		return False

	try:
		inst = rm.open_resource(res)
		inst.timeout = 60000  # 60秒タイムアウト

		# 機器情報取得
		idn = inst.query("*IDN?").strip()
		print(f"接続: {idn}")

		# オシロ側に一時ファイルとして画面保存
		inst.write(f'SAVe:IMAGe "{TEMP_PATH_ON_SCOPE}"')
		inst.query("*OPC?")  # 保存完了待ち

		# オシロからファイルを読み出し
		inst.write(f'FILESystem:READFile "{TEMP_PATH_ON_SCOPE}"')
		img_data = inst.read_raw()

		# オシロ上の一時ファイル削除
		inst.write(f'FILESystem:DELEte "{TEMP_PATH_ON_SCOPE}"')

		inst.close()

	except pyvisa.errors.VisaIOError as e:
		print(f"[エラー] VISA通信エラー: {e}")
		return False
	except Exception as e:
		print(f"[エラー] 予期しないエラー: {e}")
		return False

	# タイムスタンプ付きファイル名で保存
	timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
	filename = f"screen_{timestamp}.png"
	os.makedirs(IMAGE_DIR, exist_ok=True)
	filepath = os.path.join(IMAGE_DIR, filename)

	with open(filepath, "wb") as f:
		f.write(img_data)

	print(f"保存完了: {filepath}")
	print(f"サイズ: {len(img_data):,} bytes")
	return True


if __name__ == "__main__":
	# 引数でVISAアドレス指定可能（省略時は自動検出）
	addr = sys.argv[1] if len(sys.argv) > 1 else None
	success = capture_screen(addr)
	if not success:
		input("\nEnterキーで閉じます...")
		sys.exit(1)
	input("\nEnterキーで閉じます...")
