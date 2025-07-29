# テツダン Mod2 - TETSUDAN Train Mod 2

鉄道向けパーツを追加する Stormworks の Mod です。テツダン Mod (無印) を Component Mod 対応し、一部パーツの改良・追加を行ったものです。今後のアップデートはこちらのみ行います。

## ビルド手順

1. .env ファイルを作成してください。.env.sample の内容を参考に、各々の環境に合わせて設定してください。
2. blender_export.py を実行してください。
    - /blender/\*.py には、対応する .blend から .dae をエクスポートするときの手順を Python スクリプトとして記述しています。
    - blender_export.py は /blender 内の .blend と .py のペアを探し、Blender をバックグラウンドで起動してスクリプトを実行します。
    - .dae は /blender/exported にエクスポートされます。
