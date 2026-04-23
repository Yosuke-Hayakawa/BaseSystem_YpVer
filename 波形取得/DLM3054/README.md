# DLM3054HD

## 機器情報
- **機種**: YOKOGAWA DLM3054HD（4ch混合信号オシロスコープ）
- **シリアル**: 9031D7622
- **ファームウェア**: F1.21
- **ロジックプローブ**: 701988（PBL100 / 8bit）

## コマンドリファレンス
→ [自動制御.md](自動制御.md)（1033行、接続・チャンネル・トリガ・波形取得・ロジック等を網羅）

## ハマりポイント・ノウハウ

### USB接続タイプ
- **`TM_CTL_USBTMC2` を使うこと**
- `TM_CTL_USB`、`TM_CTL_USBTMC` では検出されない
- `TM_CTL_VISAUSB` でも検出可

### 本体側のUSBモード
- MISC → Remote Control → USB を **TMC** に変更必須
- 「Mass Storage」のままだと通信できない（USBメモリとして見えるだけ）
- モード変更後はUSBケーブルの抜き差しが必要な場合がある

### ロジックプローブ（701988）の閾値
- Bit0〜4を使用、閾値6V（6V以上=1、6V未満=0）
- 設定手順: （TODO: 確認後に追記）

## セットアップ手順
1. `ソフト/YTUSB2300.zip` を展開 → `Setup.exe` でUSBドライバインストール
2. DLM3054をUSB接続、デバイスマネージャーで認識確認
3. 本体でUSBモードを **TMC** に変更
4. `lib/` 内のtmctlLib.py + DLLでPythonから制御可能

## ファイル構成
```
DLM3054/
├── lib/            # 通信ライブラリ
│   ├── tmctlLib.py     # 横河公式Pythonラッパー
│   ├── tmctl64.dll     # 64bit用DLL
│   ├── tmctl.dll       # 32bit用DLL
│   ├── YKMUSB64.dll    # USB通信DLL(64bit)
│   └── YKMUSB.dll      # USB通信DLL(32bit)
├── 自動制御.md      # コマンドリファレンス（詳細）
├── 説明書/          # マニュアルPDF
│   ├── IMDLM3054HD-00JA.pdf    # ユーザーズマニュアル
│   ├── IMDLM3054HD-17JA.pdf    # 通信コマンドマニュアル
│   └── IM701988-01.pdf         # ロジックプローブマニュアル
├── ソフト/          # インストーラ等
│   ├── tmctl8020.zip    # TMCTLライブラリ
│   └── YTUSB2300.zip    # USBドライバ
└── README.md        # このファイル
```
