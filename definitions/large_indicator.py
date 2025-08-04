import json


def template(type_name, name):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<definition name="(M)(TNS) Large Indicator Light {name}"
	category="6" type="21" mass="1" value="20" flags="8192" tags="mod,tetsudan,train,light"
	mesh_data_name="m_tns_tetsudan_large_indicator_{type_name}_base.mesh"
	mesh_0_name="m_tns_tetsudan_large_indicator_{type_name}_light.mesh"
	light_intensity="0" light_range="1" light_ies_map="graphics/ies/ies_default.txtr" light_fov="1" light_type="0" indicator_type="1">
	<surfaces>
		<surface orientation="0" shape="1" />
		<surface orientation="1" shape="1" />
		<surface orientation="2" shape="1" />
		<surface orientation="3" shape="1" />
		<surface orientation="4" shape="1" />
		<surface orientation="5" shape="1" />
	</surfaces>
	<buoyancy_surfaces>
		<surface orientation="0" shape="1" />
		<surface orientation="1" shape="1" />
		<surface orientation="2" shape="1" />
		<surface orientation="3" shape="1" />
		<surface orientation="4" shape="1" />
		<surface orientation="5" shape="1" />
	</buoyancy_surfaces>
	<logic_nodes>
		<logic_node label="Indicator Light" mode="1" type="0" description="Switches the light on when receiving an on signal." />
		<logic_node label="Electric" mode="1" type="4" description="Electrical power connection." flags="0" />
	</logic_nodes>
	<voxels>
		<voxel flags="1" />
	</voxels>
	<light_position x="0" y="0" z="0" />
	<light_color x="1" y="1" z="1" />
	<tooltip_properties short_description="A simple light that can be used as an indicator in logic systems." />
	<reward_properties number_rewarded="4" />
</definition>
'''


print(json.dumps({
    "m_tns_tetsudan_large_indicator_type1.xml": template("type1", "Type 1"),
    "m_tns_tetsudan_large_indicator_type2.xml": template("type2", "Type 2"),
}))
