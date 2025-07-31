import os
import sys
import importlib

dirname = os.path.dirname(os.path.realpath(__file__))

# 共通スクリプトインポート
module_path = os.path.join(dirname, "scripts")
if module_path not in sys.path:
    sys.path.append(module_path)
export_utils = importlib.import_module("export_utils")

# auto_export コレクションのオブジェクトをエクスポート
export_utils.collection_export(
    "auto_export",
    os.path.join(dirname, "exported"),
    "m_tns_tetsudan_"
)
