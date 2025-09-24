def template(name: str, mesh: str, description_suffix: str = "") -> str:
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<definition name="(M)(TNS) Driving Console {name}" category="2" type="9" mass="1" value="1" flags="8" tags="mod,tetsudan,train" mesh_data_name="{mesh}">
    <surfaces>
        <surface orientation="0" shape="0" />
        <surface orientation="1" shape="0" />
        <surface orientation="3" shape="1" />
        <surface orientation="5" shape="0" />
    </surfaces>
    <buoyancy_surfaces>
        <surface orientation="3" shape="1" />
    </buoyancy_surfaces>
    <logic_nodes />
    <voxels>
        <voxel flags="1" physics_shape="9">
            <physics_shape_rotation 00="-1" 01="0" 02="0" 10="0" 11="1" 12="0" 20="0" 21="0" 22="-1"/>
        </voxel>
    </voxels>
    <tooltip_properties short_description="A decorative component.{description_suffix}" />
</definition>
'''


def template_button(button_type: str, name: str, mesh: str, mesh_0: str, description_suffix: str = "") -> str:
    audio = "audio/misc/stormworks_button_press.ogg"

    if button_type == "push":
        button_type_num = 0
        logic_node_name = "Pressed"
        logic_node_description = "Outputs an on signal when you interact wtih [$[action_interact_left]]/[$[action_interact_right]], and an off signal otherwise."
        short_description = "A button that outputs an on signal when you interact with [$[action_interact_left]]/[$[action_interact_right]], and an off signal when not interacting."

    elif button_type == "toggle":
        button_type_num = 1
        logic_node_name = "Toggled"
        logic_node_description = "Outputs an on/off signal that can be toggled by interacting with [$[action_interact_left]]/[$[action_interact_right]]."
        short_description = f"A button that toggles between sending an on or off signal when you press [$[action_interact_left]]/[$[action_interact_right]] on it."

    elif button_type == "key":
        button_type_num = 2
        logic_node_name = "Activated"
        logic_node_description = "Outputs an on signal when interacting with the button for the set duration."
        short_description = "A button that outputs an on signal when you interact with [$[action_interact_left]]/[$[action_interact_right]], and an off signal when not interacting."
        audio = "audio/ui/sfx_hud_examine.ogg"

    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<definition name="(M)(TNS) Driving Console {name}" category="2" type="8" button_type="{button_type_num}" mass="1" value="1" flags="8192" tags="mod,tetsudan,train" mesh_data_name="{mesh}" mesh_0_name="{mesh_0}" audio_filename_start="{audio}">'''

    if button_type == "key":
        xml += '''
    <sfx_datas>
        <sfx_data sfx_name="button" sfx_range_inner="3.0" sfx_range_outer="6.0" sfx_priority="0.2" sfx_is_underwater_affected="true">
            <sfx_layers>
                <sfx_layer sfx_filename_start="audio/fx5/button_toggle_on.ogg" sfx_filename_loop="" sfx_filename_end="audio/fx5/button_push.ogg" sfx_gain="1.0" sfx_loop_start_time="0.75" sfx_loop_blend_duration="10.0" sfx_volume_fade_speed="1.0" sfx_pitch_fade_speed="1.0"/>
            </sfx_layers>
        </sfx_data>
        <sfx_data sfx_name="button2" sfx_range_inner="3.0" sfx_range_outer="6.0" sfx_priority="0.2" sfx_is_underwater_affected="true">
            <sfx_layers>
                <sfx_layer sfx_filename_start="audio/fx5/button_key_turn_04.ogg" sfx_filename_loop="" sfx_filename_end="" sfx_gain="1.0" sfx_loop_start_time="0.75" sfx_loop_blend_duration="10.0" sfx_volume_fade_speed="1.0" sfx_pitch_fade_speed="1.0"/>
            </sfx_layers>
        </sfx_data>
    </sfx_datas>'''
    else:
        xml += '''
    <sfx_datas>
        <sfx_data sfx_name="button" sfx_range_inner="3.0" sfx_range_outer="6.0" sfx_priority="0.2" sfx_is_underwater_affected="true">
            <sfx_layers>
                <sfx_layer sfx_filename_start="audio/misc/stormworks_button_press.ogg" sfx_filename_loop="" sfx_filename_end="" sfx_gain="1.0" sfx_loop_start_time="0.75" sfx_loop_blend_duration="10.0" sfx_volume_fade_speed="1.0" sfx_pitch_fade_speed="1.0"/>
            </sfx_layers>
        </sfx_data>
    </sfx_datas>'''

    xml += f'''
    <surfaces>
        <surface orientation="0" shape="0" />
        <surface orientation="1" shape="0" />
        <surface orientation="3" shape="1" />
        <surface orientation="5" shape="0" />
    </surfaces>
    <buoyancy_surfaces>
        <surface orientation="3" shape="1" />
    </buoyancy_surfaces>
    <logic_nodes>
        <logic_node label="{logic_node_name}" mode="0" type="0" description="{logic_node_description}" />
        <logic_node label="Electric" mode="1" type="4" description="Electrical power connection." />
    </logic_nodes>
    <voxels>
        <voxel flags="1" physics_shape="9">
            <physics_shape_rotation 00="-1" 01="0" 02="0" 10="0" 11="1" 12="0" 20="0" 21="0" 22="-1"/>
        </voxel>
    </voxels>
    <tooltip_properties short_description="{short_description}{description_suffix}" />
</definition>
'''
    return xml


definitions = {}

for i, master_controller_type in [(1, 4), (2, 5)]:
    description_suffix = f" Fits with the master controller type {master_controller_type}."
    definitions[f"m_tns_tetsudan_console_{i}.xml"] = template(
        f"Type {i}",
        f"m_tns_tetsudan_console_{i}.mesh",
        description_suffix
    )
    definitions[f"m_tns_tetsudan_console_{i}_button_push.xml"] = template_button(
        "push",
        f"Push Button Type {i}",
        f"m_tns_tetsudan_console_{i}_button_static.mesh",
        f"m_tns_tetsudan_console_{i}_button_dynamic.mesh",
        description_suffix
    )
    definitions[f"m_tns_tetsudan_console_{i}_button_toggle.xml"] = template_button(
        "toggle",
        f"Toggle Button Type {i}",
        f"m_tns_tetsudan_console_{i}_button_static.mesh",
        f"m_tns_tetsudan_console_{i}_button_dynamic.mesh",
        description_suffix
    )
    definitions[f"m_tns_tetsudan_console_{i}_button_key.xml"] = template_button(
        "key",
        f"Key Button Type {i}",
        f"m_tns_tetsudan_console_{i}_key_static.mesh",
        f"m_tns_tetsudan_console_{i}_key_dynamic.mesh",
        description_suffix
    )
