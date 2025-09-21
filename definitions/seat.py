from definition_lib.surface import Surfaces
from definition_lib.voxel import Voxels


def template(name: str, mesh_name: str, surfaces: Surfaces, voxels: Voxels, is_not_seat=False) -> str:
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<definition name="(M)(TNS) Train Seat {name}" category="4"'''

    if is_not_seat:
        xml += f' type="9" value="{voxels.count(True) * 5}" flags="0"'
    else:
        xml += f' type="1" value="{voxels.count(True) * 10}" flags="8192"'

    xml += f' mass="{voxels.count(True)}" tags="mod,tetsudan,train,basic,seat" mesh_data_name="m_tns_tetsudan_seat_{mesh_name}.mesh">\n'
    xml += surfaces.surfaces_xml() + "\n"
    xml += surfaces.buoyancy_surfaces_xml() + "\n"
    xml += '<logic_nodes><logic_node label="Occupied" mode="0" type="0" description="Outputs an on signal if this seat is occupied by a character." /></logic_nodes>\n'
    xml += voxels.xml()
    if is_not_seat:
        xml += '<tooltip_properties short_description="A decorative component meant to be used with another train seat." />\n'
    else:
        xml += '''<seat_offset x="0.125" y="0.47" z="0.125" />
<seat_front x="0" y="0" z="1" />
<seat_up x="0" y="1" z="0" />
<seat_camera x="0" y="-0.9" z="0" />
<seat_render x="0" y="-0.85" z="-0.225" />
<tooltip_properties description="You can get in and out of the seat by interacting with it using [$[action_use_seat]]. You can place a rescued survivor in any seat by using [$[action_use_seat]] while carrying them." short_description="A passenger seat for trains." />
'''
    xml += "</definition>\n"
    return xml


def template_spacer(spacer_type, spacer_name):
    surfaces = Surfaces()
    surfaces.add(3, position=(0, 0, 0))
    surfaces.add(3, 1, position=(0, 0, -1))
    surfaces.add(5, 1, position=(0, 0, -1))
    surfaces.add(5, 1, position=(0, 1, -1))
    surfaces.add(2, position=(0, 1, -1))
    surfaces.add(0, position=(0, 0, 0))
    surfaces.add(0, position=(0, 0, -1))
    surfaces.add(0, position=(0, 1, -1))
    surfaces.add(1, position=(0, 0, 0))
    surfaces.add(1, position=(0, 0, -1))
    surfaces.add(1, position=(0, 1, -1))
    voxels = Voxels()
    voxels.add((0, 0, 0))
    voxels.add((0, 0, -1))
    voxels.add((0, 1, -1))
    return template(f"Spacer {spacer_name}", f"spacer_{spacer_type}", surfaces, voxels, is_not_seat=True)


def template_backrest(backrest_type, backrest_name):
    surfaces = Surfaces()
    surfaces.add(4, position=(0, 0, 0))
    surfaces.add(4, position=(1, 0, 0))
    surfaces.add(3, position=(0, 0, 0))
    surfaces.add(3, position=(1, 0, 0))
    surfaces.add(5, 1, position=(0, 0, 0))
    surfaces.add(5, 1, position=(1, 0, 0))
    surfaces.add(5, 1, position=(0, 1, 0))
    surfaces.add(5, 1, position=(1, 1, 0))
    surfaces.add(1, position=(0, 0, 0))
    surfaces.add(1, position=(0, 1, 0))
    surfaces.add(0, position=(1, 0, 0))
    surfaces.add(0, position=(1, 1, 0))
    voxels = Voxels()
    voxels.add((0, 0, 0))
    voxels.add((1, 0, 0))
    voxels.add((0, 1, 0))
    voxels.add((1, 1, 0))
    return template(f"Backrest {backrest_name}", f"backrest_{backrest_type}", surfaces, voxels, is_not_seat=True)


def template_no_back(seat_type, seat_name):
    surfaces = Surfaces()
    surfaces.add(3)
    surfaces.add(5)
    surfaces.add(1)
    surfaces.add(3, position=(1, 0, 0))
    surfaces.add(5, position=(1, 0, 0))
    surfaces.add(0, position=(1, 0, 0))
    voxels = Voxels()
    voxels.add((0, 0, 0))
    voxels.add((1, 0, 0))
    return template(seat_name, seat_type, surfaces, voxels)


def template_low_back(seat_type, seat_name):
    surfaces = Surfaces()
    surfaces.add(3, position=(0, 0, 0))
    surfaces.add(3, position=(1, 0, 0))
    surfaces.add(3, 1, position=(0, 0, -1))
    surfaces.add(3, 1, position=(1, 0, -1))
    surfaces.add(5, 1, position=(0, 0, -1))
    surfaces.add(5, 1, position=(0, 1, -1))
    surfaces.add(5, 1, position=(1, 0, -1))
    surfaces.add(5, 1, position=(1, 1, -1))
    surfaces.add(2, position=(0, 1, -1))
    surfaces.add(2, position=(1, 1, -1))
    surfaces.add(0, position=(1, 0, 0))
    surfaces.add(0, position=(1, 0, -1))
    surfaces.add(0, position=(1, 1, -1))
    surfaces.add(1, position=(0, 0, 0))
    surfaces.add(1, position=(0, 0, -1))
    surfaces.add(1, position=(0, 1, -1))
    voxels = Voxels()
    voxels.add((0, 0, 0))
    voxels.add((1, 0, 0))
    voxels.add((0, 0, -1))
    voxels.add((1, 0, -1))
    voxels.add((0, 1, -1))
    voxels.add((1, 1, -1))
    return template(seat_name, seat_type, surfaces, voxels)


def template_high_back(seat_type, seat_name, low_back_surface=False):
    surfaces = Surfaces()
    surfaces.add(3, position=(0, 0, 0))
    surfaces.add(3, position=(1, 0, 0))
    surfaces.add(3, 1, position=(0, 0, -1))
    surfaces.add(3, 1, position=(1, 0, -1))
    surfaces.add(5, 1, position=(0, 0, -1))
    surfaces.add(5, 1, position=(1, 0, -1))
    surfaces.add(5, 1, position=(0, 1, -1))
    surfaces.add(5, 1, position=(1, 1, -1))
    surfaces.add(5, 0 if low_back_surface else 1, position=(0, 2, -1))
    surfaces.add(5, 0 if low_back_surface else 1, position=(1, 2, -1))
    surfaces.add(1, position=(0, 0, 0))
    surfaces.add(1, position=(0, 0, -1))
    surfaces.add(1, position=(0, 1, -1))
    surfaces.add(1, position=(0, 2, -1))
    surfaces.add(0, position=(1, 0, 0))
    surfaces.add(0, position=(1, 0, -1))
    surfaces.add(0, position=(1, 1, -1))
    surfaces.add(0, position=(1, 2, -1))
    voxels = Voxels()
    voxels.add((0, 0, 0))
    voxels.add((1, 0, 0))
    voxels.add((0, 0, -1))
    voxels.add((1, 0, -1))
    voxels.add((0, 1, -1))
    voxels.add((1, 1, -1))
    voxels.add((0, 2, -1))
    voxels.add((1, 2, -1))
    return template(seat_name, seat_type, surfaces, voxels)


definitions = {
    "m_tns_tetsudan_seat_type1": template_no_back("type1", "Type 1"),
    "m_tns_tetsudan_seat_type2": template_no_back("type2", "Type 2"),
    "m_tns_tetsudan_seat_type3": template_high_back("type3", "Type 3"),
    "m_tns_tetsudan_seat_type4": template_high_back("type4", "Type 4"),
    "m_tns_tetsudan_seat_type5": template_high_back("type5", "Type 5", low_back_surface=True),
    "m_tns_tetsudan_seat_type6": template_low_back("type6", "Type 6"),
    "m_tns_tetsudan_seat_type7": template_low_back("type7", "Type 7"),
    "m_tns_tetsudan_seat_type8": template_high_back("type8", "Type 8", low_back_surface=True),
    "m_tns_tetsudan_seat_type9": template_low_back("type9", "Type 9"),
    "m_tns_tetsudan_seat_backrest_type1": template_backrest("type1", "Type 1"),
    "m_tns_tetsudan_seat_backrest_type2": template_backrest("type2", "Type 2"),
    "m_tns_tetsudan_seat_spacer_type1": template_spacer("type1", "Type 1,2"),
    "m_tns_tetsudan_seat_spacer_type6": template_spacer("type6", "Type 6"),
    "m_tns_tetsudan_seat_spacer_type7": template_spacer("type7", "Type 7"),
    "m_tns_tetsudan_seat_spacer_type9": template_spacer("type9", "Type 9")
}
