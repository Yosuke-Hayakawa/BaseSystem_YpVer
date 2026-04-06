# UF作成（ユーザーファンクション）

CRAMASのユーザーファンクション（uf.c / uf.h）の作成・編集ルールとリファレンス。

## 実ファイルの場所

| ファイル | パス | 説明 |
|----------|------|------|
| uf.c | `C:\simbase\simdat\919D_照合ECU\EXTMODULES\uf.c` | メインユーザー関数（288KB） |
| uf.h | `C:\simbase\simdat\919D_照合ECU\EXTMODULES\uf.h` | 変数構造体定義 |
| main.h | `C:\simbase\simdat\919D_照合ECU\EXTMODULES\main.h` | uf.cが#includeするファイル（uf.hのコピー） |
| UF.log | `C:\simbase\simdat\919D_照合ECU\EXTMODULES\UF.log` | コンパイルログ |
| testpat.tes | `C:\simbase\simdat\919D_照合ECU\testpat.tes` | シミュレーション設定（タイマーステップ: 1ms） |
| ioset.ios | `C:\simbase\simdat\919D_照合ECU\ENVDATA\IOPAT\ioset.ios` | ボード⇔UF変数のマッピング |
| ボード設定 | `C:\simbase\simdat\919D_照合ECU\ENVDATA\BOARD\` | IOボード設定（.ai/.di/.do/.can*/.lin*） |
| 計測データ | `C:\simbase\simdat\919D_照合ECU\ANALYZE\` | .datファイル |

**注意**: 919D_照合ECUフォルダはCRAMASが直接読みに行くため、場所は動かせない。

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
    r'C:\simbase\simdat\919D_照合ECU\EXTMODULES\uf.c',
    rf'C:\Users\CARAMAS4\git-practice\cramas-analysis\一時\uf.c.bak_{ts}'
)
shutil.copy2(
    r'C:\simbase\simdat\919D_照合ECU\EXTMODULES\uf.h',
    rf'C:\Users\CARAMAS4\git-practice\cramas-analysis\一時\uf.h.bak_{ts}'
)
```

## ビルド方法

```
cd C:\simbase\simdat\919D_照合ECU\EXTMODULES
C:\simbase\cxlib\common\crms_make.bat -f uf.mk CLIBDIR=c:/simbase/cxlib RTLVER=prtk_100
```
- EXTMODULESフォルダで実行すること
- `warning: 'CAN_SbW_Periodic_Send' defined but not used` は既知のwarningで無視してOK
- エラー時は必ず `EXTMODULES/UF.log` を確認
- CRAMAS再起動が必要な場合あり

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
val.Stress_time++;              // 1ms毎に+1
if(val.Stress_time >= 1000) {   // 1000ms = 1秒経過
    AfterStressChkReset();      // タイマーリセット
    val.AfterStressChk_Step1++; // 次のステップへ
}
```

switch/caseによる遷移：
```c
switch(val.AfterStressChk_Step1) {
    case 0:   // 初期化
        ...
        val.AfterStressChk_Step1 = VAL5;  // 次のステップへ
        break;
    case 5:   // 次の処理
        ...
        break;
}
```

#### Cパネル（手動/自動切替）

- **手動モード**: `val.AfterStressIni_Oneshot == OFF`
  - Cパネル入力をそのまま出力
- **自動モード**: `val.AfterStressIni_Oneshot == ON`
  - 内部変数（`val.Uf_xxx`）を出力

#### AfterStress判定の構造

- **AfterStressChk()**: メイン制御関数（1167行目）
- **AfterStressChkReset()**: リセット関数（570行目）
- **AfterStressInitial()**: 初期化（1346行目）
- **AfterStressCase0()**: リセット処理（1392行目）
- **AfterStressCase1()**: ベース（ストレスなし基本フロー）
- **AfterStressCase2～13()**: 派生（途中でストレス印加）

**派生ケースの作り方:**
1. Case1をコピー
2. ストレス印加ポイントでCATT連携を挿入
3. 前後のステップはそのまま再利用

#### NG判定

```c
ng_set(20);  // NG番号20をセット
```
- NG番号で何がNGか特定
- 複数NG発生時は全て記録

#### NG番号一覧（uf.cのng_set()呼び出しに基づく）

| NG番号 | 内容 | 状態 |
|--------|------|------|
| 10 | Sleep不良(タイムアウト) | ○ |
| 11 | Sleep不良(5秒/30秒経過) | ○ |
| 20 | ブザー誤吹鳴 | ○ |
| 30 | インジケータ異常 | ○ |
| 40 | UWB異常(Aコードと差) | ○ |
| 41 | UWB異常(エミュレータ出力) | ○ |
| 50 | ドアロック異常(Sleep中ロック=0以外) | ○ |
| 60 | CAN通信停止(Sleep中CAN受信あり) | ○(Sleep中のみ) |
| 61 | CAN通信途絶(Wake中500ms無受信) | ○(Wake中のみ) |
| 70 | CLG1異常(Hi時間超過) | コメントアウト |
| 71 | CLG1異常(Lo継続100ms以上) | コメントアウト |
| 72 | CLG2異常(Hi時間超過) | コメントアウト |
| 73 | CLG2異常(Lo継続100ms以上) | コメントアウト |
| 74 | CLG5異常(Sleep中動作: 6V以上) | ○ |
| 75 | CLG5異常(Wake中不動作: 6V未満) | ○(case90/91のみ) |
| 80 | メーター異常 | ○ |
| 81 | ステロク異常(Lin_SILK/SIUL) | ○ |
| 82 | SWILイルミ異常 | ○ |
| 90 | LIN通信停止(Sleep中StatusCounter変化) | ○(Sleep中のみ) |
| 91 | LIN通信途絶(Wake中250ms無応答) | ○(Wake中のみ) |
| 92 | PFW誤出力(Sleep中PFW≠0) | ○ |

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

### ファイルの場所

```
C:\simbase\simdat\919D_照合ECU\ENVDATA\IOPAT\ioset.ios
```
testpat.tesで参照：`IOSET: "ioset.ios"`

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
/S=21200,0,0x03,"+B"  /S=0,0,0x00,""  /D=805371904,0,0x18,"V10_Volt",""  /K=0
```
→ AIボード1（21200）のCH3「+B」をUFの`in.V10_Volt`（オフセット0x18）に入力

#### 例2: UF出力変数をDOボードに割り当て
```
/S=0,0,0x00,""  /S=0,0,0x00,""  /D=21100,0,0x00,"送り機@1_電源",""  /K=0
```
→ UFの出力変数をDOボード1（21100）のCH0に出力

#### 例3: CパネルのDO出力
```
/S=0,0,0x00,""  /S=0,0,0x00,""  /D=21101,0,0x00,"SSW",""  /K=0
```
→ CパネルのSSW（スタートスイッチ）をDOボード2（21101）のCH0に出力

### オフセット値の確認方法

uf.hの構造体定義順に8バイト（double）または4バイト（int）ずつ増える。
正確なオフセットはCRAMASが自動計算しているため、既存の設定を参考にする。

### 編集方法

**ioset.iosはCRAMASのGUIから設定すること**（テキスト編集は非推奨）

### 現在のUF→DOマッピング（CpanelOutput制御対象）

| UF変数 | UFオフセット | DOボード | DOアドレス | ioset.ios行 | 備考 |
|--------|-------------|---------|-----------|-------------|------|
| Uf_SmartKeyOff | 0x144 | 21100 | 0x00 | 398 | 携帯機①_電源 |
| SSW | 0x100 | 21101 | 0x00 | 399 | - |
| SleepInd | 0xF4 | 21101 | 0x03 | 400 | - |
| WakeUpInd | 0xF8 | 21101 | 0x04 | 401 | - |
| DCTY | 0xFC | 21101 | 0x05 | 402 | - |

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
- **行の順番は変えないこと**（BLKNUM: 392で管理）
- **既存のマッピングを削除する場合は `/S=0,0,0x00,""` で無効化**

---

## ボード構成（919D）

### AIボード（アナログ入力）

**AIボード1（21200 - crai.ai）:** 12ch全使用
- CH0: CLG1 - クランプ信号1
- CH1: CLG2 - クランプ信号2
- CH2: CLG5 - クランプ信号5
- CH3: +B - バッテリ電源
- CH4: ACCD - アクセサリ電源
- CH5: IGP - イグニッション電源P
- CH6: IGR - イグニッション電源R
- CH7: IGBD - イグニッションバックアップ電源
- CH8: ST2 - スタータ信号2
- CH9: RCO
- CH10: CSEL - セレクト信号
- CH11: RDAM

**AIボード2（21201 - crai_02_001.ai）:** 6ch使用
- CH0: IND - インジケータ
- CH1: SWIL - スイッチ照明
- CH2: STA - スタータ
- CH3: SLA - スマートロックアンテナ
- CH4: SLP
- CH5: SLR
- CH6～11: 未使用

**AIボード3（21202 - crai_03_001.ai）:** 全ch未使用（予備）

### DI/DOボード（デジタル入出力）

**DIボード（21000 - crdi.di）:** 16ch、11ch使用
- CH0: LSWR - ロックスイッチ
- CH1: ACCD - アクセサリ検出
- CH2: IG1D - IG1検出
- CH3: IG2D - IG2検出
- CH4: ロボット作動中
- CH5～6: 予備1～2
- CH7～10: SikuliX1～4_IN（画像認識自動化ツール入力）
- CH11～15: 未使用

**DOボード1（21100 - crdo.do）:** 16ch全使用
- CH0～2: 送り機@1_電源/ロック/アンロック
- CH3～5: 送り機@2_電源/ロック/アンロック
- CH6: D系アンテナON
- CH7: ロボット動作開始
- CH8～10: Cont1～3
- CH11: 予備4
- CH12～15: SikuliX1～4（画像認識自動化ツール出力）

**DOボード2（21101 - crdo_02.do）:** 16ch、7ch使用
- CH0: SSW - スタートスイッチ
- CH1: 車両解除
- CH2: エミュレーターOFF
- CH3～11: 未使用
- CH12～15: EmuRset1～4（エミュレータリセット）

### CANボード（CAN通信）

**重要:** CANは送信(cant)ではなく**受信(canr)ファイルにメッセージ定義がある**

**CAN CH1（21600）:** バス制御のみ
- ボーレート: 500kbps
- 故障モード試験用（断線、短絡、高負荷）
  - SleepMode: スリープ/ウェイクアップ
  - CAN_H_OPEN/CAN_L_OPEN: 断線故障
  - CAN_SHORT: 短絡故障
  - HiLoad: 高負荷通信試験

**CAN CH2（21600）:** 大量のメッセージ定義（受信側）
- **照合ECU関連**（0x632～0x642）: キー登録、ロック/アンロック、車速等
- **メーター関連**（0x610, 0x611）: 車速、走行距離、シフト位置
- **PDB関連**（0x2D1）: IG/ACC状態
- **DCM系**（0x675）: その他制御
- **ENG関係**（0xFC）: エンジン系通信

### LINボード（LIN通信）

**重要:** LINも送信(lint)ではなく**受信(linr)ファイルにメッセージ定義がある**

**LIN CH1（21700）:** 照合ECU⇔ID-BOX通信
- **照合ECU→ID-BOX@**（0x35）: キー登録、EFI通信、NM通信
- **照合ECU→ID-BOX A**（0x3A）: Lキー登録、NM通信、登録本数
- **照合ECU→RS系@**（0x36）: キーロック情報、状態通信
- **ID-BOX系A**（0x39）: L/Sキー登録、照合アンテナ情報
- **ID-BOX系B**（0x34）: キーロック、状態監視
- **電源制御@**（0x22）: IG/ACC動作、通信制御

### その他のボード種類
- **AO**: アナログ出力（crao.ao） - 解析方法はAI/DIと同じ
- **UART**: シリアル通信（cruart_*.sioc/siorb/siotb等）

### ボード設定ファイルの解析方法

#### 共通手順
1. `testpat.tes`で参照ファイルを確認
2. `ENVDATA/BOARD/`から該当ファイルを開く
3. ファイル内容の読み方：
   - `@BRD`: ボードID、ボード名、ポート番号
   - `@PRT`: ポート番号、チャンネル数、説明
   - `@LBL`: 信号ラベル名、チャンネル番号、型、初期値等
   - `@TRF`: 変換係数（ゲイン、オフセット、レンジ）

**※ ボード設定ファイル(.ai/.do/.can*等)は編集しない方針（CRAMAS GUIで操作）**

#### testpat.tesでの参照例
```
SELECTPORT00: "21200,0,crai.ai"
SELECTPORT01: "21201,0,crai_02_001.ai"
SELECTPORT02: "21202,0,crai_03_001.ai"
SELECTPORT37: "21000,0,crdi.di"
SELECTPORT38: "21100,0,crdo.do"
SELECTPORT39: "21101,0,crdo_02.do"
SELECTPORT04: "21600,1,crcan_busctrl_1_001.canb"
SELECTPORT05: "21600,2,crcan_send_1_001.cant"
SELECTPORT06: "21600,3,crcan_recv_1_001.canr"
SELECTPORT40: "21700,1,crlin_master_1_001.linm"
SELECTPORT41: "21700,2,crlin_masterctrl_1_001.linmc"
SELECTPORT42: "21700,3,crlin_slave_1_001.lint"
SELECTPORT45: "21700,6,crlin_recv_1_002.linr"
```

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
- **ポート**: 8（CAN CH2の場合）
- **シグナルID**: canrファイルの`@LBL:`行の2番目の値（例: 0x141201）
- **ラベル名**: canrファイルから**バイナリのまま**コピー必須！

### 正しい編集方法（Pythonでバイナリ処理）
```python
# canrからラベル取得
with open('crcan_recv_2_002.canr', 'rb') as f:
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

### CAN信号一覧（0x630, 0x633）

| 変数名 | シグナルID | 信号名 | CAN ID |
|--------|-----------|--------|--------|
| Can_WBZF | 0x82008 | ワイヤレスブザー吹鳴信号 | 0x630 |
| Can_NSPB | 0x141001 | メータブザー連続吹鳴信号 | 0x633 |
| Can_BZDN | 0x141101 | メータブザー断続吹鳴信号 | 0x633 |
| Can_BZ | 0x141201 | メータブザー単発吹鳴信号 | 0x633 |
| Can_BZDN2 | 0x141301 | メータブザー断続0.7秒 | 0x633 |
| Can_BZ2 | 0x142A01 | イモビキー照合完了通知 | 0x633 |
| Can_SWR2 | 0x143004 | スマートシステム警告2 | 0x633 |
| Can_SWR3 | 0x143403 | スマートシステム警告3 | 0x633 |
| Can_SWR1 | 0x143804 | スマートシステム警告1 | 0x633 |

### ファイルの役割

| ファイル | 役割 | 編集者 |
|----------|------|--------|
| .ai/.di等 | ボードのチャンネル定義 | 通常変更しない |
| uf.h | UF変数の定義 | エージェント |
| ioset.ios | ボード↔変数の配線 | CRAMAS GUI |

---

## SikuliX連携（FakeSikulix）

### プログラム場所
- **ネットワークパス**: `\\Hn-70-19528\io_bord\919D用\FakeSikulix.py`
- **共通ライブラリ**: `\\Hn-70-19528\io_bord\` 直下
  - `relay_control.py` - Arduinoリレー制御
  - `click_image.py` - シングルクリック
  - `doubleclick_image.py` - ダブルクリック
  - `image_match.py` - 画像一致判定

### 通信構成
```
CRAMAS DO(21100) CH12-15 → Arduino → SikuliX PC (DI)
SikuliX PC (DO) → Arduino → CRAMAS DI(21000) CH7-10
```

### モード選択（DI 4bit）

| di_state | 動作 |
|----------|------|
| 0 | 待機（リセット） |
| 1 (0b0001) | ダイアグ通信モニタ初期化 |
| 2 (0b0010) | キー登録 |
| 4 (0b0100) | ストップルーチン |

### 応答（DO）

| relay | 意味 |
|-------|------|
| relay_on(0) | 処理完了通知 |
| relay_on(2) | 処理開始通知 |

### CRAMAS変数対応
- **出力（DO）**: out.SikuliX1～4 → DI[0]～[3]として読まれる
- **入力（DI）**: SikuliX1～4_IN → in.Sikulix_OK, in.Sikulix_St1, in.Sikulix_St2

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
- CANビットアサイン表(305D): `Y:\305D_照合ECU\001_製品資料\03_仕様書\gncanvehcs-305D-0003-a-BITASSIGN.xlsx`
- テスト設計仕様書: `Y:\919D_照合ECU\011_実験部資料\02_テスト仕様\919D_テスト設計仕様書_テンプレート_20250827.xlsm`
- ステロクロックECU仕様書: `C:\いろいろ\一時置き\照合資料\ステロク\`
  - `CV向け/` - 制御仕様書ver1.5 + 個別仕様①～⑬
  - `変更分/` - 個別仕様③④⑦⑧⑨⑩⑪の更新版
