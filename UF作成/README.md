# UF作成（ユーザーファンクション）

CRAMASのユーザーファンクション（uf.c / uf.h）の作成・編集ルールとリファレンス。
プロジェクト固有の設定（ファイルパス、ボード構成、NG番号一覧等）は `波形解析/projects/<製品名>/docs/` を参照。

## 実ファイルの場所

| ファイル | パス | 説明 |
|----------|------|------|
| uf.c | `<EXTMODULESフォルダ>/uf.c` | メインユーザー関数 |
| uf.h | `<EXTMODULESフォルダ>/uf.h` | 変数構造体定義 |
| main.h | `<EXTMODULESフォルダ>/main.h` | uf.cが#includeするファイル（uf.hのコピー） |
| UF.log | `<EXTMODULESフォルダ>/UF.log` | コンパイルログ |
| testpat.tes | `<CRAMASプロジェクトフォルダ>/testpat.tes` | シミュレーション設定（タイマーステップ: 1ms） |
| ioset.ios | `<CRAMASプロジェクトフォルダ>/ENVDATA/IOPAT/ioset.ios` | ボード⇔UF変数のマッピング |
| ボード設定 | `<CRAMASプロジェクトフォルダ>/ENVDATA/BOARD/` | IOボード設定（.ai/.di/.do/.can*/.lin*） |
| 計測データ | `<CRAMASプロジェクトフォルダ>/ANALYZE/` | .datファイル |

**注意**: CRAMASプロジェクトフォルダはCRAMASが直接読みに行くため、場所は動かせない。

## 編集前のバックアップルール【最重要】

**必ず「バックアップ→編集」の順番を守ること！**

1. 編集前にuf.c / uf.hのコピーを `一時/` フォルダに作成する
2. タイムスタンプ付きで保存: `uf.c.bak_YYYYMMDD_HHMMSS`
3. 削除はゴミ箱経由（send2trash使用、os.remove / shutil.rmtree 禁止）

```python
import shutil
from datetime import datetime

ts = datetime.now().strftime('%Y%m%d_%H%M%S')
shutil.copy2(
    r'<EXTMODULESフォルダ>\uf.c',
    rf'<一時フォルダ>\uf.c.bak_{ts}'
)
shutil.copy2(
    r'<EXTMODULESフォルダ>\uf.h',
    rf'<一時フォルダ>\uf.h.bak_{ts}'
)
```

## ビルド方法

```
cd <EXTMODULESフォルダ>
C:\simbase\cxlib\common\crms_make.bat -f uf.mk CLIBDIR=c:/simbase/cxlib RTLVER=prtk_100
```
- EXTMODULESフォルダで実行すること
- エラー時は必ず `EXTMODULES/UF.log` を確認
- CRAMAS再起動が必要な場合あり
- プロジェクト固有の既知warningは `波形解析/projects/<製品名>/docs/` を参照

## ファイルエンコーディング

- **uf.c, uf.h** → UTF-8（CRAMASコンパイラで動作確認済み）
- **ioset.ios** → cp932（Shift-JIS）
- **ボード設定ファイル等** → 編集しない（CRAMAS GUIで操作）

## main.hとuf.hの関係

- **uf.h**: 実際の構造体定義ファイル
- **main.h**: uf.cが`#include "main.h"`で参照するファイル
- **運用**: uf.hを編集したら、main.hにもコピーする

```powershell
Copy-Item "uf.h" "main.h" -Force
```

---

## uf.c プログラム基本ルール

### CRAMASカスタムC言語

**通常のC言語ではなくCRAMAS専用言語**

#### 変数システム

```c
#define in  ExtInput    // 入力変数（読み取り専用）
#define out ExtOutput   // 出力変数（実機へ出力）
#define val ExtPrms     // 内部変数（状態管理）
```

**変数の役割:**
1. `in.xxx` - CRAMASからの入力（ボード/Cパネル）
2. `out.xxx` - CRAMASへの出力（実機反映）
3. `val.xxx` - UF内部の状態管理・計算用

#### 実行タイミング

- `uf_rtloop()` が **1msごと**に実行される
- タイマーは1ms = 1カウント

**時間定数:**
| 定数 | 値 | 時間 |
|------|-----|------|
| TIME100MS | 100 | 0.1秒 |
| TIME500MS | 500 | 0.5秒 |
| TIME1000MS | 1000 | 1秒 |
| TIME3000MS | 3000 | 3秒 |
| TIME5000MS | 5000 | 5秒 |
| 60000 | 60000 | 60秒 |
| 300000 | 300000 | 5分 |

**データ型とサイズ:**
| 型 | バイト数 | 型番号 |
|----|---------|--------|
| int | 4バイト | 5（符号付き32bit整数） |
| double | 8バイト | 10（倍精度浮動小数点） |

#### ステップ遷移

```c
val.タイマー変数++;              // 1ms毎に+1
if(val.タイマー変数 >= 1000) {   // 1000ms = 1秒経過
    リセット関数();               // タイマーリセット
    val.ステップ変数++;           // 次のステップへ
}
```

switch/caseによる遷移：
```c
switch(val.ステップ変数) {
    case 0:   // 初期化
        ...
        val.ステップ変数 = 次の値;  // 次のステップへ
        break;
    case 5:   // 次の処理
        ...
        break;
}
```

#### Cパネル（手動/自動切替）

- **手動モード**: Cパネル入力をそのまま出力
- **自動モード**: 内部変数（`val.Uf_xxx`）を出力
- 切替フラグで制御する（プロジェクトごとに変数名は異なる）

#### NG判定

```c
ng_set(20);  // NG番号20をセット
```
- NG番号で何がNGか特定
- 複数NG発生時は全て記録
- プロジェクト固有のNG番号一覧は `波形解析/projects/<製品名>/docs/` を参照

#### コメントルール（sakuraアウトライン用）

```c
/*● /// 大見出し*/
/*▲ /// 中見出し*/
/*■ /// 小見出し*/
```
- **Yp.rule**ファイルに記載

---

## uf.h 編集ルール【重要】

### 編集可能範囲

**✅ 編集OK:** 構造体**内部の変数定義のみ**
**❌ 絶対NG:** 構造体外の宣言・関数・マクロ定義、typedef struct の行

### 構造体の種類

1. `_mproject_extinput` → in.xxx（入力変数）
2. `_mproject_extoutput` → out.xxx（出力変数）
3. `_mproject_extprms` → val.xxx（内部変数）

### 禁止事項

- **空構造体禁止**（必ずダミー変数を1つ入れる）
- 構造体名の変更禁止
- typedef structの変更禁止

### 編集手順

1. 必ず `一時/` にバックアップを取る
2. 構造体内部のみ編集
3. バックアップと比較して差分確認
4. 構造体外を変更していないか確認
5. uf.hを編集したら `main.h` にもコピーする

---

## ioset.ios 参照情報

### ファイルの役割

**ボードの物理入出力をUF変数に割り当てる**設定ファイル。
CRAMASのGUIで配線図のように「このピンをこの変数に繋ぐ」設定を記述する。
testpat.tesで `IOSET: "ioset.ios"` として参照される。

### 基本構文

```
/S=ソースID,ポート,チャンネル,"ラベル"  /S=...(未使用)  /D=デスティネーションID,オフセット,"変数名",""  /K=0
```

#### ソース（/S）- 入力元
- **ソースID**: ボードID（21200: AI1, 21201: AI2, 21000: DI, 21100: DO1, 21101: DO2, 21600: CAN, 21700: LIN）
- **ポート**: ボード番号（通常0）
- **チャンネル**: チャンネル番号（16進数 0x00～0x0F等）
- **ラベル**: ボード設定ファイル(.ai/.do等)で定義したラベル名

#### デスティネーション（/D）- 出力先
- **デスティネーションID**: 805371904（UF）, 10000（電源制御）, 21100/21101（DOボード）
- **オフセット**: 構造体内のオフセット（16進数、uf.hの定義順に対応）
- **変数名**: UF変数名（`in.xxx`, `out.xxx`）

### 設定例

#### 例1: AIボードの電圧をUF入力変数に割り当て
```
/S=<AIボードID>,0,<チャンネル>,"<ラベル名>"  /S=0,0,0x00,""  /D=805371904,0,<オフセット>,"<変数名>",""  /K=0
```
→ AIボードの指定チャンネルをUFの入力変数に割り当て（オフセットはuf.hの定義順から計算）

#### 例2: UF出力変数をDOボードに割り当て
```
/S=0,0,0x00,""  /S=0,0,0x00,""  /D=21100,0,0x00,"<ラベル名>",""  /K=0
```
→ UFの出力変数をDOボード1（21100）のCH0に出力

#### 例3: CパネルのDO出力
```
/S=0,0,0x00,""  /S=0,0,0x00,""  /D=21101,0,0x00,"<ラベル名>",""  /K=0
```
→ CパネルのスイッチをDOボード2（21101）のCH0に出力

### オフセット値の確認方法

uf.hの構造体定義順に8バイト（double）または4バイト（int）ずつ増える。
正確なオフセットはCRAMASが自動計算しているため、既存の設定を参考にする。

### 編集方法

**ioset.iosはCRAMASのGUIから設定すること**（テキスト編集は非推奨）

### ボードIDとUF変数の対応

| ボードID | ボード名 | 設定ファイル | 用途 |
|---------|---------|------------|------|
| 21200 | AIボード1 | crai.ai | 電圧入力 |
| 21201 | AIボード2 | crai_02.ai | 電圧入力 |
| 21000 | DIボード | crdi.di | デジタル入力 |
| 21100 | DOボード1 | crdo.do | デジタル出力 |
| 21101 | DOボード2 | crdo_02.do | デジタル出力 |
| 21600 | CANボード | crcan_*.can* | CAN通信 |
| 21700 | LINボード | crlin_*.lin* | LIN通信 |
| 805371904 | UF | uf.h | User Function |

### 注意事項

- **編集後はCRAMASの再起動が必要な場合がある**
- **行の順番は変えないこと**（BLKNUMで管理）
- **既存のマッピングを削除する場合は `/S=0,0,0x00,""` で無効化**

---

## ボード設定ファイルの解析方法

### 共通手順
1. `testpat.tes`で参照ファイルを確認
2. `ENVDATA/BOARD/`から該当ファイルを開く
3. ファイル内容の読み方：
   - `@BRD`: ボードID、ボード名、ポート番号
   - `@PRT`: ポート番号、チャンネル数、説明
   - `@LBL`: 信号ラベル名、チャンネル番号、型、初期値等
   - `@TRF`: 変換係数（ゲイン、オフセット、レンジ）

**※ ボード設定ファイル(.ai/.do/.can*等)は編集しない方針（CRAMAS GUIで操作）**

### testpat.tesでの参照形式

`testpat.tes` 内で以下の形式でボード設定ファイルが参照される：
```
SELECTPORT番号: "ボードID,ポート番号,ファイル名"
```
<!-- 具体的なポート割り当ては波形解析/projects/<製品名>/docs/ を参照 -->

### ボード種類一覧
- **AI (.ai)**: アナログ入力
- **AO (.ao)**: アナログ出力
- **DI (.di)**: デジタル入力
- **DO (.do)**: デジタル出力
- **CAN (.canb/.cant/.canr)**: CAN通信（バス制御/送信/受信）
- **LIN (.linm/.linmc/.lint/.linr)**: LIN通信（マスタ/マスタ制御/スレーブ送信/受信）
- **UART (.sioc/.siorb/.siotb)**: シリアル通信

---

## ボード変数の追加・割り付け手順

### 概要
ボード（AI/DI/DO等）のチャンネルをUF変数に割り付ける手順。

### 手順

**1. 調査**
- ボード設定ファイル（.ai, .di等）でチャンネル一覧を確認
- uf.hで既存の入力変数を確認
- どのチャンネルをどの変数に繋ぐか一覧表を作成

**2. uf.hに変数追加**（エージェントが実施）
- 足りない変数をuf.hの構造体内に追加
- `_mproject_extinput`に`in.xxx`用の変数を追加
- コメントで用途を明記

**3. CRAMASで更新**（陽祐が実施）
- CRAMASを起動
- UFをコンパイル（uf.hの変数を認識させる）
- ioset.iosに新しい変数が自動追加される

**4. ioset.iosで割り付け**（陽祐がCRAMAS GUIで実施）

---

## CAN変数の割り付け手順

### 概要
CAN受信信号をUF変数に割り付ける場合、**canrファイルのラベル名をバイナリのままコピー**する必要がある。
単純な文字列置換では「供給元ポート不明」になる。

### 構文
```
/S=21600,ポート,シグナルID,"ラベル名"  /S=0,0,0x00,""  /D=805371904,0,オフセット,"変数名",""  /K=0
```

- **21600**: CANボードID
- **ポート**: CAN CHに対応（例: CH2の場合は8）
- **シグナルID**: canrファイルの`@LBL:`行の2番目の値（例: 0x141201）
- **ラベル名**: canrファイルから**バイナリのまま**コピー必須！

### 正しい編集方法（Pythonでバイナリ処理）
```python
# canrからラベル取得
with open('<canr受信ファイル>', 'rb') as f:
    canr = f.read()

# ioset.ios読み込み
with open('ioset.ios', 'rb') as f:
    ios_lines = f.read().split(b'\r\n')

# ラベルをバイナリのままコピーして行を構築
new_line = (b'/S=21600,8,' + sig_id + b',"' + label_binary
            + b'"  /S=0,0,0x00,""  /D=805371904,0,'
            + offset + b',"' + var_name + b'",""  /K=0')
ios_lines[行番号] = new_line

# 保存
with open('ioset.ios', 'wb') as f:
    f.write(b'\r\n'.join(ios_lines))
```

### ❌ ダメな方法
- PowerShellで文字列として編集 → ラベルが文字化けして不明になる
- 手動でラベル名を打ち込む → CRAMASが認識しない

### ファイルの役割

| ファイル | 役割 | 編集者 |
|----------|------|--------|
| .ai/.di等 | ボードのチャンネル定義 | 通常変更しない |
| uf.h | UF変数の定義 | エージェント |
| ioset.ios | ボード↔変数の配線 | CRAMAS GUI |

---

## CRAMAS環境ファイル構造

### 主要ファイル一覧

| ファイル | パス | 説明 |
|----------|------|------|
| testpat.tes | ルート | シミュレーション設定（タイマーステップ: 1ms） |
| *.ai | ENVDATA/BOARD/ | アナログ入力ボード設定 |
| *.di | ENVDATA/BOARD/ | デジタル入力ボード設定 |
| *.do | ENVDATA/BOARD/ | デジタル出力ボード設定 |
| *.canb/cant/canr | ENVDATA/BOARD/ | CAN通信設定 |
| *.linm/linmc/lint/linr | ENVDATA/BOARD/ | LIN通信設定 |
| ioset.ios | ENVDATA/IOPAT/ | ボード⇔UF変数マッピング |
| uf.c | EXTMODULES/ | メインユーザー関数 |
| uf.h | EXTMODULES/ | 変数構造体定義 |
| main.h | EXTMODULES/ | uf.hのコピー |
| UF.log | EXTMODULES/ | コンパイルログ |
| *.dat | ANALYZE/ | 計測データ |

## 参考資料

- CRAMASマニュアル: `C:\simbase\help\cramas.pdf`
- CRAMASヘルプ全般: `C:\simbase\help\`
- プロジェクト固有の参考資料は `波形解析/projects/<製品名>/docs/` を参照
