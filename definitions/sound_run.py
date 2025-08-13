import os
import glob
import re
import json

RUN_TYPES = {
    ("1", "1"),
    ("2", "2"),
    ("point", "Point")
}


def template(name):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<definition name="(M)(TNS) Train Running Sound {name}" category="6" type="66" lua_filename="m_tns_tetsudan_sound_run.lua" mass="1" value="10" flags="0" tags="mod,tetsudan,train,sound,buzzer" mesh_data_name="meshes/component_buzzer.mesh">
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
        <logic_node label="Sound Data" mode="1" type="5" description="N1:Index1, N2:Speed1, N3:Index2, N4:Speed2, ..., N8:Speed4" />
    </logic_nodes>
    <voxels>
        <voxel flags="1" />
    </voxels>
    <tooltip_properties short_description="Train running sound."/>
    <reward_properties number_rewarded="10"/>
</definition>
'''


def lua_prefix(sound_files: list[str], base_speed: list[tuple[int, float]]):
    lua = ""
    for i, file in enumerate(sound_files):
        lua += f'-- include sfx {i} "{file}"\n'
    lua += "BASE_SPEED = {"
    lua += ", ".join([f"[{k}] = {v}" for k, v in base_speed])
    lua += "}\n"
    return lua


audio_dir = os.path.join(os.path.dirname(__file__), "..", "audio")

pattern = re.compile(r"m_tns_tetsudan_run_([^_]+)_([^_]+)_([0-9]+).ogg")

data: dict[str, dict[str, tuple[str, float]]] = {}

for file in glob.glob("m_tns_tetsudan_run_*.ogg", root_dir=audio_dir):
    m = pattern.match(file)
    if m is None:
        continue
    name_raw, key, speed = m.groups()
    speed = float(speed)

    if name_raw not in data:
        data[name_raw] = {}
    data[name_raw][key] = (file, speed)

definitions = {}

for name_raw, name in RUN_TYPES:
    items = data.get(name_raw)
    if items is None:
        continue
    sound_files: list[str] = []
    base_speed: list[tuple[int, float]] = []
    for i, key in enumerate(sorted(items.keys())):
        item = items[key]
        sound_files.append(item[0])
        base_speed.append((i + 1, item[1]))

    definitions[f"m_tns_tetsudan_sound_run_{name_raw}.xml"] = {
        "xml": template(name),
        "luaPrefix": lua_prefix(sound_files, base_speed),
    }

print(json.dumps(definitions))
