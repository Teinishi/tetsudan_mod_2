from lib import export_utils

handle_l = [export_utils.get_object_by_name("handle_1_l")]
export_utils.export_objects(
    handle_l,
    "m_tns_tetsudan_crew_door_handle_1_l.dae"
)
handle_r = export_utils.duplicate_objects(handle_l)
export_utils.scale_objects(handle_r, (-1, 1, 1))
export_utils.flip_normals(handle_r)
export_utils.export_objects(
    handle_r,
    "m_tns_tetsudan_crew_door_handle_1_r.dae"
)
