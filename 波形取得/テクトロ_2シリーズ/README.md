# テクトロニクス 2シリーズ（MSO22/MSO24）自動制御

## 接続方法
- ライブラリ: **pyvisa**（`pip install pyvisa pyvisa-py`）
- Vendor ID: `0x0699`（Tektronix）
- VISAリソース文字列で自動検出（USB TMCデバイスからVID一致を探す）
- タイムアウト: 60秒（`inst.timeout = 60000`）

## 画面キャプチャの流れ
1. `SAVe:IMAGe "C:/temp_cap.png"` → オシロ内部に一時PNG保存
2. `*OPC?` → 保存完了待ち
3. `FILESystem:READFile "C:/temp_cap.png"` → ファイル読み出し
4. `inst.read_raw()` → バイナリデータ取得
5. `FILESystem:DELEte "C:/temp_cap.png"` → オシロ上の一時ファイル削除

## LINトリガID変更
```
TRIGger:A:BUS:B1:LIN:CONDition IDentifier
TRIGger:A:BUS:B1:LIN:IDentifier:VALue "110011"   ← 6bitバイナリ文字列
```
- IDは16進数ではなく **6bitバイナリ文字列** で指定する（例: 0x33 → "110011"）
- `*OPC?` の後に `time.sleep(2)` を入れないとトリガがかかる前にキャプチャされる

## 使用中のLINフレーム一覧
| 名前 | FrameID | バイナリ |
|------|---------|---------|
| STL1S01 | 0x33 | 110011 |
| IDB1S01 | 0x31 | 110001 |
| IDT1S01 | 0x30 | 110000 |
| EIG1S01 | 0x22 | 100010 |

## LINバス番号の確認方法
```python
for i in range(1, 5):
    bus_type = inst.query(f"BUS:B{i}:TYPe?").strip()
    # "LIN" が返ればそのバス番号を使う
```

## スクリプト一覧
| ファイル | 内容 |
|---------|------|
| `capture_screen.py` | 汎用画面キャプチャ。引数でVISAアドレス指定可、省略で自動検出 |
| `capture_lin_ids.py` | STL1S01→IDB1S01→IDT1S01の順にLIN ID切替＋連続キャプチャ |
| `capture_eig.py` | EIG1S01(0x22)だけキャプチャして0x33に復帰 |
| `capture_igon_rest.py` | IG ON状態でIDB1S01→IDT1S01→EIG1S01を連続キャプチャ |
| `画面取得.bat` | capture_screen.pyのランチャー（ダブルクリック用） |

## 注意点
- キャプチャ完了後、トリガIDを **0x33に復帰** する運用（capture_eig, capture_igon_rest）
- 画像保存先: `画像ファイル/` フォルダ（自動作成）
- ファイル名にタイムスタンプ付き（`YYYYMMDD_HHMMSS`）
