"""
仕様書変換スクリプト — doc→docx, xls→xlsx 一括変換
Word/Excel COM経由で旧形式を新形式（Open XML）に変換する。

使い方:
    python convert_to_openxml.py [--src フォルダパス] [--delete-old]

オプション:
    --src        変換対象フォルダ（デフォルト: カレントディレクトリ）
    --delete-old 変換成功後に元の.doc/.xlsファイルをゴミ箱に送る

前提:
    - Windows環境
    - Microsoft Word / Excel がインストールされていること
    - pip install pywin32 send2trash
"""

import glob
import os
import sys
import argparse
import time


def convert_word_files(src_dir: str, delete_old: bool = False):
	"""doc → docx 変換（Word COM経由）"""
	import win32com.client

	doc_files = glob.glob(os.path.join(src_dir, "**", "*.doc"), recursive=True)
	# .docx は除外、~$ 一時ファイルも除外
	doc_files = [f for f in doc_files
				 if not f.endswith(".docx") and not os.path.basename(f).startswith("~$")]

	if not doc_files:
		print("[Word] 変換対象の .doc ファイルなし")
		return [], []

	print(f"[Word] {len(doc_files)} 件の .doc ファイルを変換開始...")
	word = win32com.client.Dispatch("Word.Application")
	word.Visible = False
	word.DisplayAlerts = 0

	converted = []
	failed = []

	for doc_path in doc_files:
		abs_path = os.path.abspath(doc_path)
		docx_path = abs_path + "x"

		if os.path.exists(docx_path):
			print(f"  [スキップ] 既に存在: {os.path.basename(docx_path)}")
			continue

		try:
			print(f"  [変換中] {os.path.basename(abs_path)}")
			doc = word.Documents.Open(abs_path)
			doc.SaveAs2(docx_path, FileFormat=16)  # 16 = wdFormatXMLDocument (docx)
			doc.Close(0)
			converted.append(abs_path)
			print(f"  [完了]   → {os.path.basename(docx_path)}")
		except Exception as e:
			failed.append((abs_path, str(e)))
			print(f"  [失敗]   {os.path.basename(abs_path)}: {e}")

	word.Quit()
	time.sleep(1)

	print(f"\n[Word] 変換完了: {len(converted)} 成功, {len(failed)} 失敗")

	if delete_old and converted:
		_send_to_trash(converted)

	return converted, failed


def convert_excel_files(src_dir: str, delete_old: bool = False):
	"""xls → xlsx 変換（Excel COM経由）"""
	import win32com.client

	xls_files = glob.glob(os.path.join(src_dir, "**", "*.xls"), recursive=True)
	# .xlsx, .xlsm は除外、~$ 一時ファイルも除外
	xls_files = [f for f in xls_files
				 if not f.endswith((".xlsx", ".xlsm")) and not os.path.basename(f).startswith("~$")]

	if not xls_files:
		print("[Excel] 変換対象の .xls ファイルなし")
		return [], []

	print(f"[Excel] {len(xls_files)} 件の .xls ファイルを変換開始...")
	excel = win32com.client.Dispatch("Excel.Application")
	excel.Visible = False
	excel.DisplayAlerts = False

	converted = []
	failed = []

	for xls_path in xls_files:
		abs_path = os.path.abspath(xls_path)
		xlsx_path = abs_path + "x"

		if os.path.exists(xlsx_path):
			print(f"  [スキップ] 既に存在: {os.path.basename(xlsx_path)}")
			continue

		try:
			print(f"  [変換中] {os.path.basename(abs_path)}")
			wb = excel.Workbooks.Open(abs_path)
			wb.SaveAs(xlsx_path, FileFormat=51)  # 51 = xlOpenXMLWorkbook (xlsx)
			wb.Close(0)
			converted.append(abs_path)
			print(f"  [完了]   → {os.path.basename(xlsx_path)}")
		except Exception as e:
			failed.append((abs_path, str(e)))
			print(f"  [失敗]   {os.path.basename(abs_path)}: {e}")

	excel.Quit()
	time.sleep(1)

	print(f"\n[Excel] 変換完了: {len(converted)} 成功, {len(failed)} 失敗")

	if delete_old and converted:
		_send_to_trash(converted)

	return converted, failed


def _send_to_trash(file_list: list):
	"""旧ファイルをゴミ箱に送る（os.remove禁止ルール準拠）"""
	try:
		from send2trash import send2trash
		for f in file_list:
			send2trash(f)
			print(f"  [ゴミ箱] {os.path.basename(f)}")
	except ImportError:
		print("[警告] send2trash がインストールされていません。旧ファイルは手動で削除してください。")
		print("       pip install send2trash")


def main():
	parser = argparse.ArgumentParser(description="doc→docx, xls→xlsx 一括変換")
	parser.add_argument("--src", default=".",
						help="変換対象フォルダ（デフォルト: カレントディレクトリ）")
	parser.add_argument("--delete-old", action="store_true",
						help="変換成功後に元ファイルをゴミ箱に送る")
	args = parser.parse_args()

	src_dir = os.path.abspath(args.src)
	print(f"=== 仕様書変換スクリプト ===")
	print(f"対象フォルダ: {src_dir}")
	print(f"旧ファイル削除: {'あり（ゴミ箱）' if args.delete_old else 'なし'}")
	print()

	if not os.path.isdir(src_dir):
		print(f"[エラー] フォルダが見つかりません: {src_dir}")
		sys.exit(1)

	convert_word_files(src_dir, args.delete_old)
	print()
	convert_excel_files(src_dir, args.delete_old)

	print("\n=== 全変換処理完了 ===")


if __name__ == "__main__":
	main()
