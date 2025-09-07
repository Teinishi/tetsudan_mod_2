import json


def template_no_back(seat_type, seat_name):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<definition
	name="(M)(TNS) Train Seat {seat_name}"
	category="4" type="1" mass="2" value="25" flags="8192"
	tags="mod,tetsudan,train,basic,seat"
	mesh_data_name="m_tns_tetsudan_seat_{seat_type}.mesh"
	seat_pose="0" seat_health_per_sec="0">
	<surfaces>
		<surface orientation="3" shape="0">
			<position x="1" y="0" z="0" />
		</surface>
		<surface orientation="3" shape="0">
			<position x="0" y="0" z="0" />
		</surface>
		<surface orientation="5" shape="0">
			<position x="1" y="0" z="0" />
		</surface>
		<surface orientation="5" shape="0">
			<position x="0" y="0" z="0" />
		</surface>

		<surface orientation="0" shape="0">
			<position x="1" y="0" z="0" />
		</surface>
		<surface orientation="1" shape="0">
			<position x="0" y="0" z="0" />
		</surface>
	</surfaces>
	<buoyancy_surfaces />
	<logic_nodes>
		<logic_node label="Occupied" mode="0" type="0" description="Outputs an on signal if this seat is occupied by a character." flags="0">
			<position x="0" y="0" z="0" />
		</logic_node>
	</logic_nodes>
	<voxels>
		<voxel flags="1">
			<position x="0" y="0" z="0" />
		</voxel>
		<voxel flags="1">
			<position x="1" y="0" z="0" />
		</voxel>
	</voxels>
	<voxel_min x="0" y="0" z="0" />
	<voxel_max x="1" y="0" z="0" />
	<voxel_physics_min x="0" y="0" z="0" />
	<voxel_physics_max x="1" y="0" z="0" />
	<seat_offset x="0.125" y="0.47" z="0.125" />
	<seat_front x="0" y="0" z="1" />
	<seat_up x="0" y="1" z="0" />
	<seat_camera x="0" y="-0.9" z="0" />
	<seat_render x="0" y="-0.85" z="-0.225" />
	<tooltip_properties description="You can get in and out of the seat by interacting with it using [$[action_use_seat]]. You can place a rescued survivor in any seat by using [$[action_use_seat]] while carrying them." short_description="A small padded passenger seat." />
</definition>
'''


def template_low_back(seat_type, seat_name):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<definition
	name="(M)(TNS) Train Seat {seat_name}"
	category="4" type="1" mass="2" value="25" flags="8192"
	tags="mod,tetsudan,train,basic,seat"
	mesh_data_name="m_tns_tetsudan_seat_{seat_type}.mesh"
	seat_pose="0" seat_health_per_sec="0">
	<surfaces>
		<surface orientation="3" shape="0">
			<position x="1" y="0" z="0" />
		</surface>
		<surface orientation="3" shape="0">
			<position x="0" y="0" z="0" />
		</surface>
		<surface orientation="3" shape="1">
			<position x="1" y="0" z="-1" />
		</surface>
		<surface orientation="3" shape="1">
			<position x="0" y="0" z="-1" />
		</surface>
		<surface orientation="5" shape="1">
			<position x="1" y="0" z="-1" />
		</surface>
		<surface orientation="5" shape="1">
			<position x="0" y="0" z="-1" />
		</surface>
		<surface orientation="5" shape="1">
			<position x="1" y="1" z="-1" />
		</surface>
		<surface orientation="5" shape="1">
			<position x="0" y="1" z="-1" />
		</surface>
		<surface orientation="2" shape="0">
			<position x="1" y="1" z="-1" />
		</surface>
		<surface orientation="2" shape="0">
			<position x="0" y="1" z="-1" />
		</surface>

		<surface orientation="0" shape="0">
			<position x="1" y="0" z="0" />
		</surface>
		<surface orientation="0" shape="0">
			<position x="1" y="0" z="-1" />
		</surface>
		<surface orientation="0" shape="0">
			<position x="1" y="1" z="-1" />
		</surface>
		<surface orientation="1" shape="0">
			<position x="0" y="0" z="0" />
		</surface>
		<surface orientation="1" shape="0">
			<position x="0" y="0" z="-1" />
		</surface>
		<surface orientation="1" shape="0">
			<position x="0" y="1" z="-1" />
		</surface>
	</surfaces>
	<buoyancy_surfaces>
		<surface orientation="3" shape="1">
			<position x="1" y="0" z="-1" />
		</surface>
		<surface orientation="3" shape="1">
			<position x="0" y="0" z="-1" />
		</surface>
		<surface orientation="5" shape="1">
			<position x="1" y="0" z="-1" />
		</surface>
		<surface orientation="5" shape="1">
			<position x="0" y="0" z="-1" />
		</surface>
		<surface orientation="5" shape="1">
			<position x="1" y="1" z="-1" />
		</surface>
		<surface orientation="5" shape="1">
			<position x="0" y="1" z="-1" />
		</surface>
	</buoyancy_surfaces>
	<logic_nodes>
		<logic_node label="Occupied" mode="0" type="0" description="Outputs an on signal if this seat is occupied by a character." flags="0">
			<position x="0" y="0" z="0" />
		</logic_node>
	</logic_nodes>
	<voxels>
		<voxel flags="1">
			<position x="0" y="0" z="0" />
		</voxel>
		<voxel flags="1">
			<position x="1" y="0" z="0" />
		</voxel>
		<voxel flags="1">
			<position x="0" y="0" z="-1" />
		</voxel>
		<voxel flags="1">
			<position x="1" y="0" z="-1" />
		</voxel>
		<voxel flags="1">
			<position x="0" y="1" z="-1" />
		</voxel>
		<voxel flags="1">
			<position x="1" y="1" z="-1" />
		</voxel>
	</voxels>
	<voxel_min x="0" y="0" z="-1" />
	<voxel_max x="1" y="1" z="0" />
	<voxel_physics_min x="0" y="0" z="-1" />
	<voxel_physics_max x="1" y="1" z="0" />
	<seat_offset x="0.125" y="0.47" z="0.125" />
	<seat_front x="0" y="0" z="1" />
	<seat_up x="0" y="1" z="0" />
	<seat_camera x="0" y="-0.9" z="0" />
	<seat_render x="0" y="-0.85" z="-0.225" />
	<tooltip_properties description="You can get in and out of the seat by interacting with it using [$[action_use_seat]]. You can place a rescued survivor in any seat by using [$[action_use_seat]] while carrying them." short_description="A small padded passenger seat." />
</definition>
'''


def template_high_back(seat_type, seat_name, low_back_surface=False):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<definition
	name="(M)(TNS) Train Seat {seat_name}"
	category="4" type="1" mass="2" value="25" flags="8192"
	tags="mod,tetsudan,train,basic,seat"
	mesh_data_name="m_tns_tetsudan_seat_{seat_type}.mesh"
	seat_pose="0" seat_health_per_sec="0">
	<surfaces>
		<surface orientation="3" shape="0">
			<position x="1" y="0" z="0" />
		</surface>
		<surface orientation="3" shape="0">
			<position x="0" y="0" z="0" />
		</surface>
		<surface orientation="3" shape="1">
			<position x="1" y="0" z="-1" />
		</surface>
		<surface orientation="3" shape="1">
			<position x="0" y="0" z="-1" />
		</surface>
		<surface orientation="5" shape="1">
			<position x="1" y="0" z="-1" />
		</surface>
		<surface orientation="5" shape="1">
			<position x="0" y="0" z="-1" />
		</surface>
		<surface orientation="5" shape="1">
			<position x="1" y="1" z="-1" />
		</surface>
		<surface orientation="5" shape="1">
			<position x="0" y="1" z="-1" />
		</surface>
		<surface orientation="5" shape="{0 if low_back_surface else 1}">
			<position x="1" y="2" z="-1" />
		</surface>
		<surface orientation="5" shape="{0 if low_back_surface else 1}">
			<position x="0" y="2" z="-1" />
		</surface>

		<surface orientation="0" shape="0">
			<position x="1" y="0" z="0" />
		</surface>
		<surface orientation="0" shape="0">
			<position x="1" y="0" z="-1" />
		</surface>
		<surface orientation="0" shape="0">
			<position x="1" y="1" z="-1" />
		</surface>
		<surface orientation="0" shape="0">
			<position x="1" y="2" z="-1" />
		</surface>
		<surface orientation="1" shape="0">
			<position x="0" y="0" z="0" />
		</surface>
		<surface orientation="1" shape="0">
			<position x="0" y="0" z="-1" />
		</surface>
		<surface orientation="1" shape="0">
			<position x="0" y="1" z="-1" />
		</surface>
		<surface orientation="1" shape="0">
			<position x="0" y="2" z="-1" />
		</surface>
	</surfaces>
	<buoyancy_surfaces>
		<surface orientation="3" shape="1">
			<position x="1" y="0" z="-1" />
		</surface>
		<surface orientation="3" shape="1">
			<position x="0" y="0" z="-1" />
		</surface>
		<surface orientation="5" shape="1">
			<position x="1" y="0" z="-1" />
		</surface>
		<surface orientation="5" shape="1">
			<position x="0" y="0" z="-1" />
		</surface>
		<surface orientation="5" shape="1">
			<position x="1" y="1" z="-1" />
		</surface>
		<surface orientation="5" shape="1">
			<position x="0" y="1" z="-1" />
		</surface>
	</buoyancy_surfaces>
	<logic_nodes>
		<logic_node label="Occupied" mode="0" type="0" description="Outputs an on signal if this seat is occupied by a character." flags="0">
			<position x="0" y="0" z="0" />
		</logic_node>
	</logic_nodes>
	<voxels>
		<voxel flags="1">
			<position x="0" y="0" z="0" />
		</voxel>
		<voxel flags="1">
			<position x="1" y="0" z="0" />
		</voxel>
		<voxel flags="1">
			<position x="0" y="0" z="-1" />
		</voxel>
		<voxel flags="1">
			<position x="1" y="0" z="-1" />
		</voxel>
		<voxel flags="1">
			<position x="0" y="1" z="-1" />
		</voxel>
		<voxel flags="1">
			<position x="1" y="1" z="-1" />
		</voxel>
		<voxel flags="1">
			<position x="0" y="2" z="-1" />
		</voxel>
		<voxel flags="1">
			<position x="1" y="2" z="-1" />
		</voxel>
	</voxels>
	<voxel_min x="0" y="0" z="-1" />
	<voxel_max x="1" y="2" z="0" />
	<voxel_physics_min x="0" y="0" z="-1" />
	<voxel_physics_max x="1" y="2" z="0" />
	<seat_offset x="0.125" y="0.47" z="0.125" />
	<seat_front x="0" y="0" z="1" />
	<seat_up x="0" y="1" z="0" />
	<seat_camera x="0" y="-0.9" z="0" />
	<seat_render x="0" y="-0.85" z="-0.225" />
	<tooltip_properties description="You can get in and out of the seat by interacting with it using [$[action_use_seat]]. You can place a rescued survivor in any seat by using [$[action_use_seat]] while carrying them." short_description="A small padded passenger seat." />
</definition>
'''


def template_backrest(seat_type, seat_name):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<definition
	name="(M)(TNS) Train Seat {seat_name}"
	category="4" type="9" mass="1" value="10" flags="0"
	tags="mod,tetsudan,train,basic,seat"
	mesh_data_name="m_tns_tetsudan_seat_{seat_type}.mesh">
	<surfaces>
		<surface orientation="4" shape="0">
			<position x="1" y="0" z="0" />
		</surface>
		<surface orientation="4" shape="0">
			<position x="0" y="0" z="0" />
		</surface>
		<surface orientation="3" shape="0">
			<position x="1" y="0" z="0" />
		</surface>
		<surface orientation="3" shape="0">
			<position x="0" y="0" z="0" />
		</surface>
		<surface orientation="5" shape="1">
			<position x="1" y="0" z="0" />
		</surface>
		<surface orientation="5" shape="1">
			<position x="0" y="0" z="0" />
		</surface>
		<surface orientation="5" shape="1">
			<position x="1" y="1" z="0" />
		</surface>
		<surface orientation="5" shape="1">
			<position x="0" y="1" z="0" />
		</surface>
		<surface orientation="0" shape="0">
			<position x="1" y="0" z="0" />
		</surface>
		<surface orientation="0" shape="0">
			<position x="1" y="1" z="0" />
		</surface>
		<surface orientation="1" shape="0">
			<position x="0" y="0" z="0" />
		</surface>
		<surface orientation="1" shape="0">
			<position x="0" y="1" z="0" />
		</surface>
	</surfaces>
	<buoyancy_surfaces>
		<surface orientation="5" shape="1">
			<position x="1" y="0" z="0" />
		</surface>
		<surface orientation="5" shape="1">
			<position x="0" y="0" z="0" />
		</surface>
		<surface orientation="5" shape="1">
			<position x="1" y="1" z="0" />
		</surface>
		<surface orientation="5" shape="1">
			<position x="0" y="1" z="0" />
		</surface>
	</buoyancy_surfaces>
	<logic_nodes>
	</logic_nodes>
	<voxels>
		<voxel flags="1">
			<position x="0" y="0" z="0" />
		</voxel>
		<voxel flags="1">
			<position x="1" y="0" z="0" />
		</voxel>
		<voxel flags="1">
			<position x="0" y="1" z="0" />
		</voxel>
		<voxel flags="1">
			<position x="1" y="1" z="0" />
		</voxel>
	</voxels>
	<voxel_min x="0" y="0" z="0" />
	<voxel_max x="1" y="1" z="0" />
	<voxel_physics_min x="0" y="0" z="0" />
	<voxel_physics_max x="1" y="1" z="0" />
	<tooltip_properties description="" short_description="A decorative component meant to be used with another train seat." />
</definition>
'''


print(json.dumps({
    "m_tns_tetsudan_seat_type1.xml": template_no_back("type1", "Type 1"),
    "m_tns_tetsudan_seat_type2.xml": template_no_back("type2", "Type 2"),
    "m_tns_tetsudan_seat_type3.xml": template_high_back("type3", "Type 3"),
    "m_tns_tetsudan_seat_type4.xml": template_high_back("type4", "Type 4"),
    "m_tns_tetsudan_seat_type5.xml": template_high_back("type5", "Type 5", low_back_surface=True),
    "m_tns_tetsudan_seat_type6.xml": template_low_back("type6", "Type 6"),
    "m_tns_tetsudan_seat_type7.xml": template_low_back("type7", "Type 7"),
    "m_tns_tetsudan_seat_type8.xml": template_high_back("type8", "Type 8", low_back_surface=True),
    "m_tns_tetsudan_seat_type9.xml": template_low_back("type9", "Type 9"),
    "m_tns_tetsudan_seat_backrest_type1.xml": template_backrest("backrest_type1", "Backrest Type 1"),
    "m_tns_tetsudan_seat_backrest_type2.xml": template_backrest("backrest_type2", "Backrest Type 2")
}))
