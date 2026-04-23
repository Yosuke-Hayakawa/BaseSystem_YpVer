# CANoe / VTシステム

CANoe、VTシステム、vTESTstudioに関するマニュアル・ツール集。  
VTシステムを使用したHILSテストにおけるCANoe/VT制御の参照資料。

## フォルダ構成

```
CANoe_VT/
├── README.md              # 本ファイル（マニュアル索引・概要）
├── sync_manuals.bat       # マニュアル同期バッチ（サーバーからコピー）
├── マニュアル/             # マニュアル本体（mdファイル群）
│   ├── *.md                  # CANoe/VT/CAPL/LIN/FDX関連マニュアル
│   ├── ユースケース観点表.csv  # ユースケース試験の観点一覧
│   └── CAPLヘルプ更新ソフト/  # CAPL関数リファレンス自動生成ツール
│       ├── capl_doc_gui.py
│       ├── extract_capl_all_functions.py
│       ├── CAPLヘルプ更新ソフト.bat
│       └── CAPL_Functions_Reference_20260415.md
└── scripts/               # CANoe/VT制御スクリプト（今後追加）
```

## マニュアルの同期方法

サーバー上のマニュアル原本からローカルにコピーする。

```bash
# プロジェクトルートから実行
CANoe_VT\sync_manuals.bat
```

**ソースパス**:  
`\\jikken-sv05\El\共通\05ソフトG\017_技術の棚入れ\格納先フォルダ\064_GithubCopilot手順書\VTシステムマニュアル.md\`

- マニュアルが追加・更新されたら `sync_manuals.bat` を再実行すれば差分コピーされる
- `__pycache__` と `.github` は同期対象外

---

## マニュアル索引（カテゴリ別）

### CANoe 基本操作

| マニュアル | ファイル名 | 備考 |
|-----------|-----------|------|
| CANoe/CANalyzer 基本操作 | `CANoeCANalyzer_基本操作_20230607.md` | ※ `canoe_basic.md` と同一内容 |
| テストレポートビューア | `CANoe_TestReportViewer_基本操作_20220317.md` | |
| 診断テスター・シミュレーションノード設定 | `CANoe_診断テスター・シミュレーションノード設定方法（CAN／DoIP）_20230511.md` | CAN/DoIP対応 |
| パフォーマンス測定・設定 | `CANoeCANalyzer_パフォーマンス測定、設定方法_20230711.md` | |

### CAPL（CAPLプログラミング）

| マニュアル | ファイル名 | 備考 |
|-----------|-----------|------|
| CAPL入門 | `For_Beginners_CAPL.md` | ※ `beg_capl.md` と同一内容 |
| CAPLクイックガイド | `CANoeCANalyzer_CAPLクイックガイド_20200219.md` | ※ `capl_quick.md` と同一内容 |
| CAPL関数リファレンス | `CAPL_Functions_Reference_20260414.md` | 約12MB。全関数網羅 |
| CAPL関数リファレンス（最新） | `CAPLヘルプ更新ソフト/CAPL_Functions_Reference_20260415.md` | 更新ソフトで生成した最新版 |

### LIN

| マニュアル | ファイル名 | 備考 |
|-----------|-----------|------|
| LIN設定・基本操作 | `CANoeCANalyzer.LIN_LIN設定方法_基本操作_20230418.md` | ※ `lin_basic.md` と同一内容 |
| LIN入門 | `For_Beginners_LIN.md` | |
| LDF Explorer操作 | `CANoeCANalyzer.LIN_LDF_Explorer_操作マニュアル_20180905.md` | |

### FDX（Fast Data Exchange）

| マニュアル | ファイル名 | 備考 |
|-----------|-----------|------|
| FDXプロトコル仕様 | `CANoe_FDX_Protocol_JP.md` | プロトコル定義書 |
| FDXエディター基本操作 | `CANoe_FDXエディター基本操作_20161202.md` | |
| FDX連携ガイド | `CANoe_FDX連携_20250826.md` | |
| Fast Data Exchange技術解説 | `AN-AND-1-119_Fast_Data_Exchange_with_CANoe.md` | アプリノート |

### vTESTstudio

| マニュアル | ファイル名 | 備考 |
|-----------|-----------|------|
| vTESTstudio入門 | `vTESTstudio_for_Beginners.md` | |
| 基本操作 | `vTESTstudio+-+基本操作 (1).md` | |
| コマンド逆引きテクニック集 | `vTESTstudio+-+コマンド逆引きテクニック集 (1).md` | |
| 効率的な操作方法（中級編） | `vTESTstudio　効率的な操作方法（中級編） (1).md` | |

### VTシステム（ハードウェア）

| マニュアル | ファイル名 | 備考 |
|-----------|-----------|------|
| VTシステム概要 | `VTシステム-概要.md` | まずこれを読む |
| 製品ラインナップ | `VTシステム-製品ラインナップ.md` | |
| ハードウェアセットアップ | `VTシステム+-+ハードウェア+セットアップ.md` | |
| VTシステムマニュアル（日本語） | `VTSystem_Manual_JP.md` | 約470KB。包括的リファレンス |
| アドバンストマニュアル | `VTsystem_アドバンストマニュアル_20251029.md` | 上級設定 |
| VT2710初期設定 | `VTシステム_CANoe.Sensor_VT2710の初期設定.md` | CANoe.Sensor連携 |

### その他

| マニュアル | ファイル名 | 備考 |
|-----------|-----------|------|
| CANdb++ 基本操作 | `CANdb＋＋_+基本操作_20191015.md` | データベースエディター |
| ライセンスクライアント | `UserManual_LicenseClient_20240508.md` | |
| VJ Contents | `VJcontents.md` | Vector Japan コンテンツ |
| ユースケース観点表 | `ユースケース観点表.csv` | ユースケース試験（試験21）の観点一覧 |

---

## 短縮名エイリアス（同一内容ファイル）

以下のファイルはサイズが完全に一致しており、内容が同一と推定される。  
短縮名はクイックアクセス用。正式名の方がバージョン日付を含むため推奨。

| 短縮名 | 正式名 | サイズ |
|--------|--------|--------|
| `canoe_basic.md` | `CANoeCANalyzer_基本操作_20230607.md` | 436KB |
| `beg_capl.md` | `For_Beginners_CAPL.md` | 75KB |
| `capl_quick.md` | `CANoeCANalyzer_CAPLクイックガイド_20200219.md` | 42KB |
| `lin_basic.md` | `CANoeCANalyzer.LIN_LIN設定方法_基本操作_20230418.md` | 122KB |

---

## CAPLヘルプ更新ソフト

`マニュアル/CAPLヘルプ更新ソフト/` にあるPythonツール。  
CANoeのCAPLヘルプから全関数情報を抽出し、Markdownリファレンスを自動生成する。

| ファイル | 説明 |
|---------|------|
| `extract_capl_all_functions.py` | CAPL関数情報抽出スクリプト |
| `capl_doc_gui.py` | GUI版 |
| `CAPLヘルプ更新ソフト.bat` | バッチラッパー |
| `CAPL_Functions_Reference_20260415.md` | 生成されたリファレンス（最新版） |

---

## 注意事項

- マニュアルはPDFからMarkdownに変換されたもの。レイアウト崩れや画像欠落がある場合がある
- もし図を参照しなければ判断できない場合は、その旨を伝えること
- `CAPL_Functions_Reference` は約12MBあるため、全文読み込みは非推奨。必要な関数名で検索すること
- 「じか線」は社内用語で、ECUに繋がる入出力（スイッチ入力、センサー入力、モーター出力等）を指す
