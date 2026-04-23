# -*- coding: utf-8 -*-
"""
CAPLヘルプ更新ソフト - GUI
ボタンを押すだけでMarkdownファイルを出力/更新する。
内部で extract_capl_all_functions.py の関数を呼び出す。
"""
import os
import tkinter as tk
from tkinter import messagebox, filedialog
import threading

# 変換エンジンから必要な関数をインポート
from extract_capl_all_functions import (
    CANOE_HELP_BASE,
    TARGET_FOLDERS,
    extract_folder_content,
    create_markdown_document,
    build_output_path,
    _find_target_folders,
)


class App:
    """GUIウィンドウ本体。"""

    def __init__(self):
        # --- 現在のCANoeパスと対象フォルダ ---
        self.help_base = CANOE_HELP_BASE
        self.target_folders = list(TARGET_FOLDERS)

        # --- ウィンドウ作成 ---
        self.root = tk.Tk()
        self.root.title("CAPLヘルプ更新ソフト")
        self.root.geometry("520x340")
        self.root.resizable(False, False)

        # --- タイトル ---
        tk.Label(
            self.root, text="CAPLヘルプ更新ソフト",
            font=("Meiryo UI", 14, "bold"),
        ).pack(pady=(20, 5))

        # --- 説明文 ---
        tk.Label(
            self.root, text="ボタンを押すとCAPLに関するMarkdownファイルを出力/更新します",
            font=("Meiryo UI", 9),
        ).pack()

        # --- CANoeパス表示 ---
        path_text = self.help_base if self.help_base else "未検出（実行時に手動選択）"
        self.path_var = tk.StringVar(value=f"参照先: {path_text}")
        tk.Label(
            self.root, textvariable=self.path_var,
            font=("Meiryo UI", 8), fg="gray",
        ).pack(pady=(5, 0))

        # --- 実行ボタン ---
        self.btn = tk.Button(
            self.root, text="CAPL Markdown 出力",
            font=("Meiryo UI", 12, "bold"),
            width=20, height=2,
            command=self._on_click,
        )
        self.btn.pack(pady=15)

        # --- ステータス行（処理中/完了 等） ---
        self.status_var = tk.StringVar(value="待機中")
        self.status_label = tk.Label(
            self.root, textvariable=self.status_var,
            font=("Meiryo UI", 10), fg="gray",
        )
        self.status_label.pack()

        # --- 出力ファイル名表示行 ---
        self.file_var = tk.StringVar(value="")
        self.file_label = tk.Label(
            self.root, textvariable=self.file_var,
            font=("Meiryo UI", 9), fg="gray",
        )
        self.file_label.pack(pady=(5, 0))

    # --- ボタン押下時 ---
    def _on_click(self):
        # パスが未検出 or 存在しない場合は手動選択
        if not self.help_base or not os.path.isdir(self.help_base):
            messagebox.showinfo(
                "CANoeヘルプが見つかりません",
                "CANoeのCAPLFunctionsフォルダを手動で選択してください。\n\n"
                "例: C:\\Program Files\\Vector CANoe Family 18\\Help81\\"
                "CANoeDEFamilyHTML5\\Content\\Topics\\CAPLFunctions"
            )
            selected = filedialog.askdirectory(title="CAPLFunctionsフォルダを選択")
            if not selected:
                return
            self.help_base = selected
            self.target_folders = _find_target_folders(selected)
            self.path_var.set(f"参照先: {selected}")
            if not self.target_folders:
                messagebox.showerror("エラー", "選択したフォルダにサブフォルダがありません。")
                return

        self.btn.config(state=tk.DISABLED)         # 二重押し防止
        self.status_var.set("処理中...")
        self.status_label.config(fg="blue")
        self.file_var.set("")
        # 重い処理を裏スレッドで実行（UIフリーズ防止）
        threading.Thread(target=self._run, daemon=True).start()

    # --- バックグラウンド処理 ---
    def _run(self):
        try:
            # 出力先 = このスクリプトと同じフォルダ
            script_dir = os.path.dirname(os.path.abspath(__file__))
            of = build_output_path(script_dir)

            ad = {}
            tf = len(self.target_folders)
            for i, fn in enumerate(self.target_folders, 1):
                self._update_status(f"処理中... ({i}/{tf}) {fn}")
                fp = os.path.join(self.help_base, fn)
                ent = extract_folder_content(fp, fn)
                if ent:
                    ad[fn] = ent

            if ad:
                create_markdown_document(ad, of)
                total = sum(len(v) for v in ad.values())
                out_name = os.path.basename(of)
                self._finish(True,
                    f"完了: {total} 項目を出力しました\n{of}",
                    out_name)
            else:
                self._finish(False, "抽出できるコンテンツがありませんでした", "")
        except Exception as e:
            self._finish(False, f"エラー: {e}", "")

    # --- ステータス更新（スレッド安全） ---
    def _update_status(self, text):
        self.root.after(0, lambda: self.status_var.set(text))

    # --- 完了/エラー処理 ---
    def _finish(self, success, msg, out_name):
        def _do():
            self.btn.config(state=tk.NORMAL)       # ボタン再有効化
            if success:
                self.status_var.set("完了")
                self.status_label.config(fg="green")
                self.file_var.set(f"出力ファイル: {out_name}")
                self.file_label.config(fg="black")
                messagebox.showinfo("完了", msg)
            else:
                self.status_var.set("エラー")
                self.status_label.config(fg="red")
                messagebox.showerror("エラー", msg)
        self.root.after(0, _do)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    App().run()
