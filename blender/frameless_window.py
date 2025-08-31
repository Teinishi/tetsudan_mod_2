import os
import sys
import importlib

dirname = os.path.dirname(os.path.realpath(__file__))

# 共通スクリプトインポート
module_path = os.path.join(dirname, "scripts")
if module_path not in sys.path:
    sys.path.append(module_path)
export_utils = importlib.import_module("export_utils")

export_path = os.path.join(dirname, "exported")

# auto_export コレクションのオブジェクトをエクスポート
export_utils.collection_export(
    "auto_export",
    export_path,
    "m_tns_tetsudan_"
)

# 窓枠とガラス
export_utils.export_objects(
    [
        export_utils.get_object_by_name("window_frame_edge"),
        export_utils.get_object_by_name("window_glass_edge")
    ],
    "m_tns_tetsudan_window_frame_glass_edge",
    dirname=export_path
)
export_utils.export_objects(
    [
        export_utils.get_object_by_name("window_frame_corner"),
        export_utils.get_object_by_name("window_glass_corner")
    ],
    "m_tns_tetsudan_window_frame_glass_corner",
    dirname=export_path
)
