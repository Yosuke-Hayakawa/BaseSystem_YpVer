# -*- coding: utf-8 -*-
"""
NG解析結果MDから特異パターンのファイルを抽出して要解析フォルダに分類コピーする
T1 NGファイル＋同じ試験セットの時系列datファイルを丸ごとコピーする

試験セットの法則:
  000h00m27s ファイル → セット開始
  時系列datが続く
  T1 NG/OKファイル → セット末尾
  次の 000h00m27s ファイル → 次セット開始
"""
import re
import shutil
from pathlib import Path
from collections import Counter

# ====== 設定 ======
RESULT_DIR = Path(r"C:\Users\CARAMAS4\Desktop\919D_CRAMAS自動結果解析\結果")
LOG_DIR = Path(r"C:\Users\CARAMAS4\Desktop\919D_CRAMAS自動結果解析\ログデータ")
OUT_DIR = Path(r"C:\Users\CARAMAS4\Desktop\919D_CRAMAS自動結果解析\要解析")
# ==================


def find_latest_md(result_dir: Path) -> Path:
	"""結果フォルダ内の最新NGMDファイルを返す"""
	mds = sorted(result_dir.glob("*_NG解析結果.md"), reverse=True)
	if not mds:
		raise FileNotFoundError(f"NG解析結果MDが見つかりません: {result_dir}")
	return mds[0]


def parse_md(md_path: Path) -> dict[str, list[tuple[int, int]]]:
	"""MDを解析して {ファイル名: [(NG番号, case), ...]} を返す"""
	files = {}
	current_file = None
	current_ngs = []
	in_file_section = False

	for line in md_path.read_text(encoding="utf-8").splitlines():
		m = re.match(r'^## (.+_NG.*\.dat)', line)
		if m:
			if current_file:
				files[current_file] = current_ngs
			current_file = m.group(1)
			current_ngs = []
			in_file_section = True
			continue

		if re.match(r'^\| NG番号 \| 内容 \| case \| 件数', line):
			in_file_section = False
			if current_file:
				files[current_file] = current_ngs
				current_file = None

		if not in_file_section:
			continue

		m = re.match(r'^\|\s*(\d+)\s*\|.*\|\s*(\d+)\s*\|', line)
		if m:
			current_ngs.append((int(m.group(1)), int(m.group(2))))

	return files


def build_test_sets(log_dir: Path) -> dict[str, list[Path]]:
	"""ログデータをmtime順に並べて試験セットを構築する
	{T1ファイル名: [セット内の全ファイルパス]} を返す"""
	all_files = sorted(log_dir.iterdir(), key=lambda f: f.stat().st_mtime)

	sets: list[list[Path]] = []
	current_set: list[Path] = []

	for f in all_files:
		if '000h00m27s' in f.name:
			if current_set:
				sets.append(current_set)
			current_set = [f]
		else:
			current_set.append(f)
	if current_set:
		sets.append(current_set)

	# T1ファイルをキーにdict化
	result: dict[str, list[Path]] = {}
	for s in sets:
		for f in s:
			if re.search(r'T1\(\d+\)', f.name):
				result[f.name] = s
	return result


def make_folder_name(pattern: tuple) -> str:
	"""パターンからフォルダ名を生成"""
	parts = [f"NG{ng}_c{case}" for ng, case in sorted(pattern)]
	name = "__".join(parts)
	if len(name) > 200:
		name = name[:200]
	return name


def main():
	md_path = find_latest_md(RESULT_DIR)
	print(f"MD解析中: {md_path.name}")

	file_patterns = parse_md(md_path)
	print(f"  → {len(file_patterns)}ファイルのパターンを取得")

	# 多数派パターン特定
	pattern_count = Counter(tuple(sorted(ngs)) for ngs in file_patterns.values())
	majority_pattern = pattern_count.most_common(1)[0][0]
	majority_count = pattern_count.most_common(1)[0][1]
	print(f"  → 多数派パターン: {majority_count}件")

	# 特異ファイル抽出
	anomaly_files = {
		fname: tuple(sorted(ngs))
		for fname, ngs in file_patterns.items()
		if tuple(sorted(ngs)) != majority_pattern
	}
	print(f"  → 特異ファイル数: {len(anomaly_files)}件")

	if not anomaly_files:
		print("特異ファイルなし")
		return

	# パターンごとにグループ化
	pattern_groups: dict[tuple, list[str]] = {}
	for fname, pattern in anomaly_files.items():
		pattern_groups.setdefault(pattern, []).append(fname)

	print(f"\n特異パターン数: {len(pattern_groups)}種類")
	for pattern, fnames in sorted(pattern_groups.items(), key=lambda x: -len(x[1])):
		print(f"  {len(fnames)}件: {make_folder_name(pattern)}")

	# テストセット構築
	print(f"\nテストセット構築中...")
	test_sets = build_test_sets(LOG_DIR)
	print(f"  → {len(test_sets)}セット検出")

	OUT_DIR.mkdir(exist_ok=True)

	copied_files = 0
	copied_sets = 0
	not_found = 0

	for pattern, fnames in pattern_groups.items():
		folder_name = make_folder_name(pattern)
		dest_folder = OUT_DIR / folder_name
		dest_folder.mkdir(exist_ok=True)

		for fname in fnames:
			if fname not in test_sets:
				print(f"  [セット未発見] {fname}")
				not_found += 1
				continue

			set_files = test_sets[fname]
			copied_sets += 1
			for f in set_files:
				dst = dest_folder / f.name
				shutil.copy2(f, dst)
				copied_files += 1

	print(f"\n完了: {copied_sets}試験セット / {copied_files}ファイルコピー, {not_found}件セット未発見")
	print(f"要解析フォルダ: {OUT_DIR}")


if __name__ == "__main__":
	main()
	input("\nPress any key to continue . . .")
