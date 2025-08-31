# テツダン Mod 2 - TETSUDAN Train Mod 2

[Steam Workshop 公開ページ](https://steamcommunity.com/sharedfiles/filedetails/?id=3548142983)

鉄道向けパーツを追加する Stormworks の Mod です。[テツダン Mod (無印)](https://steamcommunity.com/sharedfiles/filedetails/?id=3397503269) を Component Mod 対応し、一部パーツの改良・追加を行ったものです。今後のアップデートはこちらのみ行います。

Blender から .dae をエクスポートする作業や、.dae を .mesh に変換する作業、パーツ定義 XML を Component Mod の .bin にする作業などを Python で自動化しています。

## 内容

-   枠なしガラス
-   板ブロック (1/4、1/2、3/4 厚 とそれらの組み合わせ)
-   ウェッジ、ピラミッド、逆ピラミッドの 1 ボクセルごとの分割バージョン
-   室内灯 (蛍光灯風 5 種 × 長さ 2 種、ダウンライト)
-   つり革・手すり・支柱
-   マスコン・ブレーキ・レバーサーハンドル等
-   運転席用座席 2 種
-   ロングシート・ボックスシート用座席 8 種
-   車側灯用インジケーター
-   室内壁用フック
-   VVVF 音、走行音、その他鉄道の音

### つり革

握り部の形状は 丸 (Circle)、五角形 (Pentagon)、三角形 (Triangle)、二等辺三角形 (Triangle 2) の 4 種類。丸、五角形、三角形はベルトの長さが三段階あり、短と中はベルトの留め金が露出しているタイプとカバーがかけられたタイプの 2 種類。二等辺三角形は E233 系等のタイプで短と中のみ、ベルトに六角柱のカバー。

揺れのシミュレーションは[マイコン](https://steamcommunity.com/sharedfiles/filedetails/?id=3548141507)で計算してください。

#### コンポジット入力

-   B1: ランダムオフセット
-   N1-9: 回転行列

### VVVF サウンド

-   TY GTO: 東洋 GTO (京成 3700 形未更新車)
-   TY IGBT: 東洋 IGBT (京成 3200 形)
-   MB IGBT: 三菱 IGBT (相鉄 10000 系未更新車)
-   MB SiC: 三菱 SiC-MOSFET (E235 系 1000 番台)

使用する際は別途マイコンと組み合わせて鳴らす音を制御し、惰性走行音と組み合わせてください。同時に再生できるのは 4 音声までです。

VVVF 用マイコンは今後提供予定です。

#### コンポジット入力

-   N1: 音声 1 音量
-   N2: 音声 1 ピッチ
-   N3: 音声 2 音量
-   N4: 音声 2 ピッチ
-   以降同様

### 惰性走行音

-   Train Running Sound 1
    1. 90km/h 程度 (京成 3000 形)
    2. 80km/h 程度、風切音 (京成 3700 形)
    3. 80km/h 程度、定尺レール (京成 3000 形)
-   Train Running Sound 2
    1. 80km/h 程度 (E231 系 0 番台 武蔵野線)
    2. 80km/h 程度、定尺レール (E231 系 0 番台 常磐線)
    3. 110km/h 程度 (E235 系 1000 番台)
    4. 50km/h 程度、スペノ削正 (E235 系 1000 番台)
    5. 90km/h 程度、スペノ削正 (E235 系 1000 番台 先頭車)
    6. 75km/h 程度、定尺レール (E235 系 1000 番台 グリーン車)
-   Train Running Sound Point
    1. 60km/h 程度、ポイント通過 (E235 系 1000 番台 グリーン車)

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
-   2025/08/31 v0.1.1 XML戸袋用 Porthole、4x5 Porthole を追加
