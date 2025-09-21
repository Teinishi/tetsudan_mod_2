import itertools


def template(name, mesh_name, arrow_name):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<definition name="(M)(TNS) Train Strap {name}" category="8" type="42" mass="1" value="10" flags="272" tags="mod,tetsudan,train,strap" mesh_data_name="m_tns_tetsudan_strap_bar_straight_paint_c.mesh" mesh_0_name="m_tns_tetsudan_nothing.mesh" mesh_1_name="m_tns_tetsudan_strap_{mesh_name}.mesh" mesh_editor_only_name="m_tns_tetsudan_arrow_strap_{arrow_name}.mesh">
    <surfaces>
        <surface orientation="2" />
        <surface orientation="3" />
    </surfaces>
    <buoyancy_surfaces />
	<logic_nodes>
		<logic_node label="Electric" mode="1" type="4" description="">
			<position x="0" y="0" z="0"/>
		</logic_node>
		<logic_node label="Unused" mode="1" type="1" description="This node is not used by anything.">
			<position x="0" y="0" z="1000"/>
		</logic_node>
		<logic_node label="Pivot Rotation" mode="1" type="1" description="Rotation around the bar axis. [rot]">
			<position x="0" y="0" z="0"/>
		</logic_node>
		<logic_node label="Pitch Rotation" mode="1" type="1" description="Rotation around the axis perpendicular to the bar. [2.1363rad]">
			<position x="0" y="0" z="1"/>
		</logic_node>
	</logic_nodes>
	<voxels>
		<voxel flags="1">
			<position x="0" y="0" z="0"/>
		</voxel>
		<voxel>
			<position x="0" y="0" z="1"/>
		</voxel>
	</voxels>
	<voxel_min x="0" y="0" z="0"/>
	<voxel_max x="0" y="0" z="1"/>
	<constraint_pos_parent x="0" y="0" z="0"/>
	<constraint_pos_child x="0" y="0" z="0"/>
	<tooltip_properties short_description="A hanging strap for train that can swing with number inputs."/>
</definition>
'''


definitions = {}

handle_types = [
    ("circle", "Circle"),
    ("pentagon", "Pentagon"),
    ("triangle1", "Triangle")
]

# Short, Medium
for (handle_type, handle_name), (belt_type, belt_name, arrow_name) in itertools.product(
    handle_types,
    [(1, "Short", "short"), (3, "Medium", "medium")]
):
    definitions[f"m_tns_tetsudan_strap_{handle_type}_{belt_type}_binder"] = template(
        f"{handle_name} {belt_name} 1",
        f"{handle_type}_{belt_type}_binder",
        arrow_name
    )
    definitions[f"m_tns_tetsudan_strap_{handle_type}_{belt_type}_cover"] = template(
        f"{handle_name} {belt_name} 2",
        f"{handle_type}_{belt_type}_cover",
        arrow_name
    )

# Long
for handle_type, handle_name in handle_types:
    definitions[f"m_tns_tetsudan_strap_{handle_type}_4"] = template(
        f"{handle_name} Long",
        f"{handle_type}_4",
        "long"
    )

# 六角カバー・二等辺三角形
definitions["m_tns_tetsudan_strap_triangle2_2"] = template(
    "Triangle 2 Medium",
    "triangle2_2",
    "medium"
)
definitions["m_tns_tetsudan_strap_triangle3_1"] = template(
    "Triangle 2 Short",
    "triangle3_1",
    "short"
)
