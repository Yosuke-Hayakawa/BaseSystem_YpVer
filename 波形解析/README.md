# 波形解析

CRAMAS HILSテストの波形データ解析ツール群とデータ。

## スクリプト一覧

| ファイル | 場所 | 説明 |
|----------|------|------|
| ng_check.py | scripts/ | NG判定チェック（メイン解析スクリプト） |
| dat_to_csv.py | scripts/ | dat→CSV一括変換 |
| extract_anomaly.py | scripts/ | 異常値抽出 |
| wave_viewer.py | scripts/ | CSV波形ビューア |
| 波形ビューア起動.bat | scripts/ | wave_viewerのバッチラッパー |
| NG解析.bat | ./ | ng_check.pyのバッチラッパー |

## 波形取得（オシロスコープ自動操作）

`波形取得/` フォルダにオシロスコープ（テクトロニクス 2シリーズ）を自動操作するスクリプトがある。
詳細は `波形取得/README.md` を参照。

## プロジェクトデータ

| フォルダ | 内容 | Git管理 |
|----------|------|---------|
| projects/919D/output/ | NG解析結果レポート（ng_check.py出力） | ✅ |
| projects/919D/data/ログデータ/ | CRAMASの.datファイル（約2万件、138GB） | ❌ .gitignore |
| projects/919D/data/OKファイル/ | 参照用OK波形（636MB） | ❌ .gitignore |
| projects/919D/要解析/ | 未解析NGデータ | ❌ .gitignore |

## 使い方

### NG解析
```
NG解析.bat
```
または
```
python scripts/ng_check.py
```

### dat→CSV変換
```
python scripts/dat_to_csv.py <input.dat> <output.csv>
```
CSVの読み方: `pd.read_csv(path, encoding='cp932', skiprows=1, low_memory=False)`

### 波形ビューア
```
scripts/波形ビューア起動.bat
```
