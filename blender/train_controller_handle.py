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

PREFIX = "m_tns_tetsudan_controller_"

export_utils.collection_export("type1", export_path, PREFIX)
export_utils.collection_export("type2", export_path, PREFIX)
export_utils.collection_export("type3", export_path, PREFIX)
export_utils.collection_export("type5", export_path, PREFIX)
export_utils.collection_export("type6", export_path, PREFIX)

export_utils.export_objects([
    export_utils.get_object_by_name("type4_dynamic1"),
    export_utils.get_object_by_name("type4_dynamic2"),
], f"{PREFIX}type4_dynamic.dae", dirname=export_path)
