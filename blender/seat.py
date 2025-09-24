from lib import export_utils

# 運転席のオブジェクトをエクスポート
objs = [
    export_utils.get_object_by_name(f"driver_seat_1_{i}")
    for i in range(1, 5)
]
dup = export_utils.duplicate_objects(objs)
export_utils.translate_objects(dup, (0, -0.125, 0))
export_utils.export_objects(
    objs + [export_utils.get_object_by_name("driver_seat_1_floor")],
    f"m_tns_tetsudan_driver_seat_type1.dae"
)
export_utils.export_objects(
    objs + [export_utils.get_object_by_name("driver_seat_1_wall1")],
    f"m_tns_tetsudan_driver_seat_type2.dae"
)
export_utils.export_objects(
    dup + [export_utils.get_object_by_name("driver_seat_1_floor")],
    f"m_tns_tetsudan_driver_seat_type3.dae"
)
export_utils.export_objects(
    dup + [export_utils.get_object_by_name("driver_seat_1_wall2")],
    f"m_tns_tetsudan_driver_seat_type4.dae"
)

# 座席のオブジェクトをエクスポート
export_utils.collection_export(
    "seats",
    "m_tns_tetsudan_seat_",
    origin_offset=True
)
