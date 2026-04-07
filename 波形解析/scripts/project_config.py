# -*- coding: utf-8 -*-
"""
プロジェクト設定ローダー
config.yamlからプロジェクト固有設定を読み込む
"""
import os
import sys
from pathlib import Path

try:
	import yaml
except ImportError:
	# PyYAMLがない場合の簡易パーサー（config.yamlの基本構造のみ対応）
	yaml = None


# リポジトリルート（scripts/ の2階層上）
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PROJECTS_DIR = Path(__file__).resolve().parent.parent / "projects"


def _simple_yaml_parse(text: str) -> dict:
	"""PyYAMLなしでconfig.yamlを読める最低限のパーサー"""
	result = {}
	current_section = None
	current_list = None

	for line in text.splitlines():
		stripped = line.strip()
		if not stripped or stripped.startswith('#'):
			continue

		# トップレベルキー
		if not line.startswith(' ') and not line.startswith('\t'):
			if ':' in stripped:
				key, _, val = stripped.partition(':')
				key = key.strip()
				val = val.strip().strip('"').strip("'")
				if val:
					result[key] = val
				else:
					result[key] = {}
					current_section = key
					current_list = None
			continue

		# セクション内
		if current_section is not None:
			if stripped.startswith('- '):
				# リスト項目
				item = stripped[2:].strip()
				if current_list is not None:
					if isinstance(result[current_section], dict) and current_list in result[current_section]:
						if not isinstance(result[current_section][current_list], list):
							result[current_section][current_list] = []
						result[current_section][current_list].append({})
					continue

				if isinstance(result[current_section], dict):
					# name: value 形式のリスト
					pass
				continue

			if ':' in stripped:
				key, _, val = stripped.partition(':')
				key = key.strip()
				val = val.strip().strip('"').strip("'")
				if isinstance(result[current_section], dict):
					if val:
						# 数値変換
						try:
							val = int(val)
						except ValueError:
							pass
						result[current_section][key] = val
					else:
						result[current_section][key] = []
						current_list = key

	return result


def find_project(project_name: str = None) -> Path:
	"""プロジェクトのconfig.yamlを探す"""
	if project_name:
		config = PROJECTS_DIR / project_name / "config.yaml"
		if config.exists():
			return config
		raise FileNotFoundError(f"プロジェクト設定が見つかりません: {config}")

	# プロジェクト名未指定: projectsフォルダ内の唯一のプロジェクトを使用
	if PROJECTS_DIR.exists():
		projects = [d for d in PROJECTS_DIR.iterdir() if d.is_dir() and (d / "config.yaml").exists()]
		if len(projects) == 1:
			return projects[0] / "config.yaml"
		elif len(projects) > 1:
			names = [p.name for p in projects]
			raise ValueError(f"複数プロジェクトが存在します。--project で指定してください: {names}")

	raise FileNotFoundError(f"プロジェクトが見つかりません: {PROJECTS_DIR}")


def load_config(project_name: str = None) -> dict:
	"""config.yamlを読み込んで設定辞書を返す"""
	config_path = find_project(project_name)
	project_dir = config_path.parent

	with open(config_path, 'r', encoding='utf-8') as f:
		text = f.read()

	if yaml:
		cfg = yaml.safe_load(text)
	else:
		cfg = _simple_yaml_parse(text)

	# パス解決
	cfg['_project_dir'] = project_dir
	cfg['_repo_root'] = REPO_ROOT
	cfg['_project_name'] = project_dir.name

	# temp_dirを絶対パスに解決
	temp_dir = cfg.get('temp_dir', '.cache')
	cfg['temp_dir'] = REPO_ROOT / temp_dir

	return cfg


def get_ng_names(cfg: dict) -> dict:
	"""設定からNG番号→説明の辞書を返す"""
	raw = cfg.get('ng_names', {})
	return {int(k): v for k, v in raw.items()}


def get_ng_columns(cfg: dict) -> list:
	"""設定からNGカラム情報を返す: [(name, offset), ...]"""
	test_set = cfg.get('test_set', {})
	ng_cols = test_set.get('ng_columns', [])
	if isinstance(ng_cols, list) and ng_cols and isinstance(ng_cols[0], dict):
		return [(c['name'], c['offset']) for c in ng_cols]
	# デフォルト
	return [('ng_number1', 0), ('ng_number2', 32), ('ng_number3', 64)]


def get_step_column(cfg: dict) -> str:
	"""設定からステップカラム名を返す"""
	return cfg.get('test_set', {}).get('step_column', 'AfterStressChk_Step1')


def get_first_file_marker(cfg: dict) -> str:
	"""設定からテストセット開始マーカーを返す"""
	return cfg.get('test_set', {}).get('first_file_marker', '000h00m27s')


def get_xfileconv(cfg: dict) -> str:
	"""設定からXFileConvパスを返す"""
	return cfg.get('xfileconv', r'C:\simbase\system\bin\XFileConv.exe')


def parse_project_arg(argv: list = None) -> tuple:
	"""sys.argvから --project 引数を抽出し、(project_name, remaining_args) を返す"""
	if argv is None:
		argv = sys.argv[1:]
	project = None
	remaining = []
	i = 0
	while i < len(argv):
		if argv[i] == '--project' and i + 1 < len(argv):
			project = argv[i + 1]
			i += 2
		else:
			remaining.append(argv[i])
			i += 1
	return project, remaining
