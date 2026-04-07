"""
VS Code Copilot Chatセッション復旧スクリプト（スタンドアロン版）

旧ワークスペースのチャットセッションを新ワークスペースにマージする。
VS Codeを完全に閉じた状態で実行すること。
"""
import sqlite3
import json
import shutil
import os
import sys
import subprocess
from datetime import datetime

# === パス定数 ===
OLD_STORAGE = r'C:\Users\CARAMAS4\AppData\Roaming\Code\User\workspaceStorage\7f7b6e1f0e8c620f998142ae12bb2149'
NEW_STORAGE = r'C:\Users\CARAMAS4\AppData\Roaming\Code\User\workspaceStorage\ba6259d18f991b35c35aeb6511d20538'
BACKUP_DIR = r'C:\Users\CARAMAS4\git-practice\cramas-analysis\一時'

OLD_DB = os.path.join(OLD_STORAGE, 'state.vscdb')
NEW_DB = os.path.join(NEW_STORAGE, 'state.vscdb')
OLD_SESSIONS_DIR = os.path.join(OLD_STORAGE, 'chatSessions')
NEW_SESSIONS_DIR = os.path.join(NEW_STORAGE, 'chatSessions')

KEY = 'chat.ChatSessionStore.index'


def check_vscode_running():
	"""VS Codeプロセスが起動中か確認"""
	try:
		result = subprocess.run(
			['tasklist', '/FI', 'IMAGENAME eq Code.exe', '/NH'],
			capture_output=True, text=True, timeout=10
		)
		if 'Code.exe' in result.stdout:
			return True
	except Exception:
		pass
	return False


def read_index(db_path, readonly=True):
	"""state.vscdbからチャットセッションインデックスを読み取る"""
	mode = 'ro' if readonly else 'rw'
	uri = f'file:{db_path}?mode={mode}'
	conn = sqlite3.connect(uri, uri=True)
	try:
		cur = conn.cursor()
		cur.execute("SELECT value FROM ItemTable WHERE key = ?", (KEY,))
		row = cur.fetchone()
		if not row:
			conn.close()
			return None, None
		data = json.loads(row[0])
		if readonly:
			conn.close()
			return data, None
		return data, conn
	except Exception:
		conn.close()
		raise


def main():
	print('=' * 60)
	print('  VS Code Copilot Chat セッション復旧ツール')
	print('=' * 60)
	print()

	# [1] VS Codeプロセス確認
	print('[1] VS Codeプロセス確認...')
	if check_vscode_running():
		print('  !! エラー: VS Code (Code.exe) が起動中です。')
		print('  !! VS Codeを完全に閉じてから再実行してください。')
		return 1
	print('  OK: VS Codeは起動していません。')
	print()

	# パスの存在確認
	for label, path in [('旧DB', OLD_DB), ('新DB', NEW_DB)]:
		if not os.path.exists(path):
			print(f'  !! エラー: {label}が見つかりません: {path}')
			return 1

	# [2] バックアップ
	print('[2] 新state.vscdbのバックアップ...')
	timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
	backup_path = os.path.join(BACKUP_DIR, f'state.vscdb.bak_{timestamp}')
	try:
		shutil.copy2(NEW_DB, backup_path)
		size = os.path.getsize(backup_path)
		print(f'  保存先: {backup_path}')
		print(f'  サイズ: {size:,} bytes')
	except Exception as e:
		print(f'  !! バックアップ失敗: {e}')
		return 1
	print()

	# [3] 旧DBの読み取り
	print('[3] 旧state.vscdb読み取り...')
	try:
		old_data, _ = read_index(OLD_DB, readonly=True)
	except sqlite3.OperationalError as e:
		print(f'  !! エラー: 旧DBを開けません（ロック中?）: {e}')
		return 1
	if old_data is None:
		print(f'  !! エラー: 旧DBにキー "{KEY}" が見つかりません。')
		return 1
	old_entries = old_data.get('entries', {})
	print(f'  セッション数: {len(old_entries)}')
	for sid, info in old_entries.items():
		print(f'    - {info.get("title", "N/A")[:70]}')
	print()

	# [4] 新DBの読み取り
	print('[4] 新state.vscdb読み取り...')
	try:
		new_data, conn_new = read_index(NEW_DB, readonly=False)
	except sqlite3.OperationalError as e:
		print(f'  !! エラー: 新DBを開けません（ロック中?）: {e}')
		return 1
	if new_data is None:
		if conn_new:
			conn_new.close()
		print(f'  !! エラー: 新DBにキー "{KEY}" が見つかりません。')
		return 1
	new_entries = new_data.get('entries', {})
	original_count = len(new_entries)
	print(f'  セッション数: {original_count}')
	print()

	# [5] マージ
	print('[5] インデックスマージ...')
	added_sessions = []
	for sid, entry in old_entries.items():
		if sid not in new_entries:
			new_entries[sid] = entry
			title = entry.get('title', 'N/A')
			added_sessions.append((sid, title))
			print(f'  + 追加: {title[:70]}')

	if not added_sessions:
		print('  追加対象なし（全セッション既に存在）')
		conn_new.close()
	else:
		print(f'  合計 {len(added_sessions)} セッション追加')
		print()

		# [6] 新DBに書き込み
		print('[6] 新state.vscdbに書き込み...')
		new_data['entries'] = new_entries
		updated_json = json.dumps(new_data, ensure_ascii=False)
		try:
			cur = conn_new.cursor()
			cur.execute("UPDATE ItemTable SET value = ? WHERE key = ?", (updated_json, KEY))
			conn_new.commit()
			conn_new.close()
			print('  書き込み完了')
		except Exception as e:
			conn_new.close()
			print(f'  !! 書き込み失敗: {e}')
			print(f'  !! バックアップから復元してください: {backup_path}')
			return 1
	print()

	# [7] chatSessionsファイルのコピー
	print('[7] chatSessionsファイル確認・コピー...')
	copied_files = []
	skipped_files = []
	failed_files = []

	if os.path.isdir(OLD_SESSIONS_DIR):
		if not os.path.isdir(NEW_SESSIONS_DIR):
			os.makedirs(NEW_SESSIONS_DIR, exist_ok=True)

		for filename in os.listdir(OLD_SESSIONS_DIR):
			old_file = os.path.join(OLD_SESSIONS_DIR, filename)
			new_file = os.path.join(NEW_SESSIONS_DIR, filename)

			if not os.path.isfile(old_file):
				continue

			if os.path.exists(new_file):
				skipped_files.append(filename)
				continue

			try:
				shutil.copy2(old_file, new_file)
				size = os.path.getsize(new_file)
				copied_files.append((filename, size))
				print(f'  コピー: {filename} ({size:,} bytes)')
			except Exception as e:
				failed_files.append((filename, str(e)))
				print(f'  !! 失敗: {filename} - {e}')
	else:
		print('  旧chatSessionsフォルダが見つかりません（スキップ）')

	if not copied_files and not failed_files:
		print('  コピー対象なし（全ファイル既に存在）')
	print()

	# [8] 整合性確認
	print('[8] 整合性確認...')
	# マージ後のインデックスを再読み取り
	verify_data, _ = read_index(NEW_DB, readonly=True)
	verify_entries = verify_data.get('entries', {})

	# インデックスのセッションIDからファイル名を推定
	# セッションIDの形式: "copilotcli:/xxxx" or "xxxx-xxxx-xxxx"
	index_file_ids = set()
	for sid in verify_entries.keys():
		# copilotcli:/ プレフィックスを除去してUUID部分を取得
		if sid.startswith('copilotcli:/'):
			raw_id = sid[len('copilotcli:/'):]
		else:
			raw_id = sid
		# untitled- プレフィックスも除去
		if raw_id.startswith('untitled-'):
			raw_id = raw_id[len('untitled-'):]
		index_file_ids.add(raw_id)

	# chatSessionsフォルダのファイル一覧
	session_files = set()
	if os.path.isdir(NEW_SESSIONS_DIR):
		for f in os.listdir(NEW_SESSIONS_DIR):
			if f.endswith('.jsonl'):
				session_files.add(f.replace('.jsonl', ''))

	# ファイルがあるがインデックスにないもの
	orphan_files = session_files - index_file_ids
	# インデックスにあるがファイルがないもの
	missing_files = index_file_ids - session_files

	print(f'  インデックスエントリ数: {len(verify_entries)}')
	print(f'  chatSessionsファイル数: {len(session_files)}')

	if orphan_files:
		print(f'  注意: ファイルのみ存在（インデックスなし）: {len(orphan_files)}件')
		for f in sorted(orphan_files):
			print(f'    {f}')
	if missing_files:
		print(f'  注意: インデックスのみ存在（ファイルなし）: {len(missing_files)}件')
		for f in sorted(missing_files):
			print(f'    {f}')

	if not orphan_files and not missing_files:
		print('  注意: インデックスとファイルのマッチング確認はベストエフォートです')
		print('        （copilotcli:/ 形式のセッションはファイルを持たない場合があります）')
	print()

	# [9] 結果レポート
	print('=' * 60)
	print('  復旧結果レポート')
	print('=' * 60)
	print()
	print(f'  旧DBセッション数:       {len(old_entries)}')
	print(f'  新DB(復旧前)セッション: {original_count}')
	print(f'  追加セッション数:       {len(added_sessions)}')
	print(f'  新DB(復旧後)セッション: {len(verify_entries)}')
	print()

	if added_sessions:
		print('  【追加されたセッション一覧】')
		for sid, title in added_sessions:
			print(f'    - {title[:70]}')
		print()

	print(f'  【chatSessionsファイル】')
	print(f'    コピー済み: {len(copied_files)}件')
	print(f'    既存(スキップ): {len(skipped_files)}件')
	print(f'    失敗: {len(failed_files)}件')
	if failed_files:
		for fname, err in failed_files:
			print(f'      !! {fname}: {err}')
	print()

	print(f'  バックアップ: {backup_path}')
	print()

	if len(added_sessions) > 0 or len(copied_files) > 0:
		print('  ★ 復旧完了。VS Codeを起動して確認してください。')
	else:
		print('  ★ 追加対象はありませんでした。既にマージ済みの可能性があります。')

	return 0


if __name__ == '__main__':
	try:
		code = main()
	except Exception as e:
		print(f'\n!! 予期しないエラー: {e}')
		import traceback
		traceback.print_exc()
		code = 1
	sys.exit(code)
