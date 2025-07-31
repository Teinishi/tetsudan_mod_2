import json


def template(light_type, light_name, length, is_rgb):
    ez = int(length / 2)
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<definition
    name="(M)(TNS) Train Interior Light {light_name} {length}{" (RGB)" if is_rgb else ""}"
    category="4" type="{38 if is_rgb else 10}" mass="3" value="{125 if is_rgb else 50}" flags="134217728" tags="mod,tetsudan,train,light"
    mesh_data_name="m_tns_tetsudan_interior_light_{light_type}_{length}_base.mesh"
    mesh_0_name="m_tns_tetsudan_interior_light_{light_type}_{length}_light.mesh"
    light_intensity="1" light_range="10" light_ies_map="" light_fov="0" light_type="0">
    <surfaces>
'''
    for i in range(0, length):
        z = -ez + i
        if i == 0:
            xml += f'<surface orientation="5"><position x="0" y="0" z="{z}"/></surface>\n'
        xml += f'<surface orientation="3"><position x="0" y="0" z="{z}"/></surface>\n'
        if i == length - 1:
            xml += f'<surface orientation="4"><position x="0" y="0" z="{z}"/></surface>\n'

    xml += f'''</surfaces>
    <buoyancy_surfaces />
    <logic_nodes>
'''
    if is_rgb:
        xml += '<logic_node label="Color Data" mode="1" type="5" description="Composite link containing the light\'s color data." />\n'
    else:
        xml += '<logic_node label="Light Switch" mode="1" type="0" description="Controls whether or not the light is switched on." />\n'

    xml += '''<logic_node label="Electric" mode="1" type="4" description="Electrical power connection." />
    </logic_nodes>
    <voxels>
'''
    for i in range(0, length):
        z = -ez + i
        xml += f'<voxel flags="1"><position x="0" y="0" z="{z}"/></voxel>\n'

    xml += f'''</voxels>
    <voxel_min x="0" y="0" z="{-ez}"/>
    <voxel_max x="0" y="0" z="{ez}"/>
    <voxel_physics_min x="0" y="0" z="{-ez}"/>
    <voxel_physics_max x="0" y="0" z="{ez}"/>
    <light_position x="0" y="0" z="0"/>
    <light_color x="1" y="1" z="1"/>
    <light_forward x="0" y="0" z="1"/>
'''
    if is_rgb:
        xml += '<tooltip_properties description="Three channels of the composite input can be used to set the red, green and blue components of the light\'s color using numbers between 0 and 1. The light can also operate in HSV mode, where the 3 inputs correspond to the hue, saturation and value (brightness) of the color between 0 and 1. The color mode and input channels can be customised by selecting this component with the select tool." short_description="An advanced light that can be controlled using a microcontroller."/>\n'
    else:
        xml += '<tooltip_properties description="" short_description="A basic light that can be controlled using an on/off signal." />\n'

    xml += '</definition>\n'
    return xml


definitions = {}
for type_num in range(1, 6):
    for length in (3, 5):
        definitions[f"m_tns_tetsudan_interior_light_type{type_num}_{length}.xml"] = template(
            light_type=f"type{type_num}",
            light_name=f"Type {type_num}",
            length=length,
            is_rgb=False
        )
        definitions[f"m_tns_tetsudan_interior_light_type{type_num}_{length}_rgb.xml"] = template(
            light_type=f"type{type_num}",
            light_name=f"Type {type_num}",
            length=length,
            is_rgb=True
        )

print(json.dumps(definitions))
