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

# downlight コレクションのオブジェクトをエクスポート
export_utils.auto_export("downlight", export_path, "m_tns_")

# 蛍光灯型のオブジェクトをエクスポート
for type_name in [f'type{i}' for i in range(1, 6)]:
    for suffix in ('_base', '_light'):
        obj = export_utils.get_object_by_name(f'{type_name}{suffix}')
        export_utils.export_objects([obj], os.path.join(
            export_path, f'm_tns_interior_light_{type_name}_5{suffix}.dae'))

        # 長さを変更したバージョンをエクスポート
        dup_obj = export_utils.duplicate_objects([obj])[0]
        export_utils.translate_vertices(
            dup_obj, (0, -0.25, 0), lambda c: c[1] >= 0.5)
        export_utils.translate_vertices(
            dup_obj, (0, 0.25, 0), lambda c: c[1] <= -0.5)
        export_utils.export_objects(
            [dup_obj], os.path.join(export_path, f'm_tns_interior_light_{type_name}_3{suffix}.dae'))
        export_utils.delete_objects([dup_obj])
