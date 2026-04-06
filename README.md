# cramas-analysis

CRAMAS HILSテストの解析・開発・技術調査プロジェクト。

## フォルダ構成

```
cramas-analysis/
├── 仕様書/                  # 仕様書リンク集・リファレンスドキュメント
│   ├── README.md               # 各仕様書の説明とリンク
│   ├── 919D照合ECUリファレンス.md   # 919D固有情報（NG番号、テスト手順等）
│   └── CRAMAS共通リファレンス.md    # CRAMAS共通技術（XFileConv、CSV列構成等）
│
├── 波形解析/                # NG波形解析ツール・データ
│   ├── README.md               # スクリプト説明・使い方
│   ├── scripts/                # 解析スクリプト群
│   │   ├── ng_check.py            # NG判定チェック
│   │   ├── dat_to_csv.py          # dat→CSV一括変換
│   │   ├── extract_anomaly.py     # 異常値抽出
│   │   ├── wave_viewer.py         # CSV波形ビューア
│   │   └── 波形ビューア起動.bat
│   ├── 波形取得/               # オシロスコープ自動操作
│   ├── projects/919D/          # 919Dプロジェクト
│   │   ├── output/                # NG解析結果レポート
│   │   └── data/                  # ログデータ（.gitignore）
│   └── NG解析.bat              # ng_check.pyバッチラッパー
│
├── UF作成/                  # ユーザーファンクション作成・CRAMAS制御
│   └── README.md               # uf.c/uf.hルール、ボード構成、ioset.ios等【全情報】
│
├── mcp/                     # MCPサーバー（画像閲覧機能）
│   ├── README.md
│   └── mcp_image_server.py
│
├── 一時/                    # 中間ファイル・バックアップ（.gitignore対象）
│
├── .github/
│   ├── agents/              # IMFエージェント（AIチーム）
│   │   ├── phillips.agent.md   # チームリーダー (Kingpin)
│   │   ├── cole.agent.md       # フィールドエージェント (Shadow)
│   │   ├── barnes.agent.md     # テクニカルスペシャリスト (Doc)
│   │   └── volkova.agent.md    # コントローラー (Siren)
│   └── copilot-instructions.md # プロジェクト設定
│
├── .vscode/mcp.json         # MCPサーバー設定
├── .gitignore
├── README.md
└── メインワークスペース.code-workspace
```

## データファイルについて

以下はサイズが大きいためGit管理外。

| データ | 配置先 | サイズ | 内容 |
|--------|--------|--------|------|
| ログデータ | `波形解析/projects/919D/data/ログデータ/` | 138GB | CRAMASの.datファイル（約2万件） |
| OKファイル | `波形解析/projects/919D/data/OKファイル/` | 636MB | 参照用OK波形 |
| 画像ファイル | `波形解析/波形取得/画像ファイル/` | 2.3MB | オシロキャプチャPNG |
| 要解析 | `波形解析/projects/919D/要解析/` | 11MB | 未解析NGデータ |

## 関連フォルダ（ローカル）

| パス | 用途 |
|------|------|
| `C:\simbase\simdat\919D_照合ECU\` | CRAMASプロジェクト本体（uf.c/uf.h） |
| `C:\いろいろ\一時置き\照合資料\` | 仕様書類 |

## セットアップ

```bash
pip install pyvisa pyvisa-py fastmcp
```
