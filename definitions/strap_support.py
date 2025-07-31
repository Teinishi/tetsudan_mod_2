import json


def template(support_type, support_name, pipe_file, pipe_name, description, surfaces=None):
    if surfaces is None:
        surfaces = []
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<definition
	name="(M)(TNS) Train Strap Pipe {support_name}{pipe_name}"
	category="8" type="9" mass="1" value="5" flags="0" tags="mod,tetsudan,train"
	mesh_data_name="m_tns_tetsudan_strap_pipe_{support_type}{pipe_file}.mesh">
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
pipe_types = {
    "no_pipe": {
        "pipe_file": "",
        "pipe_name": "",
        "description2": " without a pipe.",
        "surfaces": set()
    },
    "middle": {
        "pipe_file": "_middle",
        "pipe_name": " Middle",
        "description2": " with a pipe running through it",
        "surfaces": {0, 1}
    },
    "end1": {
        "pipe_file": "_end1",
        "pipe_name": " End",
        "description2": " with a pipe terminating on it",
        "surfaces": {0}
    },
    "end2": {
        "pipe_file": "_end2",
        "pipe_name": " End (Side)",
        "description2": " with a pipe terminating on it",
        "surfaces": {4}
    }
}

definitions = {}

for support_type, support in support_types.items():
    support_name = support["support_name"]
    description1 = support["description1"]
    description3 = support["description3"]
    support_surfaces = support["surfaces"]

    for pipe_type, pipe in pipe_types.items():
        if support_type == "support_1" and pipe_type == "end2":
            continue

        pipe_file = pipe["pipe_file"]
        pipe_name = pipe["pipe_name"]
        description2 = pipe["description2"]
        pipe_surfaces = pipe["surfaces"]

        filename = f"m_tns_tetsudan_strap_pipe_{support_type}{pipe_file}.xml"
        definitions[filename] = template(
            support_type,
            support_name,
            pipe_file,
            pipe_name,
            description1 + description2 + description3,
            surfaces=list(sorted(support_surfaces | pipe_surfaces))
        )

print(json.dumps(definitions))
