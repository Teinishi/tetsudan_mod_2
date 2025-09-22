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

handle_l = [export_utils.get_object_by_name("handle_1_l")]
export_utils.export_objects(
    handle_l,
    "m_tns_tetsudan_crew_door_handle_1_l.dae",
    dirname=export_path
)
handle_r = export_utils.duplicate_objects(handle_l)
export_utils.scale_objects(handle_r, (-1, 1, 1))
export_utils.flip_normals(handle_r)
export_utils.export_objects(
    handle_r,
    "m_tns_tetsudan_crew_door_handle_1_r.dae",
    dirname=export_path
)
