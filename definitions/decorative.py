def template(mesh_name, name, surfaces):
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<definition
    name="(M)(TNS) {name}"
    category="4" type="9" mass="1" value="1" flags="0"
    tags="mod,tetsudan,train"
    mesh_data_name="m_tns_tetsudan_{mesh_name}.mesh">
    <surfaces>'''
    for o in surfaces:
        xml += f'<surface orientation="{o}" shape="0" />'
    xml += '''</surfaces>
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
    return xml


definitions = {
    "m_tns_tetsudan_interior_hook_single": template("hook_type1_single", "Train Interior Hook (Single)", {5}),
    "m_tns_tetsudan_interior_hook_double": template("hook_type1_double", "Train Interior Hook (Double)", {5}),
    "m_tns_tetsudan_console_decorative_1": template("console_decorative_1", "Handle Type 1", {3}),
    "m_tns_tetsudan_console_decorative_2": template("console_decorative_2", "Handle Type 2", {3})
}
