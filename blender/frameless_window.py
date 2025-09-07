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
for name, i in [
    ("corner", 1),
    ("corner", 2),
    ("corner", 3),
    ("edge", 1),
    ("edge", 2),
    ("edge", 3),
    ("pillar", 1),
    ("pillar", 2),
    ("edge_pillar", 1),
    ("edge_pillar", 2),
]:
    export_utils.export_objects(
        [
            export_utils.get_object_by_name(f"window_frame_{name}_{i}"),
            export_utils.get_object_by_name(f"window_glass_{name}")
        ],
        f"m_tns_tetsudan_window_frame_glass_{name}_{i}",
        dirname=export_path
    )
