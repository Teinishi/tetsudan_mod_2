import json


def template(mesh_name, name):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<definition
	name="(M)(TNS) {name}"
	category="4" type="9" mass="1" value="1" flags="0"
	tags="mod,tetsudan,train"
	mesh_data_name="m_tns_tetsudan_{mesh_name}.mesh">
	<surfaces>
		<surface orientation="5" shape="0" />
	</surfaces>
	<buoyancy_surfaces />
	<logic_nodes />
	<voxels>
		<voxel flags="1">
			<position x="0" y="0" z="0" />
		</voxel>
	</voxels>
	<tooltip_properties short_description="A decorative component." />
</definition>
'''


print(json.dumps({
    "m_tns_tetsudan_interior_hook_single.xml": template("hook_type1_single", "Train Interior Hook (Single)"),
    "m_tns_tetsudan_interior_hook_double.xml": template("hook_type1_double", "Train Interior Hook (Double)")
}))
