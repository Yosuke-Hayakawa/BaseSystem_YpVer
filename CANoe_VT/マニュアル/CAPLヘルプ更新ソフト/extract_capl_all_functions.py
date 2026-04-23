# -*- coding: utf-8 -*-
"""
CAPLヘルプ更新ソフト - 変換エンジン
CANoeヘルプのHTMLファイルをMarkdownに変換する。
GUI(capl_doc_gui.py)から呼ばれる他、単体でも実行可。
"""
import os, sys, re, glob, datetime
from html.parser import HTMLParser

# ==================================================
# 設定値（変更するならここ）
# ==================================================

# CAPLFunctionsフォルダへの相対パス（CANoeバージョンに依存しない部分）
_CAPL_FUNCTIONS_REL = r"Content\Topics\CAPLFunctions"

def _find_canoe_help_base():
    """
    CANoeのCAPLFunctionsフォルダを自動検出する。
    Program Files内の 'Vector CANoe*' フォルダを走査し、
    バージョン番号が最も大きいものを採用する。
    """
    search_roots = [
        os.environ.get("ProgramFiles", r"C:\Program Files"),
        os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
    ]
    candidates = []
    for root in search_roots:
        if not os.path.isdir(root):
            continue
        for entry in os.listdir(root):
            if entry.lower().startswith("vector canoe"):
                full = os.path.join(root, entry)
                if os.path.isdir(full):
                    candidates.append(full)
    if not candidates:
        return None
    # バージョン番号が大きい＝新しいCANoeを優先（フォルダ名でソート）
    candidates.sort(reverse=True)
    for canoe_dir in candidates:
        # Help** フォルダを探す（Help81, Help90 等）
        for item in sorted(os.listdir(canoe_dir), reverse=True):
            if item.lower().startswith("help") and os.path.isdir(os.path.join(canoe_dir, item)):
                # その中の CANoeDEFamilyHTML5 を探す
                for sub in os.listdir(os.path.join(canoe_dir, item)):
                    if "HTML5" in sub:
                        capl_path = os.path.join(canoe_dir, item, sub, _CAPL_FUNCTIONS_REL)
                        if os.path.isdir(capl_path):
                            return capl_path
    return None

# 自動検出を試みる（見つからなければNone → GUI側で手動選択）
CANOE_HELP_BASE = _find_canoe_help_base()

def _find_target_folders(base_path):
    """
    CAPLFunctionsフォルダ直下のサブフォルダを自動列挙する。
    固定リストではなく、実際に存在するフォルダを全て対象にする。
    """
    if not base_path or not os.path.isdir(base_path):
        return []
    folders = []
    for entry in sorted(os.listdir(base_path)):
        full = os.path.join(base_path, entry)
        if os.path.isdir(full):
            folders.append(entry)
    return folders

# フォルダも自動列挙（CANOE_HELP_BASEが見つかっていれば）
TARGET_FOLDERS = _find_target_folders(CANOE_HELP_BASE)

# 出力ファイル名のプレフィックス（日付が後ろに付く）
OUTPUT_PREFIX = "CAPL_Functions_Reference"


# ==================================================
# HTML → Markdown 変換パーサー
# ==================================================
class ContentExtractor(HTMLParser):
    """
    HTMLタグを読み取り、Markdown形式のテキストに変換する。
    HTMLParserを継承し、タグの開始/終了/テキストを検出するたびに
    対応するMarkdown記号をcontentリストに追加する仕組み。
    """

    def __init__(self):
        super().__init__()
        self.content = []           # 変換結果を溜めるリスト
        self.current_tag = None     # 今処理中のHTMLタグ名
        self.in_body = False        # <body>の中にいるか

        # 読み飛ばすタグ（表示に不要なもの）
        self.skip_tags = {'script', 'style', 'nav', 'footer', 'header'}
        # 見出しタグ
        self.heading_tags = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}

        self.list_depth = 0         # <ul>/<ol>のネストの深さ
        self.in_table = False       # テーブルの中か
        self.table_row = []         # 現在行のセルデータ
        self.table_data = []        # テーブル全体のデータ
        self.in_pre = False         # <pre>の中か
        self.in_code = False        # <code>の中か
        self.skip_content = False   # スキップ中か

    # --- 開きタグを見つけたとき ---
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        if tag == 'body':
            self.in_body = True
        elif tag in self.skip_tags:
            self.skip_content = True       # script等の中身は無視
        elif tag in self.heading_tags:
            # <h1>→ "# ", <h2>→ "## ", ...
            self.content.append('\n' + '#' * int(tag[1]) + ' ')
        elif tag == 'p':
            self.content.append('\n\n')  # 段落 = 空行
        elif tag == 'br':
            self.content.append('\n')     # 改行
        elif tag == 'li':
            # リスト項目: ネストに応じてインデント
            self.content.append('\n' + '  ' * self.list_depth + '- ')
        elif tag in ('ul', 'ol'):
            self.list_depth += 1
        elif tag == 'pre':
            self.in_pre = True
            self.content.append('\n```\n')  # コードブロック開始
        elif tag == 'code' and not self.in_pre:
            self.in_code = True
            self.content.append('`')          # インラインコード
        elif tag == 'table':
            self.in_table = True
            self.table_data = []
        elif tag == 'tr':
            self.table_row = []
        elif tag in ('strong', 'b'):
            self.content.append('**')          # 太字
        elif tag in ('em', 'i'):
            self.content.append('*')           # 斜体

    # --- 閉じタグを見つけたとき ---
    def handle_endtag(self, tag):
        if tag == 'body':
            self.in_body = False
        elif tag in self.skip_tags:
            self.skip_content = False
        elif tag in ('ul', 'ol'):
            self.list_depth = max(0, self.list_depth - 1)
        elif tag == 'pre':
            self.in_pre = False
            self.content.append('\n```\n')
        elif tag == 'code' and not self.in_pre:
            self.in_code = False
            self.content.append('`')
        elif tag == 'table':
            self.in_table = False
            if self.table_data:
                self._format_table()           # テーブルをMarkdown化
        elif tag == 'tr':
            if self.table_row:
                self.table_data.append(self.table_row)
        elif tag in ('strong', 'b'):
            self.content.append('**')
        elif tag in ('em', 'i'):
            self.content.append('*')
        self.current_tag = None

    # --- タグの中のテキストを見つけたとき ---
    def handle_data(self, data):
        if not self.in_body or self.skip_content:
            return
        if self.in_table and self.current_tag in ('td', 'th'):
            self.table_row.append(data.strip())         # テーブルセルに追加
        elif self.in_pre:
            self.content.append(data)                    # コードはそのまま
        else:
            text = re.sub(r'\s+', ' ', data)            # 空白を正規化
            if text.strip():
                self.content.append(text)

    # --- 蓄積したテーブルデータをMarkdown表に変換 ---
    def _format_table(self):
        if not self.table_data:
            return
        mc = max(len(r) for r in self.table_data)
        for r in self.table_data:
            while len(r) < mc:
                r.append('')     # 列数を揃える
        self.content.append('\n\n| ' + ' | '.join(self.table_data[0]) + ' |\n')
        self.content.append('|' + '---|' * mc + '\n')   # 区切り線
        for r in self.table_data[1:]:
            self.content.append('| ' + ' | '.join(r) + ' |\n')
        self.content.append('\n')

    # --- 変換結果を文字列として取得 ---
    def get_content(self):
        t = ''.join(self.content)
        return re.sub(r'\n{3,}', '\n\n', t).strip()  # 過剰な空行を削減


# ==================================================
# ユーティリティ関数
# ==================================================

def extract_html_content(filepath):
    """単一のHTMLファイルを読み込み、Markdownに変換して返す。"""
    try:
        # 文字コードを自動判定（複数試す）
        for enc in ['utf-8', 'utf-8-sig', 'cp932', 'shift_jis', 'latin-1']:
            try:
                with open(filepath, 'r', encoding=enc) as fh:
                    html = fh.read()
                break
            except UnicodeDecodeError:
                continue
        else:
            return None   # どの文字コードでも読めなかった

        p = ContentExtractor()
        p.feed(html)
        return p.get_content()
    except Exception as e:
        print(f"  エラー: {filepath}: {e}")
        return None


def get_function_name_from_file(fn):
    """ファイル名からCAPL関数名を推測する。"""
    n = fn.replace('.htm', '').replace('.html', '')
    if n.startswith('CAPLfunction'):
        n = n[12:]
    elif n.startswith('CAPLfunctions'):
        n = n[13:]
    return n


def extract_folder_content(folder_path, folder_name):
    """フォルダ内の全HTMファイルを探して変換し、エントリのリストを返す。"""
    ac = []
    if not os.path.exists(folder_path):
        print(f"  フォルダが見つかりません: {folder_path}")
        return []

    # .htm / .html を再帰的に収集
    hf = []
    for root, dirs, files in os.walk(folder_path):
        for ff in files:
            if ff.endswith('.htm') or ff.endswith('.html'):
                hf.append(os.path.join(root, ff))

    print(f"  {folder_name}: {len(hf)} ファイル検出")

    # 、1ファイルずつ変換
    for i, fp in enumerate(sorted(hf)):
        fn = os.path.basename(fp)
        name = get_function_name_from_file(fn)
        c = extract_html_content(fp)
        if c:
            rp = os.path.relpath(fp, folder_path)
            sf = os.path.dirname(rp) if os.path.dirname(rp) else ""
            ac.append({'name': name, 'filename': fn, 'subfolder': sf, 'content': c})
        # 25%ごとに進捗表示
        if (i + 1) % max(1, len(hf) // 4) == 0:
            print(f"    進捗: {i+1}/{len(hf)}")

    return ac


# ==================================================
# 出力ファイル名の組み立て・旧ファイル削除
# ==================================================

def build_output_path(output_dir):
    """
    出力ファイルのフルパスを生成する。
    既存の同名プレフィックスファイルがあれば削除してから新しい名前を返す。
    ファイル名例: CAPL_Functions_Reference_20260413.md
    """
    today = datetime.date.today().strftime('%Y%m%d')
    new_name = f"{OUTPUT_PREFIX}_{today}.md"
    new_path = os.path.join(output_dir, new_name)

    # 旧日付のファイルを削除（同じプレフィックスのものを探す）
    pattern = os.path.join(output_dir, f"{OUTPUT_PREFIX}_*.md")
    for old in glob.glob(pattern):
        if old != new_path:
            os.remove(old)
            print(f"  旧ファイルを削除しました: {os.path.basename(old)}")

    return new_path


# ==================================================
# Markdownドキュメント書き出し
# ==================================================

def create_markdown_document(all_data, output_path):
    """全データを1つのMarkdownファイルに書き出す。"""
    today_str = datetime.date.today().strftime('%Y/%m/%d')

    with open(output_path, 'w', encoding='utf-8') as f:
        # --- ヘッダー ---
        f.write(f"# CAPL関数リファレンス\n\n")
        f.write(f"CANoeヘルプドキュメントから抽出\n\n")
        f.write(f"更新日: {today_str}\n\n---\n\n")

        # --- 目次 ---
        f.write(f"## 目次\n\n")
        for fn, ent in all_data.items():
            f.write(f"### {fn}\n\n")
            for e in ent[:20]:
                a = e['name'].replace(' ', '-').replace('/', '-')
                f.write(f"- [{e['name']}](#{a})\n")
            if len(ent) > 20:
                f.write(f"- ... 他 {len(ent)-20} 項目\n")
            f.write("\n")
        f.write("\n---\n\n")

        # --- 各カテゴリの本文 ---
        for fn, ent in all_data.items():
            f.write(f"# {fn}\n\n")
            sfs = {}
            for e in ent:
                s = e['subfolder'] or 'General'
                sfs.setdefault(s, []).append(e)
            for sn, se in sfs.items():
                if sn != 'General':
                    f.write(f"## {sn}\n\n")
                for e in se:
                    f.write(f"### {e['name']}\n\n{e['content']}\n\n---\n\n")

        tc = sum(len(v) for v in all_data.values())
        print(f"\n\u2713 完了: {tc} 項目を出力しました")
        print(f"  出力ファイル: {output_path}")


# ==================================================
# メイン関数（単体実行用）
# ==================================================

def main():
    print("=" * 60)
    print("CAPLヘルプ更新ソフト")
    print("=" * 60)

    if not CANOE_HELP_BASE:
        print("エラー: CANoeのヘルプフォルダが見つかりませんでした")
        print("  CANoeがインストールされているか確認してください")
        sys.exit(1)

    if not TARGET_FOLDERS:
        print(f"エラー: CAPLFunctionsフォルダ内にサブフォルダがありません")
        print(f"  パス: {CANOE_HELP_BASE}")
        sys.exit(1)

    print(f"  検出パス: {CANOE_HELP_BASE}")
    print(f"  対象フォルダ: {len(TARGET_FOLDERS)} 件")

    # 出力先 = このスクリプトと同じフォルダ
    script_dir = os.path.dirname(os.path.abspath(__file__))
    of = build_output_path(script_dir)

    ad = {}
    for fn in TARGET_FOLDERS:
        fp = os.path.join(CANOE_HELP_BASE, fn)
        print(f"\n処理中: {fn}")
        ent = extract_folder_content(fp, fn)
        if ent:
            ad[fn] = ent

    if ad:
        create_markdown_document(ad, of)
    else:
        print(f"エラー: 抽出できるコンテンツがありませんでした")


if __name__ == "__main__":
    main()
