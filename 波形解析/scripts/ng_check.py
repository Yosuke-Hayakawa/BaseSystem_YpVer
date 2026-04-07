# -*- coding: utf-8 -*-
"""
CRAMAS NG解析
_NGファイルのng_numberビットマスクからNG番号を特定して一覧化する
プロジェクト固有設定はprojects/<name>/config.yamlで管理
"""

import pandas as pd
import subprocess
import tempfile
import os
import sys
import re
import glob
from datetime import datetime
from pathlib import Path

from project_config import (
	load_config, get_ng_names, get_ng_columns, get_step_column,
	get_first_file_marker, get_xfileconv, parse_project_arg
)

# --project 引数の解析
_project_name, _remaining_args = parse_project_arg()
CFG = load_config(_project_name)
XFILECONV = get_xfileconv(CFG)
NG_NAMES = get_ng_names(CFG)
COL_INFO = get_ng_columns(CFG)
STEP_COL_NAME = get_step_column(CFG)
FIRST_FILE_MARKER = get_first_file_marker(CFG)

# デフォルトのログ/結果ディレクトリ（プロジェクトフォルダ基準）
_project_dir = CFG['_project_dir']
LOG_DIR = str(_project_dir / "data" / "ログデータ")
RESULT_DIR = str(_project_dir / "output")


def convert_dat_to_csv(dat_path):
	import time
	csv_path = tempfile.mktemp(suffix='.csv')
	si = subprocess.STARTUPINFO()
	si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
	si.wShowWindow = 0
	for _ in range(3):
		if os.path.exists(csv_path):
			try: os.remove(csv_path)
			except: pass
		r = subprocess.run([XFILECONV, "-i", dat_path, "-o", csv_path],
						   capture_output=True, startupinfo=si)
		stdout = (r.stdout or b'').decode('cp932', errors='ignore').lower()
		if "success" in stdout:
			return csv_path
		time.sleep(1)
	return None


def build_test_sets(log_dir):
	"""ログデータをmtime順に並べて試験セットを構築する
	{T1ファイル名: [セット内全ファイル名(時系列順)]} を返す"""
	all_files = sorted(
		[f for f in os.listdir(log_dir) if f.endswith('.dat') and f != 'tmp_smp.dat'],
		key=lambda f: os.path.getmtime(os.path.join(log_dir, f))
	)
	sets, current = [], []
	for f in all_files:
		if FIRST_FILE_MARKER in f:
			if current:
				sets.append(current)
			current = [f]
		else:
			current.append(f)
	if current:
		sets.append(current)

	result = {}
	for s in sets:
		for f in s:
			if re.search(r'T1\(\d+\)', f) or '_NG' in f or '_OK' in f:
				result[f] = s
	return result


def decode_ng_bits(ng_number1, ng_number2, ng_number3):
	"""ng_number1～3のビットマスクからNG番号リストを返す"""
	ngs = []
	for i in range(32):
		if int(ng_number1) & (1 << i):
			ngs.append(i + 1)       # NG1～32
	for i in range(32):
		if int(ng_number2) & (1 << i):
			ngs.append(i + 33)      # NG33～64
	for i in range(32):
		if int(ng_number3) & (1 << i):
			ngs.append(i + 65)      # NG65～96
	return sorted(ngs)


def _scan_bits(df, col_info, step_col):
	"""DataFrameからng_numberビット変化を検出し {ng番号: step} を返す
	prevは0開始"""
	ng_step = {}
	for col, offset in col_info:
		if col not in df.columns:
			continue
		vals = df[col].astype(float).fillna(0).astype(int)
		prev = 0
		for idx, cur in enumerate(vals):
			new_bits = cur & ~prev
			if new_bits:
				for i in range(32):
					if new_bits & (1 << i):
						ng_num = i + offset + 1
						step = int(float(df[step_col].iloc[idx])) if step_col else None
						if ng_num not in ng_step:
							ng_step[ng_num] = step
			prev = cur
	return ng_step


def analyze_ng_file(dat_path, test_set_files=None, log_dir=None):
	"""NGファイルを解析してNG番号と発生Stepを返す
	test_set_files指定時：T1先頭で既にビットが立っていれば時系列datを遡って正しいStepを取得"""
	csv_path = convert_dat_to_csv(dat_path)
	if csv_path is None:
		return None
	try:
		df = pd.read_csv(csv_path, encoding='cp932', skiprows=1, low_memory=False)
	except Exception:
		return None
	finally:
		try: os.remove(csv_path)
		except: pass

	step_col = STEP_COL_NAME if STEP_COL_NAME in df.columns else None

	# T1先頭で既に立っているビットを検出
	preexisting = set()
	for col, offset in COL_INFO:
		if col not in df.columns:
			continue
		first_val = int(float(df[col].fillna(0).iloc[0]))
		for i in range(32):
			if first_val & (1 << i):
				preexisting.add(i + offset + 1)

	# T1ファイル内のビット変化を検出（prev=0開始）
	ng_step = _scan_bits(df, COL_INFO, step_col)

	# T1先頭で既にビットが立っていた場合、時系列datを遡って正しいStepを取得
	if preexisting and test_set_files and log_dir:
		t1_name = os.path.basename(dat_path)
		earlier_files = [f for f in test_set_files if f != t1_name]

		# 時系列順に全ファイルを処理してprevを引き継ぐ
		prev_values = {}
		for col, _ in COL_INFO:
			prev_values[col] = 0

		for earlier_name in earlier_files:
			earlier_path = os.path.join(log_dir, earlier_name)
			ecsv = convert_dat_to_csv(earlier_path)
			if ecsv is None:
				continue
			try:
				edf = pd.read_csv(ecsv, encoding='cp932', skiprows=1, low_memory=False)
			except Exception:
				continue
			finally:
				try: os.remove(ecsv)
				except: pass

			e_step_col = STEP_COL_NAME if STEP_COL_NAME in edf.columns else None
			for col, offset in COL_INFO:
				if col not in edf.columns:
					continue
				vals = edf[col].astype(float).fillna(0).astype(int)
				prev = prev_values[col]
				for idx, cur in enumerate(vals):
					new_bits = cur & ~prev
					if new_bits:
						for i in range(32):
							if new_bits & (1 << i):
								ng_num = i + offset + 1
								if ng_num in preexisting and ng_num not in ng_step.get('_corrected', set()):
									step = int(float(edf[e_step_col].iloc[idx])) if e_step_col else None
									ng_step[ng_num] = step
									ng_step.setdefault('_corrected', set()).add(ng_num)
					prev = cur
				prev_values[col] = prev

	# 内部管理用キーを除去
	ng_step.pop('_corrected', None)
	return {'ng_step': ng_step}


def main():
	log_dir = _remaining_args[0] if _remaining_args else LOG_DIR
	os.makedirs(RESULT_DIR, exist_ok=True)

	# テストセット構築
	print("テストセット構築中...")
	test_sets = build_test_sets(log_dir)
	print(f"  → {len(test_sets)}セット検出")

	ng_files = sorted(
		[f for f in os.listdir(log_dir) if f.endswith('.dat') and '_NG' in f and f != 'tmp_smp.dat'],
		key=lambda f: os.path.getmtime(os.path.join(log_dir, f))
	)

	print(f"対象NGファイル数: {len(ng_files)}")
	print()

	timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
	md_path = os.path.join(RESULT_DIR, f"{timestamp}_NG解析結果.md")

	ng_summary = {}
	ng_case_summary = {}

	with open(md_path, 'w', encoding='utf-8') as f:
		f.write(f"# {CFG.get('project_name', 'CRAMAS')} NG解析結果\n\n")
		f.write(f"- 解析日時: {datetime.now().strftime('%Y/%m/%d %H:%M:%S')}\n")
		f.write(f"- 対象フォルダ: {log_dir}\n")
		f.write(f"- NGファイル数: {len(ng_files)}\n\n")
		f.write("---\n\n")

	errors = 0
	no_ng = 0

	for i, fname in enumerate(ng_files):
		dat_path = os.path.join(log_dir, fname)
		print(f"[{i+1}/{len(ng_files)}] {fname}")

		test_set_files = test_sets.get(fname)
		result = analyze_ng_file(dat_path, test_set_files, log_dir)
		if result is None:
			errors += 1
			print(f"  → 変換/読み込みエラー")
			continue

		if not result['ng_step']:
			no_ng += 1
			print(f"  → NG無し")
			continue

		ng_strs = [f"NG{n}({NG_NAMES.get(n, '?')}) case{s}" for n, s in sorted(result['ng_step'].items())]
		print(f"  → {', '.join(ng_strs)}")
		for n, s in result['ng_step'].items():
			ng_summary[n] = ng_summary.get(n, 0) + 1
			key = (n, s)
			ng_case_summary[key] = ng_case_summary.get(key, 0) + 1

		with open(md_path, 'a', encoding='utf-8') as f:
			f.write(f"## {fname}\n\n")
			f.write("| NG番号 | 内容 | 発生Step |\n")
			f.write("|--------|------|----------|\n")
			for n, s in sorted(result['ng_step'].items()):
				f.write(f"| {n} | {NG_NAMES.get(n, '不明')} | {s} |\n")
			f.write("\n")

	# 集計
	with open(md_path, 'a', encoding='utf-8') as f:
		f.write("---\n\n")
		f.write("## 集計\n\n")
		f.write(f"| 項目 | 件数 |\n|------|------|\n")
		f.write(f"| NGファイル数 | {len(ng_files)} |\n")
		f.write(f"| NG検出あり | {len(ng_files) - errors - no_ng} |\n")
		f.write(f"| NG無し | {no_ng} |\n")
		f.write(f"| エラー | {errors} |\n\n")

		if ng_summary:
			f.write("### NG番号 × case 集計（特異なcaseは★）\n\n")
			f.write("| NG番号 | 内容 | case | 件数 | 備考 |\n")
			f.write("|--------|------|------|------|------|\n")
			for ng in sorted(ng_summary.keys()):
				cases = {c: cnt for (n, c), cnt in ng_case_summary.items() if n == ng}
				total = sum(cases.values())
				max_cnt = max(cases.values())
				for case, cnt in sorted(cases.items(), key=lambda x: -x[1]):
					rare = "★ 特異" if cnt < max_cnt and cnt <= max(1, total * 0.2) else ""
					f.write(f"| {ng} | {NG_NAMES.get(ng, '不明')} | {case} | {cnt} | {rare} |\n")

	print()
	print("===== 完了 =====")
	print(f"NG検出あり: {len(ng_files) - errors - no_ng}")
	print(f"NG無し: {no_ng}")
	print(f"エラー: {errors}")
	print()
	print("NG番号 × case 集計:")
	for ng in sorted(ng_summary.keys()):
		cases = {c: cnt for (n, c), cnt in ng_case_summary.items() if n == ng}
		total = sum(cases.values())
		max_cnt = max(cases.values())
		case_strs = []
		for case, cnt in sorted(cases.items(), key=lambda x: -x[1]):
			rare = " ★特異" if cnt < max_cnt and cnt <= max(1, total * 0.2) else ""
			case_strs.append(f"case{case}:{cnt}件{rare}")
		print(f"  NG{ng}({NG_NAMES.get(ng, '?')}): {', '.join(case_strs)}")
	print()
	print(f"結果MD: {md_path}")


if __name__ == "__main__":
	main()
