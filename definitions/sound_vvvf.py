import os
import glob
import json


VVVF_TYPES = [
    ("ty_igbt_1", "TY IGBT"),
    ("ty_gto_1", "TY GTO"),
    ("mb_igbt_1", "MB IGBT"),
    ("mb_sic_1", "MB SiC"),
]


def template(name):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<definition name="(M)(TNS) Train Sound {name}" category="6" type="66" lua_filename="m_tns_tetsudan_sound_vvvf.lua" mass="1" value="10" flags="0" tags="mod,tetsudan,train,sound,buzzer" mesh_data_name="meshes/component_buzzer.mesh">
    <surfaces>
        <surface orientation="0" shape="1" />
        <surface orientation="1" shape="1" />
        <surface orientation="3" shape="1" />
        <surface orientation="4" shape="1" />
        <surface orientation="5" shape="1" />
    </surfaces>
    <buoyancy_surfaces>
        <surface orientation="0" shape="1" />
        <surface orientation="1" shape="1" />
        <surface orientation="3" shape="1" />
        <surface orientation="4" shape="1" />
        <surface orientation="5" shape="1" />
    </buoyancy_surfaces>
    <logic_nodes>
        <logic_node label="Sound Data" mode="1" type="5" description="N1:Volume1, N2:Pitch1, N3:Volume2, N4:Pitch2, ..., N8: Pitch4" />
    </logic_nodes>
    <voxels>
        <voxel flags="1" />
    </voxels>
    <tooltip_properties short_description="Train motor sound."/>
    <reward_properties number_rewarded="10"/>
</definition>
'''


def lua_prefix(sound_files):
    lua = ""
    for i, file in enumerate(sound_files):
        lua += f'-- include sfx {i} "{file}"\n'
    lua += f"N = {len(sound_files)}\n"
    return lua


audio_dir = os.path.join(os.path.dirname(__file__), "..", "audio")

data = {}

for filename, name in VVVF_TYPES:
    files = glob.glob(
        f"m_tns_tetsudan_sound_{filename}_*.ogg", root_dir=audio_dir)
    files.sort()
    data[f"m_tns_tetsudan_vvvf_{filename}.xml"] = {
        "xml": template(name),
        "luaPrefix": lua_prefix(files),
    }

print(json.dumps(data))
