# -*- coding: utf-8 -*-
"""
dat→CSV結合スクリプト
要解析フォルダ内の試験セットを1試験=1CSVに変換する
プロジェクト固有設定はprojects/<name>/config.yamlで管理

使い方:
  python dat_to_csv.py <要解析フォルダパス>
  python dat_to_csv.py --project 919D
  python dat_to_csv.py  (引数なしでデフォルトプロジェクトの要解析フォルダ全体を処理)
"""
import re
import os
import sys
import time
import subprocess
import pandas as pd
from pathlib import Path

from project_config import (
	load_config, get_xfileconv, get_first_file_marker, parse_project_arg
)

_project_name, _remaining_args = parse_project_arg()
CFG = load_config(_project_name)
XFILECONV = get_xfileconv(CFG)
TEMP_DIR = CFG['temp_dir']
FIRST_FILE_MARKER = get_first_file_marker(CFG)
ANOMALY_DIR = CFG['_project_dir'] / "要解析"


def convert_dat(dat_path: Path) -> pd.DataFrame | None:
	"""datファイルをXFileConvでCSV変換してDataFrameで返す"""
	TEMP_DIR.mkdir(parents=True, exist_ok=True)
	csv_tmp = TEMP_DIR / f"xconv_{os.getpid()}_{dat_path.stem}.csv"

	si = subprocess.STARTUPINFO()
	si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
	si.wShowWindow = 0

	for _ in range(3):
		if csv_tmp.exists():
			try: csv_tmp.unlink()
			except: pass
		r = subprocess.run(
			[XFILECONV, "-i", str(dat_path), "-o", str(csv_tmp)],
			capture_output=True, startupinfo=si
		)
		stdout = (r.stdout or b'').decode('cp932', errors='ignore').lower()
		if "success" in stdout and csv_tmp.exists():
			try:
				df = pd.read_csv(csv_tmp, encoding='cp932', skiprows=1, low_memory=False)
				return df
			except Exception as e:
				print(f"      CSV読み込みエラー: {e}")
				return None
			finally:
				try: csv_tmp.unlink()
				except: pass
		time.sleep(1)
	return None


def build_test_sets(folder: Path) -> list[dict]:
	"""フォルダ内のdatをmtime順で試験セットにグループ化する"""
	all_dats = sorted(
		[f for f in folder.iterdir() if f.suffix == '.dat'],
		key=lambda f: f.stat().st_mtime
	)
	if not all_dats:
		return []

	sets: list[list[Path]] = []
	current: list[Path] = []

	for f in all_dats:
		if FIRST_FILE_MARKER in f.name:
			if current:
				sets.append(current)
			current = [f]
		else:
			current.append(f)
	if current:
		sets.append(current)

	result = []
	for s in sets:
		t1_file = None
		for f in s:
			if re.search(r'T1\(\d+\)', f.name):
				t1_file = f
		if t1_file:
			t1_num = re.search(r'T1\((\d+)\)', t1_file.name).group(1)
			result.append({'t1_num': t1_num, 't1_name': t1_file.stem, 'files': s})
	return result


def convert_test_set(test_set: dict, out_dir: Path) -> Path | None:
	"""1試験セットの全datを変換→結合→1CSVとして出力"""
	dfs = []
	for dat_path in test_set['files']:
		print(f"    {dat_path.name}", end=" ")
		df = convert_dat(dat_path)
		if df is None:
			print("→ エラー")
			continue
		df.insert(0, '_source', dat_path.name)
		dfs.append(df)
		print(f"→ {len(df)}行")

	if not dfs:
		return None

	merged = pd.concat(dfs, ignore_index=True)
	out_path = out_dir / f"{test_set['t1_name']}.csv"
	merged.to_csv(out_path, index=False, encoding='utf-8-sig')
	return out_path


def process_folder(folder: Path):
	"""1フォルダ内の代表1試験セットのみCSV変換する（同じNGパターンなので1件で十分）"""
	test_sets = build_test_sets(folder)
	if not test_sets:
		print(f"  試験セットなし")
		return 0

	print(f"  {len(test_sets)}試験セット検出（代表1件のみ変換）")

	# 既にCSVがあればスキップ
	existing = list(folder.glob("*.csv"))
	if existing:
		print(f"  → {existing[0].name} 既存、スキップ")
		return 1

	ts = test_sets[0]
	print(f"  [1/{len(test_sets)}] T1({ts['t1_num']}) {len(ts['files'])}ファイル")
	out = convert_test_set(ts, folder)
	if out:
		print(f"    → {out.name} ({out.stat().st_size // 1024}KB)")
		return 1
	else:
		print(f"    → 変換失敗")
		return 0


def main():
	if _remaining_args:
		# 引数指定: 単一フォルダ処理
		folder = Path(_remaining_args[0])
		if not folder.exists():
			print(f"フォルダが見つかりません: {folder}")
			return
		print(f"対象: {folder.name}")
		process_folder(folder)
	else:
		# 引数なし: 要解析フォルダ全体
		if not ANOMALY_DIR.exists():
			print(f"要解析フォルダが見つかりません: {ANOMALY_DIR}")
			return
		subfolders = sorted([d for d in ANOMALY_DIR.iterdir() if d.is_dir()])
		print(f"要解析フォルダ: {len(subfolders)}サブフォルダ\n")
		total = 0
		for folder in subfolders:
			print(f"[{folder.name}]")
			total += process_folder(folder)
			print()
		print(f"完了: {total}試験セット変換")

	# 一時ファイル掃除
	if TEMP_DIR.exists():
		for f in TEMP_DIR.glob("xconv_*"):
			try: f.unlink()
			except: pass


if __name__ == "__main__":
	main()
