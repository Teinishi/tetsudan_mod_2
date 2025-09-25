# テツダン Mod 2 - TETSUDAN Train Mod 2

[Steam Workshop 公開ページ](https://steamcommunity.com/sharedfiles/filedetails/?id=3548142983)

鉄道向けパーツを追加する Stormworks の Mod です。[テツダン Mod (無印)](https://steamcommunity.com/sharedfiles/filedetails/?id=3397503269) を Component Mod 対応し、一部パーツの改良・追加を行ったものです。今後のアップデートはこちらのみ行います。

Blender から .dae をエクスポートする作業や、.dae を .mesh に変換する作業、パーツ定義 XML を Component Mod の .bin にする作業などを Python で自動化しています。

## 内容

-   枠なしガラス、窓枠、窓柱、Porthole の辺と角
-   板ブロック (1/4、1/2、3/4 厚 とそれらの組み合わせ)
-   ウェッジ、ピラミッド、逆ピラミッドの 1 ボクセルごとの分割バージョン
-   室内灯 (蛍光灯風 5 種 × 長さ 2 種、ダウンライト)
-   つり革・手すり・支柱
-   マスコン・ブレーキ・レバーサーハンドル等
-   運転台用ブロック、薄型ボタン等
-   箱乗り用ハンドル
-   運転席用座席 4 種
-   ロングシート・ボックスシート用座席 9 種、ロングシート用スペーサー
-   車側灯用インジケーター
-   室内壁用フック
-   VVVF 音、走行音、その他鉄道の音

### 運転台手前の面取りパーツ (Driving Console)

T 字マスコン (Master Controller Type 4, 5) は運転台手前の面取りを表現するために、手前に少し張り出しています。マスコンの左右に対応する Driving Console パーツを繋げることができ、Driving Console パーツはプッシュ、トグル、キースイッチを組み込んだバージョンがあります。

### 箱乗り用ハンドル (Lean Out Handle)

乗務員室扉横の車体側面に埋め込み設置して、車掌が駅出発時にホーム確認ができる姿勢で掴まることができます。ミラー設置すると正しく使用できないので左右用それぞれ別パーツとして実装しています。ビークルエディタでの青矢印に L または R の文字が書かれていますので、反転設置していないことの確認に使えます。

### つり革

握り部の形状は 丸 (Circle)、五角形 (Pentagon)、三角形 (Triangle)、二等辺三角形 (Triangle 2) の 4 種類、そのうち丸、五角形、三角形はベルトの長さが三段階あり、さらに短と中はベルトの留め金が露出しているタイプとカバーがかけられたタイプの 2 種類あります。二等辺三角形は E233 系等のタイプで短と中のみで、ベルトに六角柱のカバーがついています。

揺れのシミュレーションは[マイコン](https://steamcommunity.com/sharedfiles/filedetails/?id=3548141507)で計算してください。

#### コンポジット入力

-   B1: ランダムオフセット
-   N1-9: 回転行列

### VVVF サウンド

-   TD GTO: 東洋 GTO (京成 3700 形未更新車) [マイコン](https://steamcommunity.com/sharedfiles/filedetails/?id=3574471337)
-   TD IGBT: 東洋 IGBT (京成 3200 形) [マイコン](https://steamcommunity.com/sharedfiles/filedetails/?id=3574471442)
-   ME IGBT: 三菱 IGBT (相鉄 10000 系未更新車)
-   ME SiC: 三菱 SiC-MOSFET (E235 系 1000 番台) [マイコン](https://steamcommunity.com/sharedfiles/filedetails/?id=3574470719)
-   ME GTO: 三菱 GTO (阪神 9000 系) [マイコン](https://steamcommunity.com/sharedfiles/filedetails/?id=3574470846)

使用する際は別途マイコンと組み合わせて鳴らす音を制御し、惰性走行音と組み合わせてください。同時に再生できるのは 4 音声までです。

#### コンポジット入力

-   N1: 音声 1 音量
-   N2: 音声 1 ピッチ
-   N3: 音声 2 音量
-   N4: 音声 2 ピッチ
-   以降同様

### 惰性走行音

-   Train Running Sound

| インデックス | 録音時の速度 | 録音した車両                 | 備考       |
| -----------: | :----------- | :--------------------------- | :--------- |
|            1 | 90km/h 程度  | 京成 3000 形                 |            |
|            2 | 80km/h 程度  | 京成 3700 形                 | 風切音     |
|            3 | 80km/h 程度  | 京成 3000 形                 | 定尺レール |
|            4 | 80km/h 程度  | E231 系 0 番台 武蔵野線      |            |
|            5 | 80km/h 程度  | E231 系 0 番台 常磐線        | 定尺レール |
|            6 | 110km/h 程度 | E235 系 1000 番台            |            |
|            7 | 50km/h 程度  | E235 系 1000 番台            | スペノ削正 |
|            8 | 90km/h 程度  | E235 系 1000 番台 先頭車     | スペノ削正 |
|            9 | 75km/h 程度  | E235 系 1000 番台 グリーン車 | 定尺レール |

-   Train Running Sound Point
    1: 60km/h 程度、ポイント通過 (E235 系 1000 番台 グリーン車)

| インデックス | 録音時の速度 | 録音した車両                 | 備考         |
| -----------: | :----------- | :--------------------------- | :----------- |
|            1 | 60km/h 程度  | E235 系 1000 番台 グリーン車 | ポイント通過 |

別途マイコンで路線・状況に合わせて鳴らす音を選択し、対応するコンポジットチャンネルで音量と速度を指定してください。各音声で録音したときの速度が異なるため、ピッチ指定ではなく速度指定としています。同時に再生できるのは 4 音声までです。

#### コンポジット入力

-   N1: 音声 1 音量
-   N2: 音声 1 速度 (m/s)
-   N3: 音声 2 音量
-   N4: 音声 2 速度 (m/s)
-   以降同様

### その他サウンド

-   Train Miscellaneous Sound
    1. ブレーキ摩擦音 (京成 3700 形)
    2. 停止衝動 (京成 3700 形)

同時に再生できるのは 4 音声までです。

#### コンポジット入力

-   N1: 音声 1 音量
-   N2: 音声 1 ピッチ
-   N3: 音声 2 音量
-   N4: 音声 2 ピッチ

## ビルド手順

1. .env ファイルを作成してください。.env.sample を参考に、各々の環境に合わせて設定してください。
2. blender_export.py を実行してください。
    - /blender/\*.py には、対応する .blend から .dae をエクスポートするときの手順を Python スクリプトとして記述しています。
    - blender_export.py は /blender 内の .blend と .py のペアを探し、Blender をバックグラウンドで起動してスクリプトを実行します。
    - もし同名の .py がなければ、default.py が使用され、auto_export コレクション内の各オブジェクトがエクスポートされます。
    - .dae は /blender/exported にエクスポートされます。
3. compile_components.py を実行してください。
    - /definitions 以下のパーツ定義 XML ファイルが上記の規則に従っているかチェックし、問題があれば警告を出します。
    - /definitions 以下に .py ファイルを置いて、XML を Python スクリプトで生成することもできます。この場合、XML ファイル名相当をキー、内容を値とした JSON を print (標準出力)に出力することで、そのキーをファイル名とした XML ファイルがあったときと同様の処理が行われます。似たブロックのバリエーションを自動生成することができます。
    - XML から必要な mesh を読み取って、blender/exported から .dae を取得し変換します。
    - 必要な mesh を含めて Component Mod の .bin 形式にします。このときプログラムは .tmp 以下を作業フォルダとして使用します。
    - 作成した .bin ファイルを dist/data/components に出力します。
    - .env で MOD_PATH が指定されていれば、そこにも .bin ファイルを出力します。

> [!NOTE]
> compile_components.py を実行すると、dist/data/components 以下のファイルと {MOD_PATH}/data/components 以下のファイルが削除されます。ここを直接触って編集したりファイルを置いたりすることは避けてください。

## 開発にあたる注意事項

### 命名規則

-   xml、mesh、ogg、lua ファイル等の名前は `m_tns_tetsudan_` で始めること。
-   パーツ名は `(M)(TNS)` で始めること。
-   次のタグを含めること。
    -   mod
    -   tetsudan
    -   train

以上の規則は compile_components.py によってチェックされます。

### 依存関係の取り扱い

#### メッシュ

XML を読み込み、mesh_data_name、mesh_0_name、mesh_1_name、mesh_2_name、mesh_editor_only_name 属性から読み取ったファイル名から、拡張子 .mesh を .dae に変更したものを /blender/exported から探します。.dae ファイルを mesh_compiler で .mesh に変換し、component_mod_compiler でのコンパイル対象に追加されます。

バニラに存在するファイルの場合、以上の処理はスキップされます。

#### 音声

Component Lua API から音声を使う場合、Lua ファイルに次のように記述してください。/audio から音声ファイルを探し、番号順に component_mod_compiler でのコンパイル対象に追加されます。

```lua
-- include sfx <0始まりの effect_index> "<ファイル名>"
```

バニラに存在するファイルの場合、以上の処理はスキップされます。

## 更新履歴

-   2025/08/13 v0.1.0 試用版リリース
-   2025/08/31 v0.1.1
    -   XML 戸袋用 Porthole
    -   4x5 Porthole を追加
-   2025/09/01 v0.1.2
    -   窓枠追加
    -   Porthole の辺と角を追加
-   2025/09/08 v0.1.3
    -   負荷対策のためつり革を Camera Gimbal ベースに変更
    -   座席を 1 種追加 (バケットシート)
    -   ロングシート座席スペーサーを追加
    -   窓枠のバリエーションを追加
    -   4x5 Porthole を削除
    -   乗務員ブザーを追加
    -   警笛を追加
    -   Running 音を 1 ブロックに統合
    -   VVVF メーカーの略号を変更 (TY→TD, MB→ME)
-   2025/09/16 v0.1.4
    -   ブレーキハンドルの角度範囲を 80 度～-80 度に変更
-   2025/09/24 v0.1.5
    -   運転席シートの種類を追加・当たり判定を変更 (Train Driver Seat Type 1 ～ 4)
    -   T 字マスコン 2 種を追加 (Master Controller Type 4, 5)
    -   T 字マスコンと組み合わせて、運転台手前の面取りを表現するパーツを追加 (Driving Console Type 1, 2)
    -   逆転ハンドル 2 種を追加 (Reverser Type 3, 4)
    -   箱乗り用ハンドルを追加 (Lean Out Handle)
-   2025/09/24 v0.1.6
    -   箱乗り用ハンドルの操作入力設定ができなかったのを修正 (Lean Out Handle)
-   2025/09/25 v0.1.7
    -   ME GTO の VVVF サウンドを追加
    -   VVVF サウンドマイコンを配布
