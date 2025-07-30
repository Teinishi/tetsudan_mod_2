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

# 運転席のオブジェクトをエクスポート
objs = [export_utils.get_object_by_name(f'driver_seat_1_{i}')
        for i in range(1, 5)]
export_utils.export_objects(
    objs + [export_utils.get_object_by_name('driver_seat_1_floor')],
    os.path.join(export_path, f'm_tns_train_driver_seat_type1.dae')
)
export_utils.export_objects(
    objs + [export_utils.get_object_by_name('driver_seat_1_wall')],
    os.path.join(export_path, f'm_tns_train_driver_seat_type2.dae')
)

# 座席のオブジェクトをエクスポート
export_utils.auto_export(
    "seats",
    export_path,
    "m_tns_train_seat_",
    origin_offset=True
)
