from lib import export_utils

# downlight コレクションのオブジェクトをエクスポート
export_utils.collection_export("downlight", "m_tns_tetsudan_")

# 蛍光灯型のオブジェクトをエクスポート
for type_name in [f"type{i}" for i in range(1, 6)]:
    for suffix in ("_base", "_light"):
        obj = export_utils.get_object_by_name(f"{type_name}{suffix}")
        export_utils.export_objects(
            [obj],
            f"m_tns_tetsudan_interior_light_{type_name}_5{suffix}.dae",
        )

        # 長さを変更したバージョンをエクスポート
        dup_obj = export_utils.duplicate_objects([obj])[0]
        export_utils.translate_vertices(
            dup_obj, (0, -0.25, 0), lambda c: c[1] >= 0.5)
        export_utils.translate_vertices(
            dup_obj, (0, 0.25, 0), lambda c: c[1] <= -0.5)
        export_utils.export_objects(
            [dup_obj],
            f"m_tns_tetsudan_interior_light_{type_name}_3{suffix}.dae",
        )
        export_utils.delete_objects([dup_obj])
