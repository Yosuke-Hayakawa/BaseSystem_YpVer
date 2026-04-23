V2.10 | 2022-07-25
製品ラインアップ
VTシステム- ECUテスト用のI/Oモジュール

---

2

モジュール共通の特徴
VTシステムモジュール
ラック／バックプレーン
電源
エンジニアリング
まとめ
アジェンダ

---

3
モジュール外観
モジュール共通の特徴
手動測定用プラグ
ステータス
表示用LED
テストハーネス用コネクタ
（フェニックス・コンタクト社製）
バックプレーン接続用コネクタ
（制御、電源供給）
信号切替え／異常状態発生用リレー
信号調節
19インチラック用モジュール

---

4
User-programmable FPGA
モジュール共通の特徴
標準VTモジュール
CANoe上でユーザーコードが動作
VTモジュール上の標準機能セットを利用
FPGAプログラミング対応VTモジュール
VTモジュール上の標準機能も利用可能
ユーザーFPGAによる機能の追加
FPGAコードはユーザーが自由に定義可能
VTモジュール上の全I/Oハードウェアへの
アクセスも可能
FPGA対応モジュール：VT1004A、VT2004A、VT2516A、VT2710、VT2816A、VT2848、VT7900A
Test Module
user code
test execution
VT System
CANoe
I/O Hardware
  System under Test
ECU
FPGA/µC – firmware
pre-processing
FPGA - user code
pre-processing
model execution

---

5
モジュール共通の特徴

VTシステムモジュール
ラック／バックプレーン
電源
エンジニアリング
まとめ
アジェンダ

---

6
負荷および測定モジュールVT1004A / VT1104 -概要-
VTシステムモジュール
最大4個のECU出力に接続
例：バルブ、サーボモーターなどの出力ライン
2線式差動出力を想定
内部電子負荷でのシミュレーション
定電流モード／定抵抗モードでのシミュレーション実行
負荷容量（全チャンネル合計）：定格30W、
ピーク負荷（2秒間）：最大120W（過負荷防止機構付き）
ECU出力電圧値の測定（RMSも含む）
入力レンジ：
> VT1004A
:-40 V … +40 V
> VT1104
:-60 V … +60 V ※分解能：16bit
PWM測定（0.02Hz～200kHz ※Low impedance mode）
外部にシャント抵抗を配線することで電流測定としても使用可
（別途計算が必要）
定格電流:16A（短時間定格：30A–10秒間）
信号切替え、フォールトインジェクション、および外部機器
接続用（2系統）のリレーも完備

---

7
負荷および測定モジュールVT1004A / VT1104 -配線図-
VTシステムモジュール
internal bus bar 1
typically Vbatt/Gnd
internal bus bar 2
measurement 
plugs at front
Original 
Load
e.g. lamp
electronic 
load
voltage/PWM 
measurement
A
D
internal load
original load
ECU power
(bus bar 1)
bus bar 2
Vbatt
Gnd
swap relays
swap relays
1 of 4 channels
VT1004A / VT1104
ECU
output
bus bar 2
short circuit
short circuit to
Vbatt or ground
(bus bar 1)


| 1 of 4 channels to ground
load load
circuit circuit 1)
2
bar
internal bar original
or
short short
bus batt (bus
V |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | 1 of 4 channels to ground
load load
circuit circuit 1)
2
bar
internal bar original
or
short short
bus batt (bus
V |  |  |  |  |  |  |  |  |  |  |
| voltage/PWM electronic
measurement load
A
D
swap relays
internal bus bar 1
typically V /Gnd
batt
swap relays
internal bus bar 2
VT1004A / VT1104 | voltage/PWM electronic
measurement load
A
D |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |


---

8
刺激モジュールVT2004A -概要-
VTシステムモジュール
最大4個のECU入力を管理
例：温度センサー、スイッチなどの入力ライン
2線式差動入力を想定
センサーシミュレーション
可変抵抗：10Ω～10kΩ（ch4のみ1Ω～250kΩ）
定格：200mA, 3.5W
ポテンショメーターのシミュレーション（ch1のみ）
> 可変抵抗を2チャンネル組み合わせて使用することで、
追加のポテンショメーターとして使用することも可能
（別途ソフトウェア上で計算が必要）
出力レンジ：0～40V、分解能：14bit、
最大出力電流：150mA、信号切替時間：1ms（CANoeから操作した場合）
任意波形出力（各チャンネル）
モジュールにダウンロードし、定義された波形での信号出力
信号切替え、フォールトインジェクション、および外部機器接続用（2系統）
のリレーも完備

---

9
internal bus bar 1
typically Vbatt/Gnd
internal bus bar 2
measurement 
plugs at front
Original 
Sensor
e.g. temperature
decade 
resistor
voltage 
stimulation
bus bar 2
short circuit
short circuit to
Vbatt or ground
(bus bar 1)
original sensor
A
D
ECU power
(bus bar 1)
bus bar 2
Vbatt
Gnd
swap relays
swap relays
1 of 4 channels
VT2004A
ECU
input
刺激モジュールVT2004A -内部配線図-
VTシステムモジュール


| 1 of 4 channels to ground sensor
circuit circuit 1)
2
bar
bar original
or
short short
bus batt (bus
V |  |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | 1 of 4 channels to ground sensor
circuit circuit 1)
2
bar
bar original
or
short short
bus batt (bus
V |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |
| voltage decade
stimulation resistor
D
A
swap relays
internal bus bar 1
typically V /Gnd
batt
swap relays
internal bus bar 2
VT2004A | voltage decade
stimulation resistor
D
A |  |  |  |  |  |  |  |  |  |  |  |


---

10
デジタルI/OモジュールVT2516A -概要-
VTシステムモジュール
最大16個のECUデジタル入出力に接続
一般的にデジタルとして使用される入力／出力
（例：スイッチ、LEDなど）
シングルエンド、低電流
単純なI/Oチャンネルとして利用可能の典型的なVTシステム特性
短絡、開放、およびオリジナルのセンサー／アクチュエータ接続用のリレー
外部負荷接続用リレー、プルアップ／プルダウン抵抗
デジタル信号出力（電圧範囲：0～25V、出力電流：±30mA）
出力電圧は任意に変更可能で、簡易的なアナログ出力としても利用可
PWM出力（0.02Hz～25 kHz）
ビットストリーム出力（2～4096bit）
デジタル信号入力（しきい値：0～25V、サンプリング間隔：50µs）
PWM測定（0.02Hz～200kHz）
電圧測定（入力レンジ：±40V、A/Dコンバーター：12bit、1kS/sec）

---

11
ECU
input or
measurement 
plugs at front
Original 
Part
voltage 
measure-
ment
digital 
input
internal Vbatt/Gnd
bus bar
pull-up/-down 
or load resistor
original sensor 
or actuator
ECU power
bus bar
Vbatt
Gnd
internal bus bar
output
short circuit or 
switch to Vbatt
short circuit or 
switch to ground
ground 
or Vbatt
e.g. switch
Pull-up/
-down
ground 
or Vbatt
...
...
...
digital 
signal 
generator
1 of 16 channels
VT2516A
デジタルI/OモジュールVT2516A -内部配線図-
VTシステムモジュール


| ... |  |  | ... |  |  | ... |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |


---

12
シリアルインターフェイスモジュールVT2710 + PSI5SENT piggy -概要-
VTシステムモジュール
デジタルシリアルセンサープロトコルの解析とシミュレーション

4x PSI5 / SENT （PSI5SENTpiggyが各chに必要）

SPI、I2C、UART（RS232 / RS422 / RS485）、LVDS
それぞれ2ch対応（※10MHzを超えるアプリは非対応）

2x8 ユーザーFPGA デジタルI/O
PSI5SENT

PSI5の最大ボーレート：200kBit/s

センサー電源供給出力：25V / 200mA 

同期電圧パルスの電圧や立ち上がり、パルス幅を自由に設定可能

SPC（Short PWM Code）プロトコルのサポート

シグナル線間の短絡

調整可能なRC回路：0.5 Ω… 15.5 Ω/ 1nF … 127nF
SPI / UART / I2C 

ロジックレベルは自由に調整可能：6V / 200mA

SPI用の最大5xチップセレクト（CS）ライン

最大10MHzのクロック周波数

---

13
シリアルインターフェイスモジュールVT2710 -内部配線図-
VTシステムモジュール
internal bus bar 1
typically Vbatt/Gnd
internal bus bar 2
measurement 
plugs at front
Power
supply
bus bar 2
short circuits
short circuit to
Vbatt or ground
(bus bar 1)
ECU power
(bus bar 1)
bus bar 2
Vbatt
Gnd
swap relays
swap relays
VT2710
1 of 4 PSI5/SENT channels
PSI5/SENT GND
PSI5/SENT +
SENT VDD
Sync
Pulse
Variable 
R / C 
Sync +
supply out
Sensor
Sync + 
supply in
Frame out
ECU
Frame in
OR
Rx/Tx
U or I 


| 1 of 4 PSI5/SENT channels to ground
circuits
circuit 1)
2
bar
bar
or
short short
bus batt (bus
V
SENT VDD |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | 1 of 4 PSI5/SENT channels to ground
circuits
circuit 1)
2
bar
bar
or
short short
bus batt (bus
V
SENT VDD |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Sensor |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | PSI5/SENT + |  |  | Sync + |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | PSI5/SENT GND |  |  | supply in
Frame out |  |
| Power Sync
Rx/Tx
supply Pulse
Variable
U or I R / C
swap relays
internal bus bar 1
typically V /Gnd
batt
swap relays
internal bus bar 2
VT2710 | Power Sync
Rx/Tx
supply Pulse
Variable
U or I R / C |  |  |  |  |  |  |  | Variable
R / C |  |  |  |  |  |  |  |  |  |  |  |  |  |


---

14
電源制御モジュールVT7001A / VT7101 -概要-
VTシステムモジュール
ECUテスト向けに電源供給を制御
2系統での電源供給
> ECUの2端子（Terminal15、Terminal30）に電源供給
> 2台のECUに個別に電源供給
> 外部2系統および内部1系統の電源を、組み換えて接続可能
Terminal31(GND)ラインを切断可能
定格電流：70A
VT7001A
：±40V
VT7101
：±60V
電流測定（自動レンジ切替）
測定レンジ：7段階（100µA、1mA、…、100A）
リレー
ECU電源のon/off 切替え用として
ECU電源ラインの短絡発生用として
複数モードでの電源供給経路切替え用として
VTシステムとベクター製ネットワークインターフェイス間での
ハードウェア同期（sync ケーブルでの接続）

---

15
電源制御モジュールVT7001A / VT7101 -配線図-
VTシステムモジュール
2台の外部電源を制御可能

シリアル通信(RS232) あるいは

制御用電圧出力
> 出力レンジとして±10Vの範囲で外部電源の出力電圧値、最大出力電流を設定
> 制御用の任意電圧曲線の生成（例：電源供給妨害シミュレーション）
> 電気的絶縁プラグ
内部電源：3～30 V、0.5 A (30 V)、2 A (15 V)
Controllable 
Power 
Supply
Controllable 
Power 
Supply
2nd, optional
ECU
under Test
Terminal 15
Terminal 30
Terminal 31
Simplified sketch of most important 
connections to show the principle!
Control of power supplies
VT7001

---

16
汎用モジュールVT28xx
VTシステムモジュール
汎用I/O モジュール
3 種類のモジュール構成: デジタルI/O、アナログI/O、リレー
多チャンネル化コンパクトなテスト構成、1チャンネル当たりのコストを低減
VTシステムモジュールの基本機能を実装:
> CANoeでの自動設定
> 信号調整
> 測定データの前処理（RMS等）
> フロント面でのLED表示（ただし、測定用プラグはなし）
> フェニックス・コンタクト社製コネクタでの簡単な接続
典型的な応用例として
テストシステムにおけるECU以外の入出力制御を行うためにも利用可能
フォールトインジェクションを必要としない単純なECU入出力に対応

---

17
8chの電流測定
チャンネルごとに3つのシャント抵抗: 
±0.05 A、±1 A or ±16A (auto-ranging)
外付けシャント抵抗による測定も可能
チャンネルごとに追加可能(± 100mV) 
8chのアナログ入力、16 bit、250 kS/s
±60 V – シングルエンド、外部リファレンス可能
同時に電流測定
電流方向を検出
電圧測定：～60V（内部／外部基準電位）
電流測定モジュールVT2808
VTシステムモジュール

---

18
汎用アナログI/OモジュールVT2816A
VTシステムモジュール
12chアナログ入力、16bit、250kS/sec
±60V または±10V（高解像度用）
差動またはシングルエンド
8ch電流測定入力（シャント抵抗）
±5A、固定レンジ（レンジ変更不可）
アナログ電圧入力との多重利用可能
4chアナログ出力、16bit、200mA
0～28V または±10V
差動またはシングルエンド
VT2816 FPGA: FPGAプログラミング対応の
VT2816モジュールも準備

---

19
汎用デジタルI/OモジュールVT2848
VTシステムモジュール
48点デジタル入出力
シングルエンド：0～60V
入力
しきい値：0～40V
PWM測定（ch1-16の16チャンネルに限定）
出力
GND/Vbatt/Vextへのスイッチ機能
> オープンコレクタ出力、ローサイドスイッチ
> ハイサイドスイッチ
> プッシュプル
出力電流：200mA
PWM出力（ch33-48の16チャンネルに限定）
VT2848 FPGA: FPGAプログラミング対応の
VT2848モジュールも準備

---

20
汎用リレーモジュールVT2820
VTシステムモジュール
20点汎用リレー
12点リレー（常開接点：a接点）
GND/VBattへの接続用リレーあり
8点リレー（切替接点：c接点）
最大6A、ヒューズあり
Bus Bar 1a (Vbatt)
Bus Bar 1b (Gnd)
Relay I/O Pina
Fuse
Relay I/O Pinb
Relay I/O Pina
Fuse
Relay I/O Pinb
Relay I/O Pinc
Fuse
normally open relays
change over relays

---

21
スイッチマトリックスモジュールVT2832
VTシステムモジュール
主目的: 高電流下でのスイッチング
スイッチマトリックスのサイズ: 4 行x 8 列
スイッチパスごとの最大電流: 16A
最大電圧: 60V
高速なスイッチング（10 kHz程度）
チャタリングの模擬が可能
より大きい電流を流すための複数チャンネル利用も可
モジュールデザイン
より大きなスイッチマトリックスへの集約が可能
ソリッドステートリレー(SSR)を利用
メカニカルリレーと異なり磨耗がなく、耐久性が高い
最大50kHzまでの信号周波数に最適

---

22
スイッチマトリックスモジュールVT2832 – リレースイッチ
VTシステムモジュール
VT2832
Voltage + 
Current
Measurement
Voltage + 
Current
Measurement
Voltage + 
Current
Measurement
Voltage + 
Current
Measurement
Voltage + 
Current
Measurement
Voltage + 
Current
Measurement
Voltage + 
Current
Measurement
Voltage + 
Current
Measurement
Row 1
Row 2
Row 3
Row 4
Switch 1
Switch 2
Switch 3
Switch 4
Column 1
Column 2
Column 3
Column 4
Column 5
Column 6
Column 7
Column 8

---

23
リアルタイムモジュールVT6020 / VT6060
VTシステムモジュール
リアルタイム実行向けの専用PCモジュール

ソフトウェアはすべてインストール済み

Windows 10 IOT 上でCANoe RTを実行
Ethernet (100M/1Gbps)でPCに接続
EtherCAT®でVTシステムと接続（専用ポート）
ネットワークインターフェースモジュール専用ポート（PCI Express)：
最大8ポート

VT6104A / VT6204 / VT6306は、VH9100を用いて接続

VT6104B / VT6204Bは、付属ケーブルを用いて接続
前面、および背面にそれぞれ2つのUSBポート
4つのEthポート
COM Express 規格に基づいたモジュール

VT6020    : Intel® Atom CPU@1.8GHz、8GB RAM、128GB SSD
ファンレス冷却、PCIe：4ポート

VT6060
: High-performance Intel® CoreTM i7 
CPU@2.7GHz、16GB RAM、128GB SSD
アクティブ冷却、PCIe：8ポート
EtherCAT® is registered trademark and patented technology, licensed by Beckhoff Automation GmbH, Germany.

---

24
ネットワークインターフェイスモジュールVT6104B / VT6204B -概要-
VTシステムモジュール
4つの独立したチャンネルを持つネットワークインターフェイス
CAN、CAN FD、LIN、K-Line、J1708に対応
VT6204BはFlexRay（2ch）に対応
トランシーバは、別のサーブボード(piggy)に搭載
各種制御用リレーを実装
短絡、断線
終端抵抗
トランシーバ制御
（例：電源供給のon/off 切替え）
タイムスタンプのハードウェア同期
PCI Express バスを利用した接続
VT6000 付属の「PCI Express x1」
ケーブルを用いて接続
PC (notebook / desktop) PC側にPCI Expressポートが必要

---

25
ネットワークインターフェイスモジュールVT6104B / VT6204B –リレースイッチ-
VTシステムモジュール
internal Vbatt/Gnd
bus bar
termination
short circuit to
Vbatt or ground
short circuit
ECU power
bus bar
Vbatt
Gnd
internal bus bar
120Ω
CAN high / LIN / FR A BP
CAN/LIN ground
CAN low / FR A BM
n.c.
n.c.
CAN/LIN V+
channel 1 & 2 only
open wire
tranceiver 
ground
transceiver
V+
FR B BM (VT6204B only)
FR B BP (VT6204B only)
1 of 4 channels
VT6104B / VT6204B
electrically 
isolated 
transceiver 
piggy
(CAN, LIN, 
J1708, FR)
n.c.
n.c.
100Ω
100Ω


|  |  | channel 1 & 2 only |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |
|  |  | n.c. |  | 120Ω 100Ω |  |  |  |
|  |  | n.c. |  |  |  |  |  |
|  |  | n.c. |  | 100Ω |  |  |  |


---

26
2x 100BASE-TX / 1000BASE-Tチャンネル（オンボード）
piggyを搭載することで、6チャンネル増設可能
Ethernetフレーム用の高精度タイムスタンプ
複数のバスインターフェイスと同期
ハードウェア同期（1µs 精度）
2ノード間Ethernetモニタリング
100BASE-TX / 1000BASE-T と車載Ethernetチャンネル間のメ
ディアコンバージョン
複数のプロトコルに対応するハードウェアフィルター
複数の設定可能なテストアクセスポイント(TAPs) 
Monitoring TAP: PHY層で接続することで、非常に低いレイテンシの
テストモード
Stimulation TAP: MAC層を経由することで、パケットを追加で送信可能
レイヤー2 - 柔軟で変更可能なEthernetスイッチとして動作可能
接続方式: PCIe (x1) cable
EthernetインターフェイスVT6306B -概要-
VTシステムモジュール

---

27
100BASE-T1piggy 1101
VTシステムモジュール
VT6306(B)モジュール専用piggy
6x 100BASE-T1 (NXP TJA1101)
フォールトインジェクション
シグナルラインとGND / Vbatt間の短絡
チャンネル1-3：可変抵抗器による信号減衰
範囲: 
0Ω … 2555Ω 
ステップ:
5Ω

---

28
Ethernet インターフェイスVT6306B + 100BASE-T1 piggy -配線図-
VTシステムモジュール
internal bus bar 1
typically Vbatt/Gnd
internal bus bar 2
decade 
resistor
bus bar 2
short circuit
short circuit to
Vbatt or ground
(bus bar 1)
ECU power
(bus bar 1)
bus bar 2
Vbatt
Gnd
swap relays
swap relays
1 of 6 channels
line breaks
...
...
...
...
Automotive
Ethernet
Transceiver
100BASE-T1piggy 1101
channel 1-3
input or
output
ECU
VT6306B


| ... |  |
| --- | --- |


---

29
1000BASE-T1piggy 88Q2112
VTシステムモジュール
VT6306(B)モジュール専用piggy
6x 1000BASE-T1 (Marvell 88Q2112)
フォールトインジェクション
シグナルラインとGND / Vbatt間の短絡
備考
OA SIG TC12 1000BASE-T1 Interoperability Test Suite v1.2（sec. 5.1.1および7.2.1）に定める、1000BASE-T1ネットワークの信号品質（SQI）を変化させる場合は、
CANoeで制御できるサードパーティ製のハードウェアを使用し、信号線にガウシアンノイズを印加することが必要です。

---

30
Ethernet インターフェイスVT6306B + 1000BASE-T1 piggy -配線図-
VTシステムモジュール
internal bus bar 1
typically Vbatt/Gnd
internal bus bar 2
bus bar 2
short circuit
short circuit to
Vbatt or ground
(bus bar 1)
ECU power
(bus bar 1)
bus bar 2
Vbatt
Gnd
swap relays
swap relays
1 of 6 channels
line breaks
...
...
...
...
Automotive
Ethernet
Transceiver
1000BASE-T1piggy 88Q2112
input or
output
ECU
VT6306B


| ... |  |
| --- | --- |


---

31
ファクト
現状VTシステムで使わているMolex PCIeコネクタシステムの廃止と置換え
影響
VTシステムRTモジュール：VT6011、VT6051A
VTシステムネットワークインターフェイスモジュール：VT6104A、VT6204、VT6306
PCI Expressケーブル（付属品）：VT6104A、VT6204
Bressner PCIe PCインターフェイスモジュール：OSS-PCIe-HIB25-x1 (project article)
対応品
新PCIeコネクタシステム導入: Mini SAS HD SFF-8644
新ネットワークインターフェイスモジュール：VT6104B、VT6204B、VT6306B
新RTモジュール：VT6020、VT6060
新PCIe PCインターフェイス：MXH832
新PCIeケーブル（0.5m for in-rack / 1.0m for cros-rack usage）
新RTモジュールと既存ネットワークインターフェイス活用のためのアダプターVH9110
次世代PCIeコネクタシステムの変更
VTシステムモジュール
Mini SAS HD SFF-8644 connector

---

32
ケーブルアダプターVH9100
VTシステムモジュール
モチベーション
新RTモジュール(VT6020 / VT6060) における現行ネットワークインターフェイスモジュール
VT6104(A) / VT6204 / VT6306の再利用
主な機能
PCIe Gen1 MolexコネクタからGen3 MiniSAS (SFF8644) コネクタへ変換
新RTモジュール(VT6020 / VT6060) に搭載
注意: VH9100は、RTモジュール(VT6011 / VT6051A) と新ネットワークインターフェイスモジュール
(VT6104B / VT6204B / VT6306B) の接続には使用できません。
PCIe Gen1 
Molex
PCIe Gen3 
MiniSAS
Application specific
VH9100
VT6104(A)
VT6204
VT6306
VT6060
VT6020

---

33
PCIe PCインターフェイスMXH832
VTシステムモジュール
モチベーション
CAN RTラックPCと
VT6104B、VT6204B、VT6306Bの接続に
使用
主な機能
4つのPCIe Gen3 x16
コネクタシステムMiniSAS (SFF8644) 
CANoe RTラックPCと
VTシステムネットワークインターフェイス
モジュールを最大4つまで接続可能
*https://www.dolphinics.com/products/MXH832.html

---

34
VT6104B / VT6204B / VT6306B とVT60x0 の標準的な構成
VTシステムモジュール
リアルタイムシステムとしてのVTシステム
VT6020 / VT6060 + VT6104B / VT6204B / VT6306B
VT6020 / VT6060上でCANoe RT server を実行
LAN経由でPC (RT GUI client) から制御
使いやすく、ハイパフォーマンスで、信頼性の高いシステム構成
専用PCにVT6104B / VT6204B / VT6306Bを接続
リアルタイムモジュール(VT6020 / VT6060) を使用しない構成
> PC上でCANoe を実行
PC側にPCI Expressポートが必要なため、追加のハード
ウェアが必要となる
> 配線も複雑になる可能性が高い
VT6104
VT6000
VT6104
VT6104
VT6104
VT System
Ethernet TCP/IP
Ethernet Adapter
VT6104
VT6104
VT6104
VT6104
VT6104
VT6104
VT System
n PCIe Cables
EtherCAT
PCIe Cable Adapters
(PCIe Extension Cards)
Ethernet 
Adapter


|  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| VT6000 | VT6104 | VT6104 | VT6104 | VT6104 |  |  |  |  |  |  |
|  |  |  |  |  | V | T | Sys | tem |  |  |
|  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |

|  | n | PC | Ie | Cab | les |
| --- | --- | --- | --- | --- | --- |

| Eth | erCAT |
| --- | --- |

|  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| VT6104 | VT6104 | VT6104 | VT6104 | VT6104 VT6104 | V |  |  |  |  |
|  |  |  |  |  |  | T | Syste | m |  |
|  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |


---

35
拡張モジュールVT7900A
VTシステムモジュール
お客様固有のVTシステムモジュールを実現するための
ベースモジュール
お客様固有の回路基板をピギーバック上に実装
ファームウェアの必要なし、容易に構成可能
簡易的な基板としてデジタル／アナログ入出力を許可
> 4点デジタル入力、4点デジタル出力
> 4点アナログ入力（入力範囲:0～4V、分解能:8bit）
> 4点アナログ出力（出力範囲:0～4V、出力精度:40mV）
CANoeおよびVTシステムへお客様固有の回路を統合
ベクターだけでなく、お客様ご自身での回路拡張も可能
VT7900A拡張モジュール

---

36
VT7900A FPGA上に実装するパワートレインやシャシーECU向けの
ローテーションセンサーシミュレーションボード
以下のような一般的な車速センサータイプのシミュレーション：
クランクシャフト＋カムシャフトセンサーシミュレーション
システム変数による自由な歯数設定
4chのセンサーシミュレーション
最大1MHzでの電圧変調
最大300 kHzでの電流変調
ローテーションセンサーボードVT7820
VTシステムモジュール
s type
i type
v type
拡張モジュール
VT7900A FPGA
ローテーションセンサーボード
VT7820

---

37
line breaks
VT7820
1 of 4 channels
Current modulation
ECU
input
ISensor
Voltage modulation
USensor
VT7900A FPGA
short circuit
ローテーションセンサーボードVT7820 -配線図-
VTシステムモジュール
電圧変調
範囲
-12 V … 12 V
最大周波数
1 MHz
スルーレート
190 V/µs
電流変調
範囲
0 mA … 100 mA
最大周波数
300 kHz
スルーレート
250 mA/µs

---

38
ISO15118規格に対応したスマートチャージコミュニケーションの通信評価用
PWMコントロールパイロットライン通信
「電気自動車(EV)」あるいは「電気自動車充電設備(EVSE)」のシミュレーション
CANoeのシステム変数を使用した計測と刺激
パワーラインコミュニケーション(PLC)
Integrated Green PHY
> VT7970: Qualcomm QCA7000 chip set
> VT7971: Vertexcom chip set
CANoeとEthernetで接続するためのRJ45ソケット
コントロールパイロットラインの障害を模擬可能
（断線／GND短絡）
コンポーネント要素の許容差を模擬可能
ケーブルのキャパシタンスを模擬
ケーブル線間の可変抵抗を模擬
PWM信号周波数を任意に変更
Proximity Contactの接続制御と電圧計測が可能
スマートチャージコミュニケーションモジュールVT7970 / VT7971
VTシステムモジュール
拡張モジュール
VT7900A
スマートチャージコミュニケーション用
ボードVT7870 / VT7871

---

39
スマートチャージコミュニケーションモジュールVT7970 / VT7971 – 回路ブロック図
VTシステムモジュール
R1
Cs
dLAN® Green PHY 
Vg
Control Pilot (CP)
Protective Earth (PE)
High pass filter
Low pass filter
Voltage / Frequency 
measurement
Ethernet
(RJ45 connector)
EVSE

Vg刺激

High/Low電圧の変動範囲：± 15V

PWM（1kHz ± 10%、1 … 99%）

R1 可変抵抗：1k ± 3%

CS 可変キャパシタ：0 … 6.3nF（100pF刻み）
EVSE 動作モード
EV 動作モード
R2 可変抵抗：1k74 ± 3%
R3 可変抵抗：270R ± 3%
CV 可変キャパシタ：0 … 6.3nF（100pF刻み）
Control Pilot (CP)
Ground
Low pass filter
dLAN® Green PHY 
High pass filter
Cv
D
R2
R3
Voltage / Frequency 
measurement
Ethernet
(RJ45 connector)
EV

---

40
モジュール共通の特徴
VTシステムモジュール

ラック／バックプレーン
電源
エンジニアリング
まとめ
アジェンダ

---

41
バックプレーンVT8006A + VT8012A
ラック／バックプレーン
産業用EthernetプロトコルEtherCAT®を使用して、VTシステムとPCをEthernetで接続

高速、リアルタイム、低レイテンシ

標準Ethernetポートを使用専用のインターフェイスハードウェアは不要
is registered trademark and patented technology, licensed by Beckhoff Automation GmbH, Germany.
VT8006A

19インチ（ハーフサイズ:42HP）用の
バックプレーン

VTモジュール6枚までサポート

使用例
> 開発者の机上や持ち運びに適した
コンパクトなテストボックス
> 特別な用途向けのテストボックス
（例:診断通信テスト）
VT8012A

19インチ（フルサイズ:84HP）用の
バックプレーン

VTモジュール12枚までサポート

複数のバックプレーンをカスケード接続可能
→モジュール数に制限なし

使用例
> 開発者用の大きなテストボックス
> 複雑なHILテストシステム

---

42
VTシステムラック
ラック／バックプレーン
19インチDesktop Case

最大12モジュール

（高さ:5U ※換気用の隙間含）
19インチSubrack

最大12モジュール

19インチケース取付用
（高さ:4U）
19/2インチDesktop Case

最大6モジュール

（高さ:5U ※換気用の隙間含）

---

43
モジュール共通の特徴
VTシステムモジュール
ラック／バックプレーン

電源
エンジニアリング
まとめ
アジェンダ

---

44
VTシステム用電源モジュールVTC8920B
電源
VTシステム用の電源モジュール

12V固定出力のため、VTシステムへの電源電圧供給用として
使用可能

最大200W（1ラック分相当）

背面にAC電源コードを接続、前面にOn/Offスイッチを搭載

消費電力の表示

外部電源なしの評価ボックスを実現

---

45
モジュール共通の特徴
VTシステムモジュール
ラック／バックプレーン
電源

エンジニアリング
まとめ
アジェンダ

---

46
エンジニアリングサービス
エンジニアリング
各種エンジニアリングサービス提供

コンサルティングおよびトレーニング

テスト実装のためのサポート

テストシステム開発

VT FPGAモジュールの機能追加

VT7900A（FPGA）のカスタマイズ開発

テストケース実装

オンサイトサポート

…

---

47
モジュール共通の特徴
VTシステムモジュール
ラック／バックプレーン
電源
エンジニアリング

まとめ
アジェンダ

---

48
利点
まとめ
車載ECUのI/Oへ接続するために一体化されたハードウェアを実現
基本的なすべてのテスト用部品を実装（例: リレー、ディケード抵抗等）
汎用的な測定器と違い、車載ECUに特化したハードウェア
車載ECUのテスト要件（電圧、電流、低レイテンシ、高スループット等）を実現
複雑なテスト環境の配線を簡素化
セットアップ時間の最少化
CANoeによる制御:
テスト、シミュレーション、解析用にI/Oをダイレクトかつ容易に制御
スケーラブルなテスト向けソリューション:
机上で使用する小型の一般的なI/Oボックスから、実験室等での小型HILシステムまで対応
ベクターは、スマートな車載ECUテスト向けソリューションを提供します。

---

49
ベクターWebサイト「ベクター・ジャパンMember Area」から資料のダウンロードが可能
製品説明スライド（概要）
> ベクターテストソリューションのご紹介
> VTシステムのご紹介
> VTシステムの各モジュール紹介
> …
CANoeテスト機能、vTESTstudio自習用サンプル
> VTシステムを使用したvTESTstudioトレーニングテキスト、サンプル
> …
Vector Customer Portal
「ベクター・ジャパンMember Area」はベクターの製品をご利用いただいているお客様
向けの無料会員サイトです。
ご利用には、ベクターがお知らせする専用アクセスURLとパスワードが必要になります。
ご利用を希望される製品ユーザー様はこちらまでお問い合わせください。
アドバンストマニュアル
> VTシステムユーザーズマニュアル
> VTシステムCANoe.Sensor VT2710の初期設定
> …
まとめ

---

50
ベクター製品の操作方法や車載プロトコルの
トレーニングを提供
Webサイト「Vector Academy」から
トレーニングスケジュールの確認、受講申込
が可能
トレーニングコース（抜粋）
CANalyzer/CANoe測定・解析
CAPL基礎編
CANoeモデリング
vTESTstudio Fundamental
…
その他にもCANや車載Ethernetなどの
プロトコル基礎、AUTOSARなどの
トレーニングも開催
Vector Academy （トレーニング）
まとめ

---

51
ベクター動画ポータル（YouTube）にてECUテストに関する紹介動画を閲覧可能
関連動画
まとめ

---

52
© 2021. Vector Japan Co., Ltd. All rights reserved. Any distribution or copying is subject to prior written approval by Vector. V2.10 | 2022-07-25
ベクター・ジャパン株式会社
www.vector.com/jp/ja/
【営業へのお問い合わせ】
◆営業部（CSL）
（東京）
TEL: 03-4586-1808
（名古屋）TEL: 052-770-7180
E-mail: sales@jp.vector.com
【技術的なお問い合わせ】
◆カスタマーサポート部（CSP）
（東京）
TEL: 03-4586-1810
E-mail：support@jp.vector.com
※記載内容については予告なく変更されることがありますので、あらかじめご了承ください。
