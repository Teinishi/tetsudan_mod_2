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

    def __init__(self, orientation, shape=0, rotation=0, buoyancy=None):
        self.orientation = orientation
        self.rotation = rotation
        self.shape = shape
        self.buoyancy_shape = buoyancy

    def surface_xml(self):
        xml = "<surface"
        if self.orientation != 0:
            xml += f' orientation="{self.orientation}"'
        if self.rotation != 0:
            xml += f' rotation="{self.rotation}"'
        if self.shape != 0:
            xml += f' shape="{self.shape}"'
        xml += " />"
        return xml

    def buoyancy_surface_xml(self):
        buoyancy_shape = self.buoyancy_shape or BUOYANCY_SURFACE_MAP.get(
            self.shape)
        if buoyancy_shape is not None:
            return Surface(self.orientation, buoyancy_shape, self.rotation).surface_xml()
        else:
            return ""
