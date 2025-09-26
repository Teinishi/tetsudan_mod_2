from definition_lib.surface import Surface

DRAGGABLE_X = 8
DRAGGABLE_Y = 16
DRAGGABLE_Z = 32


def template(name: str, mass: float, surfaces: list[Surface], mesh_name: str | None = None, arrow_name: str | None = None, physics_shape: int = 1, flags: int = 1):
    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<definition name="(M)(TNS) {name}" category="0" type="6" mass="{mass}" value="1" flags="{flags}" tags="mod,tetsudan,train,basic"{
        f' mesh_data_name="m_tns_tetsudan_{mesh_name}.mesh"' if mesh_name is not None else ""
    }{
        f' mesh_editor_only_name="m_tns_tetsudan_{arrow_name}.mesh"' if arrow_name is not None else ""
    }>
    <surfaces>{"".join([s.surface_xml() for s in surfaces])}</surfaces>
    <buoyancy_surfaces>{"".join([s.buoyancy_surface_xml() for s in surfaces])}</buoyancy_surfaces>
    <logic_nodes />
    <voxels>
        <voxel flags="1" physics_shape="{physics_shape}" />
    </voxels>
    <tooltip_properties short_description="Basic building block." />
    <reward_properties tier="0" number_rewarded="2000" />
</definition>
'''
    return xml


definitions = {
    "m_tns_tetsudan_basic_slab_0001": template(
        "Quarter Block",
        0.25,
        [Surface(0), Surface(1), Surface(3, 1), Surface(4), Surface(5)],
        "basic_slab_0001",
        arrow_name="arrow_basic_physics_9",
        physics_shape=9,
        flags=DRAGGABLE_X | DRAGGABLE_Z
    ),
    "m_tns_tetsudan_basic_slab_0010": template(
        "Quarter Block (Middle)",
        0.25,
        [Surface(0), Surface(1), Surface(4), Surface(5)],
        "basic_slab_0010",
        arrow_name="arrow_basic_physics_8",
        physics_shape=8,
        flags=DRAGGABLE_X | DRAGGABLE_Z
    ),
    "m_tns_tetsudan_basic_slab_0011": template(
        "Half Block",
        0.5,
        [Surface(0), Surface(1), Surface(3, 1), Surface(4), Surface(5)],
        "basic_slab_0011",
        arrow_name="arrow_basic_physics_8",
        physics_shape=8,
        flags=DRAGGABLE_X | DRAGGABLE_Z
    ),
    "m_tns_tetsudan_basic_slab_0101": template(
        "Double Quarter Block (A)",
        0.5,
        [Surface(0), Surface(1), Surface(3, 1), Surface(4), Surface(5)],
        "basic_slab_0101",
        arrow_name="arrow_basic_physics_1",
        physics_shape=1,
        flags=DRAGGABLE_X | DRAGGABLE_Z
    ),
    "m_tns_tetsudan_basic_slab_0110": template(
        "Half Block (Middle)",
        0.5,
        [Surface(0), Surface(1), Surface(4), Surface(5)],
        "basic_slab_0110",
        arrow_name="arrow_basic_physics_1",
        physics_shape=1,
        flags=DRAGGABLE_X | DRAGGABLE_Z
    ),
    "m_tns_tetsudan_basic_slab_0111": template(
        "Three-Quarter Block",
        0.75,
        [Surface(0), Surface(1), Surface(3, 1), Surface(4), Surface(5)],
        "basic_slab_0111",
        arrow_name="arrow_basic_physics_7",
        physics_shape=7,
        flags=DRAGGABLE_X | DRAGGABLE_Z
    ),
    "m_tns_tetsudan_basic_slab_1001": template(
        "Double Quarter Block (B)",
        0.5,
        [
            Surface(0),
            Surface(1),
            Surface(2, 1),
            Surface(3, 1),
            Surface(4),
            Surface(5)
        ],
        "basic_slab_1001",
        arrow_name="arrow_basic_physics_1",
        physics_shape=1,
        flags=DRAGGABLE_X | DRAGGABLE_Z
    ),
    "m_tns_tetsudan_basic_slab_1011": template(
        "Half + Quarter Block",
        0.75,
        [
            Surface(0),
            Surface(1),
            Surface(2, 1),
            Surface(3, 1),
            Surface(4),
            Surface(5)
        ],
        "basic_slab_1011",
        arrow_name="arrow_basic_physics_1",
        physics_shape=1,
        flags=DRAGGABLE_X | DRAGGABLE_Z
    ),
    "m_tns_tetsudan_basic_wedge1_1q": template(
        "Quarter Wedge",
        0.25,
        [
            Surface(0),
            Surface(1),
            Surface(3),
            Surface(4),
        ],
        "basic_wedge1_1q",
        physics_shape=1,
        flags=DRAGGABLE_X
    ),
    "m_tns_tetsudan_basic_wedge1_2q": template(
        "Half Wedge",
        0.25,
        [
            Surface(0),
            Surface(1),
            Surface(3),
            Surface(4),
        ],
        "basic_wedge1_2q",
        physics_shape=1,
        flags=DRAGGABLE_X
    ),
    "m_tns_tetsudan_basic_wedge2_1": template(
        "Wedge 1x2 Voxel 1",
        0.75,
        [
            Surface(0, 11, 3),
            Surface(1, 9, 1),
            Surface(3, 1),
            Surface(4, 1),
            Surface(5, buoyancy=1),
            Surface(5, 21),
        ],
        "basic_wedge2_1",
        physics_shape=4,
        flags=DRAGGABLE_X
    ),
    "m_tns_tetsudan_basic_wedge2_2": template(
        "Wedge 1x2 Voxel 2",
        0.25,
        [
            Surface(0, 12, 3),
            Surface(1, 10, 1),
            Surface(3, 1),
            Surface(4, buoyancy=1),
            Surface(5, 22),
        ],
        "basic_wedge2_2",
        physics_shape=5,
        flags=DRAGGABLE_X
    ),
    "m_tns_tetsudan_basic_pyramid2_1": template(
        "Pyramid 1x2 Voxel 1",
        0.4,
        [
            Surface(0, 11, 3),
            Surface(3, 9, 1),
            Surface(4, 2, 2),
            Surface(5),
            Surface(5, 27),
        ],
        "basic_pyramid2_1",
        physics_shape=10,
    ),
    "m_tns_tetsudan_basic_pyramid2_2": template(
        "Pyramid 1x2 Voxel 2",
        0.1,
        [
            Surface(0, 12, 3),
            Surface(3, 10, 1),
            Surface(4),
            Surface(5, 28),
        ],
        "basic_pyramid2_2",
        physics_shape=11,
    ),
    "m_tns_tetsudan_basic_invpyramid2_1": template(
        "Inverse Pyramid 1x2 Voxel 1",
        0.86,
        [
            Surface(0, 1),
            Surface(1, 9, 1),
            Surface(2, 11, 3),
            Surface(3, 1),
            Surface(4, 1),
            Surface(5, 47),
            Surface(5, buoyancy=1),
        ],
        "basic_invpyramid2_1",
        physics_shape=26,
    ),
    "m_tns_tetsudan_basic_invpyramid2_2": template(
        "Inverse Pyramid 1x2 Voxel 2",
        0.64,
        [
            Surface(0, 1),
            Surface(1, 10, 1),
            Surface(2, 12, 3),
            Surface(3, 1),
            Surface(4, buoyancy=1),
            Surface(5, 48),
            Surface(5, 2, 3),
        ],
        "basic_invpyramid2_2",
        physics_shape=27,
    ),
    "m_tns_tetsudan_basic_wedge4_1": template(
        "Wedge 1x4 Voxel 1",
        0.875,
        [
            Surface(0, 17, 3),
            Surface(1, 13, 1),
            Surface(3, 1),
            Surface(4, 1),
            Surface(5, buoyancy=1),
            Surface(5, 23),
        ],
        "basic_wedge4_1",
        physics_shape=6,
        flags=DRAGGABLE_X
    ),
    "m_tns_tetsudan_basic_wedge4_2": template(
        "Wedge 1x4 Voxel 2",
        0.625,
        [
            Surface(0, 18, 3),
            Surface(1, 14, 1),
            Surface(3, 1),
            Surface(4, buoyancy=1),
            Surface(5, buoyancy=1),
            Surface(5, 24),
        ],
        "basic_wedge4_2",
        physics_shape=7,
        flags=DRAGGABLE_X
    ),
    "m_tns_tetsudan_basic_wedge4_3": template(
        "Wedge 1x4 Voxel 3",
        0.375,
        [
            Surface(0, 19, 3),
            Surface(1, 15, 1),
            Surface(3, 1),
            Surface(4, buoyancy=1),
            Surface(5),
            Surface(5, 25),
        ],
        "basic_wedge4_3",
        physics_shape=8,
        flags=DRAGGABLE_X
    ),
    "m_tns_tetsudan_basic_wedge4_4": template(
        "Wedge 1x4 Voxel 4",
        0.125,
        [
            Surface(0, 20, 3),
            Surface(1, 16, 1),
            Surface(3, 1),
            Surface(4),
            Surface(5, 26),
        ],
        "basic_wedge4_4",
        physics_shape=9,
        flags=DRAGGABLE_X
    ),
    "m_tns_tetsudan_basic_pyramid4_1": template(
        "Pyramid 1x4 Voxel 1",
        0.57,
        [
            Surface(0, 17, 3),
            Surface(3, 13, 1),
            Surface(4, 2, 2),
            Surface(5, 29),
        ],
        "basic_pyramid4_1",
        physics_shape=12,
    ),
    "m_tns_tetsudan_basic_pyramid4_2": template(
        "Pyramid 1x4 Voxel 2",
        0.3,
        [
            Surface(0, 18, 3),
            Surface(3, 14, 1),
            Surface(4),
            Surface(5),
            Surface(5, 30),
        ],
        "basic_pyramid4_2",
        physics_shape=13,
    ),
    "m_tns_tetsudan_basic_pyramid4_3": template(
        "Pyramid 1x4 Voxel 3",
        0.11,
        [
            Surface(0, 19, 3),
            Surface(3, 15, 1),
            Surface(4),
            Surface(5),
            Surface(5, 31),
        ],
        "basic_pyramid4_3",
        physics_shape=14,
    ),
    "m_tns_tetsudan_basic_pyramid4_4": template(
        "Pyramid 1x4 Voxel 4",
        0.02,
        [
            Surface(0, 20, 3),
            Surface(3, 16, 1),
            Surface(4),
            Surface(5, 32),
        ],
        "basic_pyramid4_4",
        physics_shape=15,
    ),
    "m_tns_tetsudan_basic_invpyramid4_1": template(
        "Inverse Pyramid 1x4 Voxel 1",
        0.88,
        [
            Surface(0, 1),
            Surface(1, 13, 1),
            Surface(2, 17, 3),
            Surface(3, 1),
            Surface(4, 1),
            Surface(5, buoyancy=1),
            Surface(5, 49),
        ],
        "basic_invpyramid4_1",
        physics_shape=28,
    ),
    "m_tns_tetsudan_basic_invpyramid4_2": template(
        "Inverse Pyramid 1x4 Voxel 2",
        0.84,
        [
            Surface(0, 1),
            Surface(1, 14, 1),
            Surface(2, 18, 3),
            Surface(3, 1),
            Surface(4, buoyancy=1),
            Surface(5, buoyancy=1),
            Surface(5, 50),
        ],
        "basic_invpyramid4_2",
        physics_shape=29,
    ),
    "m_tns_tetsudan_basic_invpyramid4_3": template(
        "Inverse Pyramid 1x4 Voxel 3",
        0.72,
        [
            Surface(0, 1),
            Surface(1, 15, 1),
            Surface(2, 19, 3),
            Surface(3, 1),
            Surface(4, buoyancy=1),
            Surface(5, buoyancy=1),
            Surface(5, 51),
        ],
        "basic_invpyramid4_3",
        physics_shape=30,
    ),
    "m_tns_tetsudan_basic_invpyramid4_4": template(
        "Inverse Pyramid 1x4 Voxel 4",
        0.55,
        [
            Surface(0, 1),
            Surface(1, 16, 1),
            Surface(2, 20, 3),
            Surface(3, 1),
            Surface(4, buoyancy=1),
            Surface(5, 52),
            Surface(5, 2, 3),
        ],
        "basic_invpyramid4_4",
        physics_shape=31,
    ),
    "m_tns_tetsudan_basic_pyramid2x2_1": template(
        "Pyramid 2x2 Voxel 1",
        0.5,
        [
            Surface(0, 11, 3),
            Surface(1, 10, 1),
            Surface(2, 33),
            Surface(3, 1),
            Surface(4, 9, 2),
            Surface(5, 12, 0),
        ],
        physics_shape=16,
    ),
    "m_tns_tetsudan_basic_pyramid2x2_2": template(
        "Pyramid 2x2 Voxel 2",
        0.25,
        [
            Surface(0, 12, 3),
            Surface(2, 34),
            Surface(3, 2, 1),
            Surface(4, 10, 2),
        ],
        physics_shape=17,
    ),
    "m_tns_tetsudan_basic_pyramid2x4_1": template(
        "Pyramid 2x4 Voxel 1",
        0.9375,
        [
            Surface(0, 17, 3),
            Surface(1, 15, 1),
            Surface(2, 35),
            Surface(3, 1),
            Surface(4, 9, 2),
            Surface(5, buoyancy=1),
        ],
        "basic_pyramid2x4_1",
        physics_shape=18,
    ),
    "m_tns_tetsudan_basic_pyramid2x4_2": template(
        "Pyramid 2x4 Voxel 2",
        0.5625,
        [
            Surface(0, 18, 3),
            Surface(1, 16, 1),
            Surface(2, 36),
            Surface(3, 1),
            Surface(4, buoyancy=1),
            Surface(5, 12),
        ],
        "basic_pyramid2x4_2",
        physics_shape=19,
    ),
    "m_tns_tetsudan_basic_pyramid2x4_3": template(
        "Pyramid 2x4 Voxel 3",
        0.21875,
        [
            Surface(0, 19, 3),
            Surface(2, 37),
            Surface(3, 9, 1),
            Surface(4, 10, 2),
            Surface(5),
        ],
        "basic_pyramid2x4_3",
        physics_shape=20,
    ),
    "m_tns_tetsudan_basic_pyramid2x4_4": template(
        "Pyramid 2x4 Voxel 4",
        0.03125,
        [
            Surface(0, 20, 3),
            Surface(2, 38),
            Surface(3, 10, 1),
            Surface(4),
        ],
        "basic_pyramid2x4_4",
        physics_shape=21,
    ),
    "m_tns_tetsudan_basic_pyramid4x4_1": template(
        "Pyramid 4x4 Voxel 1",
        1.125,
        [
            Surface(0, 17, 3),
            Surface(1, 14, 1),
            Surface(2, 43),
            Surface(3, 1),
            Surface(4, 13, 2),
            Surface(5, 18),
        ],
        physics_shape=22,
    ),
    "m_tns_tetsudan_basic_pyramid4x4_2": template(
        "Pyramid 4x4 Voxel 2",
        0.75,
        [
            Surface(0, 18, 3),
            Surface(1, 15, 1),
            Surface(2, 44),
            Surface(3, 1),
            Surface(4, 14, 2),
            Surface(5, 19),
        ],
        physics_shape=23,
    ),
    "m_tns_tetsudan_basic_pyramid4x4_3": template(
        "Pyramid 4x4 Voxel 3",
        0.375,
        [
            Surface(0, 19, 3),
            Surface(1, 16, 1),
            Surface(2, 45),
            Surface(3, 1),
            Surface(4, 15, 2),
            Surface(5, 20),
        ],
        physics_shape=24,
    ),
    "m_tns_tetsudan_basic_pyramid4x4_4": template(
        "Pyramid 4x4 Voxel 4",
        0.0625,
        [
            Surface(0, 20, 3),
            Surface(2, 46),
            Surface(3, 2, 1),
            Surface(4, 16, 2),
        ],
        physics_shape=25,
    ),
    "m_tns_tetsudan_basic_invpyramid2x2_1": template(
        "Inverse Pyramid 2x2 Voxel 1",
        0.825,
        [
            Surface(0, 1),
            Surface(1, 9, 1),
            Surface(2, 54),
            Surface(2, 2, 2),
            Surface(3, 1),
            Surface(4, 1),
            Surface(5, 11),
        ],
        physics_shape=32,
    ),
    "m_tns_tetsudan_basic_invpyramid2x2_2": template(
        "Inverse Pyramid 2x2 Voxel 2",
        0.45,
        [
            Surface(0, 11, 3),
            Surface(1, 10, 1),
            Surface(2, 53),
            Surface(3, 1),
            Surface(4, 9, 2),
            Surface(5, 12),
        ],
        physics_shape=33,
    ),
    "m_tns_tetsudan_basic_invpyramid2x4_1": template(
        "Inverse Pyramid 2x4 Voxel 1",
        0.88125,
        [
            Surface(0, 1),
            Surface(1, 13, 1),
            Surface(2, 11, 3),
            Surface(2, 58),
            Surface(3, 1),
            Surface(4, 1),
            Surface(5, buoyancy=1),
        ],
        "basic_invpyramid2x4_1",
        physics_shape=34,
    ),
    "m_tns_tetsudan_basic_invpyramid2x4_2": template(
        "Inverse Pyramid 2x4 Voxel 2",
        0.76875,
        [
            Surface(0, 1),
            Surface(1, 14, 1),
            Surface(2, 12, 3),
            Surface(2, 57),
            Surface(3, 1),
            Surface(5, 11),
        ],
        "basic_invpyramid2x4_2",
        physics_shape=35,
    ),
    "m_tns_tetsudan_basic_invpyramid2x4_3": template(
        "Inverse Pyramid 2x4 Voxel 3",
        0.5625,
        [
            Surface(0, 17, 3),
            Surface(1, 15, 1),
            Surface(2, 56),
            Surface(3, 1),
            Surface(4, 9, 2),
        ],
        "basic_invpyramid2x4_3",
        physics_shape=36,
    ),
    "m_tns_tetsudan_basic_invpyramid2x4_4": template(
        "Inverse Pyramid 2x4 Voxel 4",
        0.3375,
        [
            Surface(0, 18, 3),
            Surface(1, 16, 1),
            Surface(2, 55),
            Surface(3, 1),
            Surface(5, 12),
        ],
        "basic_invpyramid2x4_4",
        physics_shape=37,
    ),
    "m_tns_tetsudan_basic_invpyramid4x4_1": template(
        "Inverse Pyramid 4x4 Voxel 1",
        0.8625,
        [
            Surface(0, 1),
            Surface(1, 13, 1),
            Surface(2, 2, 2),
            Surface(2, 66),
            Surface(3, 1),
            Surface(4, 1),
            Surface(5, 17),
        ],
        physics_shape=38,
    ),
    "m_tns_tetsudan_basic_invpyramid4x4_2": template(
        "Inverse Pyramid 4x4 Voxel 2",
        0.675,
        [
            Surface(0, 17, 3),
            Surface(1, 14, 1),
            Surface(2, 65),
            Surface(3, 1),
            Surface(4, 13, 2),
            Surface(5, 18),
        ],
        physics_shape=39,
    ),
    "m_tns_tetsudan_basic_invpyramid4x4_3": template(
        "Inverse Pyramid 4x4 Voxel 3",
        0.45,
        [
            Surface(0, 18, 3),
            Surface(1, 15, 1),
            Surface(2, 64),
            Surface(3, 1),
            Surface(4, 14, 2),
            Surface(5, 19),
        ],
        physics_shape=40,
    ),
    "m_tns_tetsudan_basic_invpyramid4x4_4": template(
        "Inverse Pyramid 4x4 Voxel 4",
        0.225,
        [
            Surface(0, 19, 3),
            Surface(1, 16, 1),
            Surface(2, 63),
            Surface(3, 1),
            Surface(4, 15, 2),
            Surface(5, 20),
        ],
        physics_shape=41,
    ),
}
