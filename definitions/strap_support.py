import json


def template(support_type, support_name, bar_file, bar_name, description, surfaces=None):
    if surfaces is None:
        surfaces = []
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<definition
	name="(M)(TNS) Train Strap {support_name}{bar_name}"
	category="8" type="9" mass="1" value="5" flags="0" tags="mod,tetsudan,train"
	mesh_data_name="m_tns_tetsudan_strap_{support_type}{bar_file}.mesh">
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


support_types = {
    "support_1": {
        "support_name": "Support 1",
        "description1": "The lowest segment of handrail support",
        "description3": ".",
        "surfaces": {2}
    },
    "support_2": {
        "support_name": "Support 2",
        "description1": "The second segment of handrail support",
        "description3": ". This is meant to be on top of Support 1.",
        "surfaces": {2, 3}
    },
    "support_3": {
        "support_name": "Support 3",
        "description1": "The third segment of handrail support",
        "description3": ". This is meant to be on top of Support 2.",
        "surfaces": {2, 3}
    }
}
bar_types = {
    "no_bar": {
        "bar_file": "",
        "bar_name": "",
        "description2": " without a bar.",
        "surfaces": set()
    },
    "middle": {
        "bar_file": "_middle",
        "bar_name": " Middle",
        "description2": " with a bar running through it",
        "surfaces": {0, 1}
    },
    "end1": {
        "bar_file": "_end1",
        "bar_name": " End",
        "description2": " with a bar terminating on it",
        "surfaces": {0}
    },
    "end2": {
        "bar_file": "_end2",
        "bar_name": " End (Side)",
        "description2": " with a bar terminating on it",
        "surfaces": {4}
    }
}

definitions = {}

for support_type, support in support_types.items():
    support_name = support["support_name"]
    description1 = support["description1"]
    description3 = support["description3"]
    support_surfaces = support["surfaces"]

    for bar_type, bar in bar_types.items():
        if support_type == "support_1" and bar_type == "end2":
            continue

        bar_file = bar["bar_file"]
        bar_name = bar["bar_name"]
        description2 = bar["description2"]
        bar_surfaces = bar["surfaces"]

        filename = f"m_tns_tetsudan_strap_bar_{support_type}{bar_file}.xml"
        definitions[filename] = template(
            support_type,
            support_name,
            bar_file,
            bar_name,
            description1 + description2 + description3,
            surfaces=list(sorted(support_surfaces | bar_surfaces))
        )

print(json.dumps(definitions))
