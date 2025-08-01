import json


def template(bar_type, bar_name, description, surfaces=None, flags=0):
    if surfaces is None:
        surfaces = []
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<definition
	name="(M)(TNS) Train Strap Bar {bar_name}"
	category="8" type="9" mass="1" value="5" tags="mod,tetsudan,train"
	flags="{flags}"
	mesh_data_name="m_tns_tetsudan_strap_bar_{bar_type}.mesh">
	<surfaces>
        {''.join([f'<surface orientation="{o}" />' for o in surfaces])}
	</surfaces>
	<buoyancy_surfaces />
	<logic_nodes />
	<voxels>
		<voxel flags="1" />
	</voxels>
	<tooltip_properties short_description="{description}" />
	<reward_properties number_rewarded="60" />
</definition>
'''


print(json.dumps({
    "m_tns_tetsudan_strap_bar_straight.xml": template(
        "straight",
        "Straight",
        "A straight section of bar for supporting train straps.",
        surfaces=[0, 1],
        flags=8
    ),
    "m_tns_tetsudan_strap_bar_t.xml": template(
        "t",
        "T-Piece",
        "A T-shaped section of bar for supporting train straps.",
        surfaces=[0, 1, 4],
    ),
    "m_tns_tetsudan_strap_bar_curve.xml": template(
        "curve",
        "Curve",
        "A curved section of bar for supporting train straps.",
        surfaces=[0, 2],
    )
}))
