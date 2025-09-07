def _tuple_min(a: tuple[int, int, int], b: tuple[int, int, int]) -> tuple[int, int, int]:
    return (min(a[0], b[0]), min(a[1], b[1]), min(a[2], b[2]))


def _tuple_max(a: tuple[int, int, int], b: tuple[int, int, int]) -> tuple[int, int, int]:
    return (max(a[0], b[0]), max(a[1], b[1]), max(a[2], b[2]))


class Voxel:
    position: tuple[int, int, int]
    has_physics: bool

    def __init__(self, position: tuple[int, int, int] = (0, 0, 0), has_physics: bool = True):
        self.position = position
        self.has_physics = has_physics

    def voxel_xml(self):
        flags = 1 if self.has_physics else 0

        xml = "<voxel"
        if flags != 0:
            xml += f' flags="{flags}"'
        if self.position == (0, 0, 0):
            xml += " />"
        else:
            xml += "><position"
            for i, x in enumerate(["x", "y", "z"]):
                if self.position[i] != 0:
                    xml += f' {x}="{self.position[i]}"'
            xml += " /></voxel>"

        return xml


class Voxels:
    voxels: list[Voxel]

    def __init__(self):
        self.voxels = []

    def add(self, position: tuple[int, int, int] = (0, 0, 0), has_physics: bool = True):
        self.voxels.append(Voxel(position, has_physics))

    def count(self, only_physics=False) -> int:
        n = 0
        for v in self.voxels:
            if not only_physics or v.has_physics:
                n += 1
        return n

    def voxels_xml(self) -> str:
        xml = "<voxels"
        if len(self.voxels) == 0:
            xml += " />"
        else:
            xml += ">"
            xml += "".join([s.voxel_xml() for s in self.voxels])
            xml += "</voxels>"
        return xml

    def bounding_box_xml(self) -> str:
        voxel_min: tuple[int, int, int] = (0, 0, 0)
        voxel_max: tuple[int, int, int] = (0, 0, 0)
        voxel_physics_min: tuple[int, int, int] = (0, 0, 0)
        voxel_physics_max: tuple[int, int, int] = (0, 0, 0)
        for v in self.voxels:
            voxel_min = _tuple_min(voxel_min, v.position)
            voxel_max = _tuple_max(voxel_min, v.position)
            if v.has_physics:
                voxel_physics_min = _tuple_min(voxel_physics_min, v.position)
                voxel_physics_max = _tuple_max(voxel_physics_min, v.position)

        return "".join([f'<{tag} x="{p[0]}" y="{p[1]}" z="{p[2]}" />' for tag, p in [
            ("voxel_min", voxel_min),
            ("voxel_max", voxel_max),
            ("voxel_physics_min", voxel_physics_min),
            ("voxel_physics_max", voxel_physics_max)
        ]])

    def xml(self) -> str:
        return self.voxels_xml() + self.bounding_box_xml()
