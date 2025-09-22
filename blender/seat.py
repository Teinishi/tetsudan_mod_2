from lib import export_utils

# 運転席のオブジェクトをエクスポート
objs = [export_utils.get_object_by_name(f"driver_seat_1_{i}")
        for i in range(1, 5)]
export_utils.export_objects(
    objs + [export_utils.get_object_by_name("driver_seat_1_floor")],
    f"m_tns_tetsudan_driver_seat_type1.dae"
)
export_utils.export_objects(
    objs + [export_utils.get_object_by_name("driver_seat_1_wall")],
    f"m_tns_tetsudan_driver_seat_type2.dae"
)

# 座席のオブジェクトをエクスポート
export_utils.collection_export(
    "seats",
    "m_tns_tetsudan_seat_",
    origin_offset=True
)
