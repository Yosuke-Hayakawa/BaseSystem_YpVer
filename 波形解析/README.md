# 波形解析

CRAMAS HILSテストの波形データ解析ツール群とデータ。

## スクリプト一覧

| ファイル | 場所 | 説明 |
|----------|------|------|
| project_config.py | scripts/ | プロジェクト設定ローダー |
| ng_check.py | scripts/ | NG判定チェック（メイン解析スクリプト） |
| dat_to_csv.py | scripts/ | dat→CSV一括変換 |
| extract_anomaly.py | scripts/ | 異常値抽出 |
| wave_viewer.py | scripts/ | CSV波形ビューア |
| 波形ビューア起動.bat | scripts/ | wave_viewerのバッチラッパー |
| NG解析.bat | ./ | ng_check.pyのバッチラッパー |

## プロジェクト構成

製品ごとに `projects/<製品名>/` を作り、`config.yaml` で固有設定を管理する。

```
projects/<製品名>/
├── config.yaml     # NG番号辞書、カラム名、パス設定等
├── docs/           # 製品固有リファレンス
├── output/         # NG解析結果レポート
├── data/           # ログデータ（.gitignore）
└── 要解析/         # 特異パターンデータ（.gitignore）
```

## 使い方

### NG解析
```
NG解析.bat
```
または
```
python scripts/ng_check.py --project 919D
python scripts/ng_check.py                    # プロジェクト自動検出
python scripts/ng_check.py /path/to/logdir    # ログフォルダ直接指定
```

### dat→CSV変換
```
python scripts/dat_to_csv.py --project 919D
python scripts/dat_to_csv.py <フォルダパス>
```

### 波形ビューア
```
scripts/波形ビューア起動.bat
```
