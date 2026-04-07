# -*- coding: utf-8 -*-
"""CRAMASログ波形ビューア"""

import sys
import os
import re
import subprocess
from pathlib import Path

import pandas as pd
import pyqtgraph as pg
from PySide6.QtWidgets import (
	QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
	QListWidget, QListWidgetItem, QPushButton, QLabel, QFileDialog,
	QSplitter, QGroupBox, QStatusBar
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from project_config import load_config, get_xfileconv, get_first_file_marker

# 設定読み込み（GUIアプリなので--project引数は使わず、デフォルトプロジェクトを使用）
try:
	CFG = load_config()
	XFILECONV = get_xfileconv(CFG)
	FIRST_FILE_MARKER = get_first_file_marker(CFG)
	TEMP_DIR = CFG['temp_dir']
except Exception:
	XFILECONV = r"C:\simbase\system\bin\XFileConv.exe"
	FIRST_FILE_MARKER = "000h00m27s"
	TEMP_DIR = Path(__file__).resolve().parent.parent.parent / ".cache"

TEMP_DIR = Path(TEMP_DIR)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

RE_TIMESERIES = re.compile(r'_\d+h\d+m\d+s\.dat$', re.IGNORECASE)
RE_FIRST_FILE = re.compile(re.escape(FIRST_FILE_MARKER) + r'\.dat$', re.IGNORECASE)
RE_T1 = re.compile(r'T1\((\d+)\).*_(OK|NG)[^.]*\.dat$', re.IGNORECASE)

COLORS = [
	'#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
	'#9467bd', '#8c564b', '#e377c2', '#17becf',
	'#bcbd22', '#7f7f7f'
]


def scan_folder(folder: str) -> list:
	"""フォルダをスキャンして試験セットリストを返す"""
	all_files = sorted(Path(folder).glob('*.dat'), key=lambda f: f.stat().st_mtime)
	sets = []
	current_ts = []

	for f in all_files:
		if RE_FIRST_FILE.search(f.name):
			# 000h00m27s → 新セット開始
			current_ts = [f]
		elif RE_TIMESERIES.search(f.name):
			if current_ts:
				current_ts.append(f)
		elif RE_T1.search(f.name):
			m = RE_T1.search(f.name)
			sets.append({
				'T1': m.group(1),
				'result': m.group(2).upper(),
				'timeseries': current_ts.copy(),
				't1_file': f
			})
			current_ts = []

	return sets


def convert_dat(dat_path: Path, csv_path: Path) -> bool:
	"""XFileConvでdatをCSVに変換。成功したらTrue"""
	if not Path(XFILECONV).exists():
		return False
	result = subprocess.run(
		[XFILECONV, "-i", str(dat_path), "-o", str(csv_path)],
		capture_output=True,
		text=False
	)
	stdout = result.stdout or b''
	return b'success' in stdout.lower()


def load_test_set(test_set: dict) -> pd.DataFrame | None:
	"""試験セットのdatをCSV変換して連結したDataFrameを返す"""
	dfs = []
	for dat_file in test_set['timeseries']:
		# 一時CSVパス（フォルダ名+ファイル名でユニーク化）
		safe_stem = dat_file.parent.name + '_' + dat_file.stem
		csv_path = TEMP_DIR / (safe_stem + '.csv')

		ok = convert_dat(dat_file, csv_path)
		if not ok:
			# 変換失敗時は既存CSVがあれば使用
			if not csv_path.exists():
				continue

		try:
			df = pd.read_csv(csv_path, encoding='cp932', skiprows=1)
			dfs.append(df)
		except Exception as e:
			print(f"[WARN] CSV読み込みエラー {csv_path}: {e}")

	if not dfs:
		return None

	combined = pd.concat(dfs, ignore_index=True)
	if 'TIME(sec)' in combined.columns:
		combined = combined.sort_values('TIME(sec)').reset_index(drop=True)
	return combined


class WaveViewer(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setWindowTitle("波形ビューア - CRAMASログ解析")
		self.resize(1400, 800)

		self.test_sets: list = []
		self.current_df: pd.DataFrame | None = None
		self.plots: dict = {}  # name -> PlotItem
		self.x_ref_plot = None
		self.color_idx = 0

		self._setup_ui()
		self.setStatusBar(QStatusBar())

	def _setup_ui(self):
		central = QWidget()
		self.setCentralWidget(central)
		layout = QHBoxLayout(central)
		layout.setContentsMargins(4, 4, 4, 4)

		splitter = QSplitter(Qt.Horizontal)
		layout.addWidget(splitter)

		# ===== 左パネル =====
		left = QWidget()
		left.setMinimumWidth(240)
		left.setMaximumWidth(320)
		left_layout = QVBoxLayout(left)
		left_layout.setSpacing(4)

		# フォルダ選択
		btn_open = QPushButton("📂 フォルダを開く")
		btn_open.clicked.connect(self.open_folder)
		left_layout.addWidget(btn_open)

		self.lbl_folder = QLabel("（未選択）")
		self.lbl_folder.setWordWrap(True)
		self.lbl_folder.setStyleSheet("color: gray; font-size: 11px;")
		left_layout.addWidget(self.lbl_folder)

		# T1番号一覧
		grp_t1 = QGroupBox("T1番号一覧")
		grp_t1_layout = QVBoxLayout(grp_t1)
		self.t1_list = QListWidget()
		self.t1_list.currentRowChanged.connect(self.on_t1_selected)
		grp_t1_layout.addWidget(self.t1_list)
		left_layout.addWidget(grp_t1)

		# 信号一覧
		grp_sig = QGroupBox("信号一覧（ダブルクリックで追加）")
		grp_sig_layout = QVBoxLayout(grp_sig)
		self.sig_list = QListWidget()
		self.sig_list.itemDoubleClicked.connect(self.on_signal_dblclick)
		grp_sig_layout.addWidget(self.sig_list)
		left_layout.addWidget(grp_sig)

		# クリアボタン
		btn_clear = QPushButton("グラフをクリア")
		btn_clear.clicked.connect(self.clear_plot)
		left_layout.addWidget(btn_clear)

		splitter.addWidget(left)

		# ===== 右パネル（グラフ） =====
		pg.setConfigOption('background', 'w')
		pg.setConfigOption('foreground', 'k')

		self.glw = pg.GraphicsLayoutWidget()
		splitter.addWidget(self.glw)
		splitter.setSizes([280, 1120])

	def open_folder(self):
		folder = QFileDialog.getExistingDirectory(self, "フォルダを選択")
		if folder:
			self.load_folder(folder)

	def load_folder(self, folder: str):
		self.test_sets = scan_folder(folder)
		self.lbl_folder.setText(os.path.basename(folder))
		self.t1_list.clear()
		self.sig_list.clear()
		self.clear_plot()

		for ts in self.test_sets:
			label = f"T1({ts['T1']})  {ts['result']}  [{len(ts['timeseries'])}ファイル]"
			item = QListWidgetItem(label)
			if ts['result'] == 'NG':
				item.setForeground(QColor('#cc0000'))
				item.setBackground(QColor('#fff0f0'))
			else:
				item.setForeground(QColor('#005500'))
			self.t1_list.addItem(item)

		self.statusBar().showMessage(f"{len(self.test_sets)} 試験を読み込みました")

	def on_t1_selected(self, row: int):
		if row < 0 or row >= len(self.test_sets):
			return

		ts = self.test_sets[row]
		self.statusBar().showMessage(f"T1({ts['T1']}) を変換中...")
		QApplication.processEvents()

		self.clear_plot()
		self.sig_list.clear()
		self.current_df = load_test_set(ts)

		if self.current_df is None:
			self.statusBar().showMessage("❌ データ読み込み失敗（XFileConvまたはdatファイルを確認してください）")
			return

		# 数値カラムのみ表示（TIME(sec)はX軸なので先頭に）
		numeric_cols = self.current_df.select_dtypes(include='number').columns.tolist()
		if 'TIME(sec)' in numeric_cols:
			numeric_cols.remove('TIME(sec)')
			numeric_cols.insert(0, 'TIME(sec)')

		for col in numeric_cols:
			self.sig_list.addItem(col)

		n = len(self.current_df)
		self.statusBar().showMessage(
			f"T1({ts['T1']}) {ts['result']} - {n} サンプル, {len(numeric_cols)} 信号"
		)

	def on_signal_dblclick(self, item: QListWidgetItem):
		name = item.text()
		if self.current_df is None:
			return
		if name == 'TIME(sec)' or name in self.plots:
			return
		if name not in self.current_df.columns:
			return

		x_col = 'TIME(sec)' if 'TIME(sec)' in self.current_df.columns else None
		x = self.current_df[x_col].values if x_col else range(len(self.current_df))
		y = self.current_df[name].values

		color = COLORS[self.color_idx % len(COLORS)]
		self.color_idx += 1

		row = len(self.plots)
		p = self.glw.addPlot(row=row, col=0)
		p.showGrid(x=True, y=True, alpha=0.3)
		p.setLabel('left', name, size='9pt')
		p.setLabel('bottom', 'TIME(sec)')
		pen = pg.mkPen(color=color, width=1.5)
		p.plot(x, y, pen=pen)

		if self.x_ref_plot is None:
			self.x_ref_plot = p
		else:
			p.setXLink(self.x_ref_plot)

		self.plots[name] = p

	def clear_plot(self):
		"""グラフをクリア"""
		self.glw.clear()
		self.plots = {}
		self.color_idx = 0
		self.x_ref_plot = None


if __name__ == '__main__':
	app = QApplication(sys.argv)
	viewer = WaveViewer()

	# 引数でフォルダ指定可能
	if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
		viewer.load_folder(sys.argv[1])

	viewer.show()
	sys.exit(app.exec())
