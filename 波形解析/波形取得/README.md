# 波形取得 — オシロスコープ自動操作

Tektronix MSO22/MSO24をUSB経由でPythonから自動操作し、画面キャプチャやトリガ変更を行う。

## 機器情報

- **対象機器**: Tektronix 2シリーズ MSO (MSO22 / MSO24)
- **接続**: USB TMC (Test & Measurement Class)
- **制御**: pyvisa + SCPIコマンド
- **説明書**: `説明書/テクトロ_2シリーズ/` にコマンドリスト・メインマニュアルあり

## 前提条件

- Python 3.12以上
- `pip install pyvisa pyvisa-py`（またはNI-VISAドライバ）
- オシロとPCをUSBケーブルで接続

## スクリプト一覧

| スクリプト | 用途 |
|-----------|------|
| `capture_screen.py` | 画面キャプチャ（汎用） |
| `capture_lin_ids.py` | LIN IDを順番に切替えて連続キャプチャ |
| `capture_eig.py` | EIG1S01(0x22)単体キャプチャ |
| `capture_igon_rest.py` | IG ON状態で残りフレームをキャプチャ |
| `画面取得.bat` | capture_screen.pyのバッチラッパー |

### capture_screen.py（基本）

単純に今の画面をキャプチャしてPNG保存する。

```
python capture_screen.py              # 自動検出
python capture_screen.py "USB::..."   # VISAアドレス指定
```

- 保存先: スクリプトと同じフォルダ
- ファイル名: `screen_YYYYMMDD_HHMMSS.png`

### capture_lin_ids.py（LIN連続キャプチャ）

LINバスのトリガIDを順番に変更し、各フレームの画面を自動キャプチャする。

- LINバス番号は自動検出（B1〜B4を順に確認）
- トリガ条件を`IDentifier`に設定し、IDを6bitバイナリ文字列で指定
- 各ID変更後2秒待ってからキャプチャ（トリガがかかるのを待つ）

### capture_eig.py / capture_igon_rest.py（追加キャプチャ）

特定条件での追加撮影用。LINバスはB1固定。終了時にトリガを0x33に復帰する。

## SCPIコマンド — よく使うもの

### 接続・基本

```python
rm = pyvisa.ResourceManager()
inst = rm.open_resource("USB::0x0699::...")
inst.timeout = 60000  # 60秒（画面保存は時間がかかる）
idn = inst.query("*IDN?")  # 機器情報
inst.query("*OPC?")  # 直前コマンドの完了待ち
```

### 画面キャプチャ

```python
# オシロ内部に一時PNG保存 → PC側に読み出し → オシロ上の一時ファイル削除
inst.write('SAVe:IMAGe "C:/temp_cap.png"')
inst.query("*OPC?")
inst.write('FILESystem:READFile "C:/temp_cap.png"')
img_data = inst.read_raw()
inst.write('FILESystem:DELEte "C:/temp_cap.png"')
```

**注意**: `SAVe:IMAGe`はオシロ内部ストレージにファイルを作る。直接PCに転送する方法はないため、一時ファイル経由が必須。

### バス設定の確認

```python
# バスタイプ確認（LIN/CAN/SPI等）
bus_type = inst.query("BUS:B1:TYPe?")

# LIN IDフォーマット確認
id_format = inst.query("BUS:B1:LIN:IDFORmat?")
```

### LINトリガ設定

```python
# トリガ条件をID一致に設定
inst.write("TRIGger:A:BUS:B1:LIN:CONDition IDentifier")

# LIN IDを6bitバイナリ文字列で指定（0x33 = 110011）
inst.write('TRIGger:A:BUS:B1:LIN:IDentifier:VALue "110011"')
inst.query("*OPC?")
```

## LIN ID — 6bitバイナリ変換表

LINのFrame IDは6bitで指定する（SCPIコマンドではバイナリ文字列）。

| フレーム名 | Frame ID | 6bitバイナリ | 用途 |
|-----------|----------|-------------|------|
| EIG1S01 | 0x22 | 100010 | 電源制御 |
| IDT1S01 | 0x30 | 110000 | ID-BOX→照合ECU |
| IDB1S01 | 0x31 | 110001 | ID-BOX→照合ECU |
| STL1S01 | 0x33 | 110011 | 照合ECU→ステロク |
| ID-BOX系@ | 0x35 | 110101 | 照合ECU→ID-BOX |
| RS系@ | 0x36 | 110110 | 照合ECU→RS |
| ID-BOX系A | 0x39 | 111001 | ID-BOX→照合ECU |
| ID-BOX系B | 0x3A | 111010 | 照合ECU→ID-BOX |
| ID-BOX系C | 0x34 | 110100 | ID-BOX→照合ECU |

## 測定ノウハウ

### オシロ接続時の注意

- USBケーブルは直結すること（ハブ経由だと`pyvisa`が検出失敗する場合がある）
- オシロの電源投入後、USB認識まで数秒かかる。スクリプト実行前に認識を確認
- `inst.timeout = 60000`（60秒）は必須。画面保存コマンドは応答に数秒かかる

### LIN波形測定のコツ

- **トリガ変更後は2秒以上待つ**: ID変更直後にキャプチャすると、前のIDの波形が写る場合がある
- **測定終了後はトリガを元に戻す**: 手動操作に戻った時に混乱しないよう、0x33（STL1S01）に復帰させる
- **LINバス番号の確認**: オシロのバス設定でLINが何番に割り当てられているか、スクリプト実行前に確認。`capture_lin_ids.py`は自動検出するが、`capture_eig.py`等はB1固定

### IG状態別の測定

919D照合ECUのLIN通信はIG状態で挙動が変わる。

| IG状態 | LIN通信 | 備考 |
|--------|---------|------|
| OFF（Sleep） | 停止 | LINフレームは流れない |
| IG ON（エンジンOFF） | 一部動作 | EIG1S01, IDB1S01, IDT1S01等が流れる |
| エンジンON | フル動作 | 全フレームが流れる |

- Sleep状態ではLINトリガがかからないため、キャプチャしても無意味
- IG ON / エンジンONで撮り分けることで、状態依存の通信有無が確認できる

### ファイル命名規則

スクリプトの出力ファイル名は状態が分かるように命名されている。

```
{状態}_{フレーム名}_{ID}_{タイムスタンプ}.png
```

例:
- `engON_STL1S01_0x33_20260320_193729.png` — エンジンON時のSTL1S01
- `igON_IDB1S01_0x31_20260320_194700.png` — IG ON時のIDB1S01

### 画像の確認方法

自作MCPサーバーで直接確認できる（VS Code + Copilot Chat）。

```
list_images("C:\Users\CARAMAS4\Desktop\919D_CRAMAS自動結果解析\波形取得")
view_image("C:\...\engON_STL1S01_0x33_20260320_193729.png")
```

詳細は `919D_CRAMAS自動結果解析/scripts/mcp_image_server.py` を参照。

## LINバス設定（B1）— 重要設定値

オシロでLINデコードを有効にするには、以下3つの設定が**全て必要**。
1つでも抜けるとNO DECODEになる。

| 項目 | 設定値 | SCPIコマンド | 備考 |
|------|--------|-------------|------|
| バスタイプ | LIN | `BUS:B1:TYPe LIN` | |
| ソース | CH1 | `BUS:B1:LIN:SOUrce CH1` | LIN信号を接続したCH |
| ボーレート | **9600bps** | `BUS:B1:LIN:BITRate CUSTom` → `BUS:B1:LIN:BITRate:CUSTom 9600` | ⚠ プリセットに9600がないため**CUSTOM**で指定 |
| 閾値 | **5.0V** | `BUS:B1:LIN:SOUrce:THReshold 5.0` | ⚠ デフォルト0Vだと全くデコードできない |
| 極性 | NORMAL | `BUS:B1:LIN:POLarity NORMAL` | |
| IDフォーマット | NOPARITY | `BUS:B1:LIN:IDFORmat NOPARITY` | 6bitバイナリ指定時はNOPARITY |
| 規格 | V2X | `BUS:B1:LIN:STANDard V2X` | |

### ハマりポイント

1. **閾値（Threshold）**: デフォルト0V → LINは0〜12Vスイングなので全ビットがHIGH扱いになりNO DECODE。**必ず5Vに設定**
2. **ボーレート**: 919DのステロクLINは**9600bps**。プリセットのRATEリストに9600がないため、`CUSTom`モードで数値指定する必要がある。19200bpsだとデコードエラーになる
3. **SCPI設定順序**: `BITRate CUSTom` を先に設定してから `BITRate:CUSTom 9600` でカスタム値をセット

### SCPI設定スクリプト例

```python
# B1をLINに設定
inst.write('BUS:B1:TYPe LIN')
inst.write('BUS:B1:LIN:SOUrce CH1')
inst.write('BUS:B1:LIN:SOUrce:THReshold 5.0')
inst.write('BUS:B1:LIN:BITRate CUSTom')
inst.write('BUS:B1:LIN:BITRate:CUSTom 9600')
inst.write('BUS:B1:LIN:POLarity NORMAL')
inst.write('BUS:B1:LIN:IDFORmat NOPARITY')
inst.write('BUS:B1:LIN:STANDard V2X')
```

### CH割り当て（ステロクECU測定時）

| CH | 信号 | スケール | 接続先 |
|----|------|---------|--------|
| CH1 | LIN | 2V/div | ステロクECU Pin6 (LIN) |
| CH2 | IG | 5V/div | ステロクECU Pin1 (IGE) |
| CH3 | REF（照合ECU側LIN） | 2V/div | 照合ECU LIN端子 |
| CH4 | IND（予備） | — | 必要に応じてインジケータ等 |
