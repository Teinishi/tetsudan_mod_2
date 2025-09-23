from definition_lib.surface import Surface


def template(
    name: str,
    mesh: str,
    mesh_editor_only: str,
    surfaces: list[Surface],
    seat_pose: int = 6,
    seat_offset: tuple[float, float, float] = (0.0, -0.5, -0.5),
    seat_front: tuple[float, float, float] = (0.0, 0.0, 1.0),
    seat_up: tuple[float, float, float] = (0.0, 1.0, 0.0),
    seat_camera: tuple[float, float, float] = (0.0, -0.25, 0.0),
    seat_render: tuple[float, float, float] = (0.0, -0.3, 0.0)
):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<definition name="(M)(TNS) {name}" category="1" type="1" mass="1" value="50" flags="8192" tags="mod,tetsudan,train,basic,seat,control,pilot" mesh_data_name="m_tns_tetsudan_{mesh}.mesh" mesh_0_name="meshes/component_pilot_seat_hat_headset.mesh" mesh_1_name="meshes/component_pilot_seat_hat_pilot.mesh" mesh_2_name="meshes/component_pilot_seat_hat_helmet.mesh" mesh_editor_only_name="m_tns_tetsudan_{mesh_editor_only}.mesh" seat_pose="{seat_pose}">
    <surfaces>{"".join([s.surface_xml() for s in surfaces])}</surfaces>
    <buoyancy_surfaces>{"".join([s.buoyancy_surface_xml() for s in surfaces])}</buoyancy_surfaces>
    <logic_nodes>
        <logic_node label="Seat data" mode="0" type="5" description="Outputs the axis, hotkey and occupied data from the helm. (On/Off 1+ : Hotkeys) (On/Off 31 : Trigger) (On/Off 32 : Occupied) (Value 1 : [$[action_left]]/[$[action_right]]) (Value 2 : [$[action_up]]/[$[action_down]]) (Value 3 : [$[action_pedal_left]]/[$[action_pedal_right]]) (Value 4 : [$[action_throttle_up]]/[$[action_throttle_down]]) (Value 9 : Look X)  (Value 10 : Look Y)" />
        <logic_node label="Headset Video" mode="1" type="6" description="Displays video UI overlay on a helmet mounted display." />
    </logic_nodes>
    <voxels>
        <voxel flags="1" />
    </voxels>
    <voxel_min x="0" y="0" z="0"/>
    <voxel_max x="0" y="0" z="0"/>
    <voxel_physics_min x="0" y="0" z="0"/>
    <voxel_physics_max x="0" y="0" z="0"/>
    <seat_offset x="{seat_offset[0]}" y="{seat_offset[1]}" z="{seat_offset[2]}"/>
    <seat_front x="{seat_front[0]}" y="{seat_front[1]}" z="{seat_front[2]}"/>
    <seat_up x="{seat_up[0]}" y="{seat_up[1]}" z="{seat_up[2]}"/>
    <seat_camera x="{seat_camera[0]}" y="{seat_camera[1]}" z="{seat_camera[2]}"/>
    <seat_render x="{seat_render[0]}" y="{seat_render[1]}" z="{seat_render[2]}"/>
    <tooltip_properties description="You can get in and out of the position by interacting with it using [$[action_use_seat]]." short_description="A compact control handle."/>
</definition>
'''


definitions = {
    "m_tns_tetsudan_lean_out_handle_l.xml": template(
        "Lean Out Handle (Left)",
        "crew_door_handle_1_l",
        "arrow_crew_door_handle_l",
        [Surface(0, 1), Surface(1), Surface(2, 1),
         Surface(3, 1), Surface(4, 1), Surface(5)],
        seat_offset=(0.375, -0.5, -0.5),
        seat_camera=(-0.6, -0.25, 0.0),
        seat_render=(-0.6, -0.3, 0.0)
    ),
    "m_tns_tetsudan_lean_out_handle_r.xml": template(
        "Lean Out Handle (Right)",
        "crew_door_handle_1_r",
        "arrow_crew_door_handle_r",
        [Surface(0), Surface(1, 1), Surface(2, 1),
         Surface(3, 1), Surface(4, 1), Surface(5)],
        seat_offset=(-0.375, -0.5, -0.5),
        seat_camera=(0.6, -0.25, 0.0),
        seat_render=(0.6, -0.3, 0.0)
    )
}
