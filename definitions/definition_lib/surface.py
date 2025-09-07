BUOYANCY_SURFACE_MAP = {
    1: 1,
    2: 2,
    9: 1,
    11: 1,
    13: 1,
    14: 1,
    17: 1,
    18: 1,
}


class Surface:
    orientation: int
    rotation: int
    shape: int
    buoyancy_shape: int | None
    position: tuple[int, int, int]

    def __init__(self, orientation, shape=0, rotation=0, buoyancy=None, position=(0, 0, 0)):
        self.orientation = orientation
        self.rotation = rotation
        self.shape = shape
        self.buoyancy_shape = buoyancy
        self.position = position

    def surface_xml(self) -> str:
        xml = "<surface"

        if self.orientation != 0:
            xml += f' orientation="{self.orientation}"'

        if self.rotation != 0:
            xml += f' rotation="{self.rotation}"'

        if self.shape != 0:
            xml += f' shape="{self.shape}"'

        if self.position == (0, 0, 0):
            xml += " />"
        else:
            xml += "><position"
            for i, x in enumerate(["x", "y", "z"]):
                if self.position[i] != 0:
                    xml += f' {x}="{self.position[i]}"'
            xml += " /></surface>"

        return xml

    def buoyancy_surface_xml(self) -> str:
        buoyancy_shape = self.buoyancy_shape or \
            BUOYANCY_SURFACE_MAP.get(self.shape)
        if buoyancy_shape is not None:
            return Surface(self.orientation, buoyancy_shape, self.rotation, position=self.position).surface_xml()
        else:
            return ""


class Surfaces:
    surfaces: list[Surface]

    def __init__(self):
        self.surfaces = []

    def add(self, orientation, shape=0, rotation=0, buoyancy=None, position=(0, 0, 0)):
        self.surfaces.append(
            Surface(orientation, shape, rotation, buoyancy, position))

    def surfaces_xml(self):
        xml = "<surfaces"
        if len(self.surfaces) == 0:
            xml += " />"
        else:
            xml += ">"
            xml += "".join([s.surface_xml() for s in self.surfaces])
            xml += "</surfaces>"
        return xml

    def buoyancy_surfaces_xml(self):
        xml = "<buoyancy_surfaces"
        if len(self.surfaces) == 0:
            xml += " />"
        else:
            xml += ">"
            xml += "".join([s.buoyancy_surface_xml() for s in self.surfaces])
            xml += "</buoyancy_surfaces>"
        return xml
