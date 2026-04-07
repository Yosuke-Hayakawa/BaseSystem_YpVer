# cramas-analysis

CRAMAS HILSテストの解析・開発・技術調査プロジェクト。

> **初めての方は → [QUICKSTART.md](QUICKSTART.md)**

## フォルダ構成

```
cramas-analysis/
├── 仕様書/                  # 仕様書リンク集・リファレンスドキュメント
│   ├── README.md               # 各仕様書の説明とリンク
│   └── CRAMAS共通リファレンス.md    # CRAMAS共通技術（XFileConv、CSV列構成等）
│
├── 波形解析/                # NG波形解析ツール・データ
│   ├── README.md               # スクリプト説明・使い方
│   ├── scripts/                # 解析スクリプト群
│   │   ├── project_config.py      # プロジェクト設定ローダー
│   │   ├── ng_check.py            # NG判定チェック
│   │   ├── dat_to_csv.py          # dat→CSV一括変換
│   │   ├── extract_anomaly.py     # 異常値抽出
│   │   ├── wave_viewer.py         # CSV波形ビューア
│   │   └── 波形ビューア起動.bat
│   ├── projects/<製品名>/       # 製品別プロジェクト
│   │   ├── config.yaml            # 製品固有設定（NG番号、カラム名等）
│   │   ├── docs/                  # 製品固有リファレンス
│   │   ├── output/                # NG解析結果レポート
│   │   ├── data/                  # ログデータ（.gitignore）
│   │   └── 要解析/                # 特異パターンデータ（.gitignore）
│   └── NG解析.bat              # ng_check.pyバッチラッパー
│
├── 波形取得/                # オシロスコープ自動操作・画面キャプチャ
│   ├── README.md               # スクリプト説明・SCPIコマンド
│   ├── capture_screen.py       # 画面キャプチャ（汎用）
│   ├── 画面取得.bat            # capture_screen.pyバッチラッパー
│   └── 画像ファイル/           # キャプチャ画像（.gitignore）
│
├── UF作成/                  # ユーザーファンクション作成・CRAMAS制御
│   └── README.md               # uf.c/uf.hルール、ボード構成、ioset.ios等
│
├── ツール/                  # プロジェクト横断の便利ツール
│   ├── README.md               # ツール説明
│   └── restore_chat_sessions.py  # VS Code会話復旧ツール
│
├── mcp/                     # MCPサーバー（画像閲覧機能）
│   ├── README.md
│   └── mcp_image_server.py
│
├── 一時/                    # 中間ファイル・バックアップ（.gitignore対象）
│
├── .github/
│   ├── agents/              # IMFエージェント（AIチーム）
│   └── copilot-instructions.md # プロジェクト設定
│
├── .vscode/mcp.json         # MCPサーバー設定
├── .gitignore
├── README.md
├── QUICKSTART.md
└── メインワークスペース.code-workspace
```

## プロジェクト構成

製品ごとに `波形解析/projects/<製品名>/` フォルダを作り、`config.yaml` で固有設定を管理する。

```bash
# 特定プロジェクトを指定して解析
python scripts/ng_check.py --project 919D

# プロジェクトが1つだけなら自動検出
python scripts/ng_check.py
```

> **`919D/` はテンプレート（見本）として同梱。** 新プロジェクト作成方法は [波形解析/projects/README.md](波形解析/projects/README.md) を参照。

## データファイルについて

以下はサイズが大きいためGit管理外（.gitignore）。

| データ | 配置先 |
|--------|--------|
| ログデータ | `波形解析/projects/<製品名>/data/` |
| 解析結果 | `波形解析/projects/<製品名>/output/` |
| キャプチャ画像 | `波形取得/画像ファイル/` |

## セットアップ

```bash
pip install pandas pyyaml pyvisa pyvisa-py fastmcp PySide6 pyqtgraph
```
