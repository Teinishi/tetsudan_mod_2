# テツダン Mod 2 - TETSUDAN Train Mod 2

鉄道向けパーツを追加する Stormworks の Mod です。テツダン Mod (無印) を Component Mod 対応し、一部パーツの改良・追加を行ったものです。今後のアップデートはこちらのみ行います。

Blender から .dae をエクスポートする作業や、.dae を .mesh に変換する作業、パーツ定義 XML を Component Mod の .bin にする作業などを Python で自動化しています。

## 内容

-   枠なしガラス
-   ハーフブロック、クォーターブロック
-   室内灯 (蛍光灯風 5 種 × 長さ 2 種、ダウンライト)
-   つり革・手すり・支柱
-   運転席用座席 2 種
-   ロングシート・ボックスシート用座席 8 種
-   車側灯用インジケーター
-   室内壁用フック

## 規則

-   xml、mesh、ogg ファイルの名前は `m_tns_tetsudan_` で始めること。
-   パーツ名は `(M)(TNS)` で始めること。
-   次のタグを含めること。
    -   mod
    -   tetsudan
    -   train

以上の規則は compile_components.py によってチェックされます。

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
