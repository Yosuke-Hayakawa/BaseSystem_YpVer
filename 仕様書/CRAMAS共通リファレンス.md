# CRAMAS共通リファレンス

CRAMAS HILSテストの解析で共通的に使う知識・ツール・フォーマットのまとめ。
製品型番に依存しない汎用情報をここに集約する。

---

## XFileConv（dat→CSV変換ツール）

CRAMASのdatファイルをCSVに変換する外部ツール。

```
パス: C:\simbase\system\bin\XFileConv.exe
使い方: XFileConv.exe -i <input.dat> -o <output.csv>
成功判定: stdoutに "success" を含む
エンコード: cp932（Shift-JIS）
CSVの読み方: pd.read_csv(path, encoding='cp932', skiprows=1, low_memory=False)
```

注意：1ファイルの変換に約30秒かかる。

---

## 試験セットの構造

1回の試験（=1サイクル）は以下のファイル群で構成される：

```
MMDDHHMMSS_000h00m27s.dat   ← セット開始（固定値 000h00m27s）
MMDDHHMMSS_000h00m54s.dat   ← +27秒
MMDDHHMMSS_000h01m21s.dat   ← +54秒
MMDDHHMMSS_000h01m48s.dat   ← +81秒
MMDDHHMMSS_000h02m15s.dat   ← +108秒
MMDDHHMMSS_000h02m42s.dat   ← +135秒
製品名_試験名(T1(番号))_NG.dat  ← T1ファイル（試験結果）
```

- 時系列datは27秒間隔の連続録画（1ファイル約28000行、サンプリング1ms）
- T1ファイルがNG/OKの判定結果を含む
- mtime順でソートし、`000h00m27s`でセット開始を検出する

---

## ng_number1〜3のビットマスク仕様

- **蓄積型ビットマスク**（一度立ったビットは消えない）
- ng_number1: NG1〜32（bit0=NG1, bit9=NG10, ...）
- ng_number2: NG33〜64
- ng_number3: NG65〜96
- case100のAfterStressChkReset()でng_outはリセットされるが、ng_number1〜3は維持

---

## Sleep/WakeUp判定基準（CPU Duty）

| 状態 | MainCpu_HiDuty | SubCpu_HiDuty |
|------|---------------|--------------|
| Sleep | <10 or ≥90 | ≥90 or <10 |
| WakeUp | ≥50 | ≥50 かつ <90 |

---

## 各スクリプトの説明

### ng_check.py
NGファイルを解析してNG番号と発生caseを特定し、NG×case集計をMDに出力する。

```
実行: python scripts\ng_check.py [ログデータフォルダパス]
出力: 結果\YYYYMMDD_HHMMSS_NG解析結果.md
```

処理フロー：
1. テストセットを構築（build_test_sets）
2. _NGファイルを1件ずつXFileConvでCSV変換
3. ng_number1〜3のビット差分でNG番号を検出、AfterStressChk_Step1で発生caseを記録
4. **T1先頭で既にビットが立っていた場合、時系列datを遡って正しいStepを取得**
5. NG×case集計、最多caseの20%以下に★特異マーク

### extract_anomaly.py
NG解析結果MDから特異パターンの試験を自動抽出し、要解析フォルダに分類コピーする。

```
実行: python scripts\extract_anomaly.py
入力: 結果\最新のNG解析結果MD
出力: 要解析\NG番号_case番号\ 等のフォルダにdatファイルをコピー
```

処理フロー：
1. 最新MDからファイルごとのNGパターン(NG番号, case)を抽出
2. 最多パターン=多数派、それ以外=特異
3. 特異パターンごとにフォルダ名生成（NG10_c32形式、複数NG時は__区切り）
4. T1ファイル＋時系列datをセットごとコピー

### dat_to_csv.py
要解析フォルダ内のdatを1試験セット=1CSVに結合変換する。解析用。

```
実行: python scripts\dat_to_csv.py [対象フォルダパス]
      python scripts\dat_to_csv.py  ← 引数なしで要解析フォルダ全体
出力: 対象フォルダ内に試験名.csv
```

処理フロー：
1. 対象フォルダ内の試験セットを構築
2. **代表1件のみ変換**（同じNGパターンなので1件で十分）
3. 時系列dat+T1ファイルを全部CSV変換→pandasで縦結合→1CSV出力
4. 既にCSVがあればスキップ

---

## CSVの列構成

CRAMASのCSVは1062列程度になる。主要列：

| 列名 | 内容 |
|------|------|
| `_source` | 元datファイル名（dat_to_csv.pyが付与） |
| `TIME(sec)` | 時刻 |
| `AfterStressChk_Step1` | 現在のcase番号 |
| `ng_number1〜3` | NGビットマスク（蓄積型） |
| `SleepInd`, `WakeUpInd`, `SleepState` | Sleep関連 |
| `MainCpu_HiDuty`, `SubCpu_HiDuty` | CPU Duty（Sleep/WakeUp判定用） |
| `ACCD`, `IG1D` | 電源状態 |
| `Can_*` | CAN受信信号 |
| `CLG1`, `CLG2`, `CLG5` | アンテナ信号 |
| `Lin_*` | LIN通信関連 |

---

## 共通の注意事項

- datファイルはCRAMAS独自形式、XFileConv.exeでのみCSV変換可能
- CSVはcp932エンコード、1行目スキップが必要（skiprows=1）
- ioset.iosはcp932エンコード、テキスト編集ではなくCRAMAS GUIから設定
- uf.cを変更したら対応する.mdatも更新が必要
- 1ファイルの変換に約30秒、1試験セット（7ファイル）で約3.5分かかる
- CSVは1試験あたり約850MB（1062列×19万行）になるのでメモリに注意
