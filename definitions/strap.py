import itertools
import json


def template(name, mesh_name):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<definition name="(M)(TNS) Train Strap {name}" category="8" type="66" lua_filename="m_tns_tetsudan_strap.lua" mass="1" value="10" flags="32" tags="mod,tetsudan,train,strap" mesh_data_name="m_tns_tetsudan_strap_bar_straight.mesh" mesh_0_name="m_tns_tetsudan_strap_{mesh_name}.mesh">
    <surfaces>
        <surface orientation="4" />
        <surface orientation="5" />
    </surfaces>
    <buoyancy_surfaces />
    <logic_nodes>
        <logic_node label="Rotation Data" mode="1" type="5" description="N1-9: Rotation matrix, B1: Random offset" />
    </logic_nodes>
    <voxels>
        <voxel flags="1" />
    </voxels>
    <tooltip_properties short_description="A hanging strap for train that can swing with a composite input."/>
    <reward_properties number_rewarded="10"/>
</definition>
'''


definitions = {}

handle_types = [
    ("circle", "Circle"),
    ("pentagon", "Pentagon"),
    ("triangle1", "Triangle")
]

# Short, Medium
for (handle_type, handle_name), (belt_type, belt_name) in itertools.product(
    handle_types,
    [(1, "Short"), (3, "Medium")]
):
    definitions[f"m_tns_tetsudan_strap_{handle_type}_{belt_type}_binder.xml"] = template(
        f"{handle_name} {belt_name} 1",
        f"{handle_type}_{belt_type}_binder"
    )
    definitions[f"m_tns_tetsudan_strap_{handle_type}_{belt_type}_cover.xml"] = template(
        f"{handle_name} {belt_name} 2",
        f"{handle_type}_{belt_type}_cover"
    )

# Long
for handle_type, handle_name in handle_types:
    definitions[f"m_tns_tetsudan_strap_{handle_type}_4.xml"] = template(
        f"{handle_name} Long",
        f"{handle_type}_4"
    )

# 六角カバー・二等辺三角形
definitions[f"m_tns_tetsudan_strap_triangle2_2.xml"] = template(
    f"Triangle 2 Medium",
    f"triangle2_2"
)
definitions[f"m_tns_tetsudan_strap_triangle3_1.xml"] = template(
    f"Triangle 2 Short",
    f"triangle3_1"
)

print(json.dumps(definitions))
