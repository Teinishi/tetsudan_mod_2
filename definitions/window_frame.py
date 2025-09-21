from definition_lib.surface import Surface

DRAGGABLE_X = 8
DRAGGABLE_Y = 16
DRAGGABLE_Z = 32


def template(name, mesh_name, arrow_name, surfaces: list[Surface], flags=0):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<definition name="(M)(TNS) {name}" category="15" type="6" mass="1" value="5" flags="{flags}" tags="mod,tetsudan,train,basic,window" mesh_data_name="m_tns_tetsudan_{mesh_name}.mesh" mesh_editor_only_name="m_tns_tetsudan_{arrow_name}.mesh">
    <surfaces>{"".join([s.surface_xml() for s in surfaces])}</surfaces>
    <buoyancy_surfaces>{"".join([s.buoyancy_surface_xml() for s in surfaces])}</buoyancy_surfaces>
	<logic_nodes />
	<voxels>
		<voxel flags="1" physics_shape="0" />
	</voxels>
	<tooltip_properties short_description="Modular window piece." />
	<reward_properties number_rewarded="4" />
</definition>
'''


definitions = {
    "m_tns_tetsudan_window_frame_corner_1": template(
        "Window Frame Corner 1",
        "window_frame_glass_corner_1",
        "arrow_framed_window_corner",
        [Surface(0), Surface(1, buoyancy=1), Surface(2),
         Surface(3, 1), Surface(4), Surface(5, 1)],
    ),
    "m_tns_tetsudan_window_frame_corner_2": template(
        "Window Frame Corner 2",
        "window_frame_glass_corner_2",
        "arrow_framed_window_corner",
        [Surface(1, buoyancy=1), Surface(2),
         Surface(3), Surface(4), Surface(5)],
    ),
    "m_tns_tetsudan_window_frame_corner_3": template(
        "Window Frame Corner 3",
        "window_frame_glass_corner_3",
        "arrow_framed_window_corner",
        [Surface(1, buoyancy=1), Surface(2),
         Surface(3), Surface(4), Surface(5)],
    ),
    "m_tns_tetsudan_window_frame_edge_1": template(
        "Window Frame Edge 1",
        "window_frame_glass_edge_1",
        "arrow_framed_window_edge",
        [Surface(0), Surface(1, buoyancy=1), Surface(2),
         Surface(3, 1), Surface(4), Surface(5)],
        flags=DRAGGABLE_Z
    ),
    "m_tns_tetsudan_window_frame_edge_2": template(
        "Window Frame Edge 2",
        "window_frame_glass_edge_2",
        "arrow_framed_window_edge",
        [Surface(1, buoyancy=1), Surface(2),
         Surface(3), Surface(4), Surface(5)],
        flags=DRAGGABLE_Z
    ),
    "m_tns_tetsudan_window_frame_edge_3": template(
        "Window Frame Edge 3",
        "window_frame_glass_edge_3",
        "arrow_framed_window_edge",
        [Surface(1, buoyancy=1), Surface(2),
         Surface(3), Surface(4), Surface(5)],
        flags=DRAGGABLE_Z
    ),
    "m_tns_tetsudan_window_frame_pillar_1": template(
        "Window Frame Pillar 1",
        "window_frame_glass_pillar_1",
        "arrow_framed_window_pillar",
        [Surface(1, buoyancy=1), Surface(2),
         Surface(3), Surface(4), Surface(5)],
        flags=DRAGGABLE_Y
    ),
    "m_tns_tetsudan_window_frame_pillar_2": template(
        "Window Frame Pillar 2",
        "window_frame_glass_pillar_2",
        "arrow_framed_window_pillar",
        [Surface(1, buoyancy=1), Surface(2),
         Surface(3), Surface(4), Surface(5)],
        flags=DRAGGABLE_Y
    ),
    "m_tns_tetsudan_window_frame_edge_pillar_1": template(
        "Window Frame Edge Pillar 1",
        "window_frame_glass_edge_pillar_1",
        "arrow_framed_window_edge_pillar",
        [Surface(0), Surface(1, buoyancy=1), Surface(2),
         Surface(3, 1), Surface(4), Surface(5)],
        flags=DRAGGABLE_Z
    ),
    "m_tns_tetsudan_window_frame_edge_pillar_2": template(
        "Window Frame Edge Pillar 2",
        "window_frame_glass_edge_pillar_2",
        "arrow_framed_window_edge_pillar",
        [Surface(1, buoyancy=1), Surface(2),
         Surface(3), Surface(4), Surface(5)],
        flags=DRAGGABLE_Z
    )
}
