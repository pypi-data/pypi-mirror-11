import math
from . core import *
from . color import *
from . primitives import *

__all__ = [
    "Threads",
]

class Helix(object):
    def __init__(self, radius, pitch, height, resolution=20, offset=(0, 0, 0), phase=0, min_limit=(None, None, None), max_limit=(None, None, None)):
        self.radius = radius
        self.pitch = pitch
        self.height = height
        self.resolution = resolution
        self.offset = offset
        self.phase = phase
        self.min_limit = min_limit
        self.max_limit = max_limit

    def __len__(self):
        return int(self.height / self.pitch * self.resolution)

    def apply_limits(self, xyz):
        ret = []
        for (val, _min, _max) in zip(xyz, self.min_limit, self.max_limit):
            if _min != None and val < _min:
                return False
            if _max != None and val > _max:
                return False
        return True

    def step_offset(self, other):
        angle_step = (2 * math.pi) / self.resolution
        angle = self.phase - other.phase
        return int(angle / angle_step)
    
    def debug(self):
        c = Cube(x=.1, y=.1, z=.1, center=True)
        objs = []
        for coord in self:
            _c = Translate(coord)(c)
            objs.append(_c)
        objs = Union()(*objs)
        return objs

    def __iter__(self):
        angle_step = (2 * math.pi) / self.resolution
        pitch_step = self.pitch / (2 * math.pi)
        (xo, yo, zo) = self.offset
        for idx in range(len(self)):
            angle = angle_step * idx + self.phase
            x = self.radius * math.cos(angle) + xo
            y = self.radius * math.sin(angle) + yo
            z = pitch_step * angle + zo
            if not self.apply_limits((x, y, z)):
                continue
            yield (x, y, z)

class ThreadProfile(object):
    def __init__(self, major_diameter, pitch):
        self.major_diameter = major_diameter
        self.pitch = pitch

    @property
    def height(self):
        return math.cos(math.radians(30)) * self.pitch

    @property
    def minor_diameter(self):
        return self.major_diameter - (1.25 * self.height)

    @property
    def pitch_diameter(self):
        return self.major_diameter - (0.75 * self.height)

    @property
    def crest_offset(self):
        return self.pitch / 8.0

    @property
    def valley_offset(self):
        return self.pitch / 4.0

    @property
    def slope_offset(self):
        return self.pitch * (3 / 16.0)

    def __iter__(self):
        z = 0
        pt1 = (self.minor_diameter, z)
        z += self.valley_offset
        pt2 = (self.minor_diameter, z)
        z += self.slope_offset
        pt3 = (self.major_diameter, z)
        z += self.crest_offset
        pt4 = (self.major_diameter, z)
        points = [pt1, pt2, pt3, pt4]
        return iter(points)

class DistanceSelect(list):
    def euclidean_distance(self, pt1, pt2):
        return math.sqrt(sum([(val1 - val2) ** 2 for (val1, val2) in zip(pt1, pt2)]))

    def nearest(self, pt1):
        def distance_sort(this, that):
            return cmp(this[2], that[2])
        distance = [(pt2, idx, self.euclidean_distance(pt1, pt2)) for (idx, pt2) in enumerate(self)]
        distance.sort(distance_sort)
        return distance[0]

class Threads(SCAD_Object):
    Defaults = {
        "resolution": {"type": RadialResolution, "default": lambda: RadialResolution(), "propagate": True},
        "diameter": {"type": float, "default": 1},
        "height": {"type": float, "default": 1},
        "pitch": {"type": float, "default": 1},
        "debug": {"type": bool, "default":  False},
    }

    def prepare_helix_list(self, hlist):
        points = []
        helix_list = []
        for helix in hlist:
            _points = list(helix)
            helix_map = {}
            helix_map["helix"] = helix
            helix_map["select"] = DistanceSelect(_points)
            helix_map["points"] = _points
            helix_map["offset"] = len(points)
            points.extend(_points)
            helix_list.append(helix_map)
        return (points, helix_list)

    def snap(self, point, z_value):
        return (point[0], point[1], z_value)

    def snap_face(self, points, face, z_value):
        for idx in face:
            points[idx] = self.snap(points[idx], z_value)

    def build_screw(self, helix_list):
        (points, helix_list) = self.prepare_helix_list(helix_list)
        bottom_idx = len(points)
        points.append((0, 0, 0))
        top_idx = len(points)
        points.append((0, 0, self.height))
        faces = []
        for (hidx, helix) in enumerate(helix_list):
            next_helix = helix_list[(hidx + 1) % len(helix_list)]
            prev_helix = helix_list[(hidx - 1) % len(helix_list)]
            offset = helix["offset"]
            next_offset = next_helix["offset"]
            prev_offset = prev_helix["offset"]
            top_flag = False
            bottom_flag = False
            for (idx, pt) in enumerate(helix["points"]):
                if idx < (len(helix["points"]) - 1):
                    (next_pt, next_idx, distance) = next_helix["select"].nearest(pt)
                    if next_pt[2] > pt[2]:
                        face = (idx + offset + 1, idx + offset, next_idx + next_offset)
                        faces.append(face)
                    else:
                        if not top_flag:
                            top_flag = True
                            previous_pt = helix["points"][idx - 1]
                            (next_pt, next_idx, distance) = next_helix["select"].nearest(previous_pt)
                            face = (idx + offset, next_idx + next_offset, top_idx)
                            #self.snap_face(points, face, self.height)
                            faces.append(face)
                        face = (idx + offset + 1, idx + offset, top_idx)
                        #self.snap_face(points, face, self.height)
                        faces.append(face)
                if idx > 0:
                    (prev_pt, prev_idx, distance) = prev_helix["select"].nearest(pt)
                    if prev_pt[2] < pt[2]:
                        face = (idx + offset - 1, idx + offset, prev_idx + prev_offset)
                        faces.append(face)
                        if not bottom_flag:
                            bottom_flag = True
                            face = (idx + offset - 1, prev_idx + prev_offset, bottom_idx)
                            #self.snap_face(points, face, 0)
                            faces.append(face)
                    else:
                        face = (idx + offset - 1, idx + offset, bottom_idx)
                        #self.snap_face(points, face, 0)
                        faces.append(face)
        return Polyhedron(points=points, faces=faces)

    def scad_debug(self, helix_list):
        colors = ["red", "green", "blue", "cyan"]
        debug = [Color(colorname=color)(helix.debug()) for (color, helix) in zip(colors, helix_list)]
        debug = Union()(*debug)
        return debug

    def scad(self):
        profile = ThreadProfile(self.diameter, self.pitch)
        min_limit = (None, None, 0)
        max_limit = (None, None, self.height)
        height = self.height + self.pitch * 2
        helix_list = []
        resolution = self.resolution.get_fragments(self.height)
        for (diameter, z_offset) in profile:
            radius = diameter / 2.0
            offset = (0, 0, z_offset - self.pitch)
            helix = Helix(radius, self.pitch, height, resolution=resolution, offset=offset, min_limit=min_limit, max_limit=max_limit)
            helix_list.append(helix)
        screw = self.build_screw(helix_list)
        if self.debug:
            debug = self.scad_debug(helix_list)
            screw = Union()(screw, debug)
        return screw
