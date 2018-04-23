from numpy import *
from math import *

#### objects

class Vector(object):

    # TODO: flexible amount of coordinates; in list

    def __init__(self, x, y, z):
        # self.x, self.y, self.z, self.point = float(x), float(y), float(z), float(point)
        self.coordinates = [float(x), float(y), float(z)]

    def scalar(self, vector): return sum(list(map(lambda x, y: x*y, self, vector)))

    def cross(self, vector):
        vector1 = self.tuple()
        vector2 = vector.tuple()

        output = []

        for n in range(len(vector)):
            for i in range(len(vector)):
                if i != n:
                    j = 1
                    for j in range(j, len(vector) - i):
                        if i+j != n:
                            break

                    sum = (vector1[i] * vector2[i+j]) - (vector1[i+j] * vector2[i])
                    output.append(sum)
                    break

        return eval(self.vectorTempl() % tuple(output))

    def tuple(self):
        """Returns a tuple with all components (implicit)."""
        return tuple(self.coordinates)

    def length(self): return sqrt(sum(list(map(lambda x: x**2, self.coordinates))))

    def vectorTempl(self): return "Vector(%f, %f, %f)"

    def normalize(self):
        return eval( self.vectorTempl() % tuple(
            map(lambda x: x / self.length(), self.coordinates)))

    def scale(self, t):
        return tuple(map(lambda x: x * t, self))

    def __add__(self, other):
        return self.vectorTempl() % tuple( list(map(lambda x,y: x+y, self, other)))

    def __sub__(self, other): return self.vectorTempl() % tuple(map(lambda x,y: x-y, self.coordinates, other))

    def __mul__(self, t):
        if type(t) == Vector:
            return self.scalar(t)

        return self.scale(t)

    def __getitem__(self, item):
        if type(item) == int:
            return self.coordinates[item]
        elif type(item) == slice:
            return self.coordinates[item]

    def __len__(self): return len(self.coordinates)

    def __repr__(self): return self.vectorTempl() % self.tuple()

    def __truediv__(self, t):
        return self.scale(t)


class Triangle(object):

    def __init__(self, a, b, c):
        self.a, self.b, self.c = a, b, c # points a, b and c
        ab = self.b - self.a # vector from a to b
        ac = self.c - self.a # vector from a to c

    def normal(self):
        return self.ab.cross(self.ac).normalize()

    def intersection(self, ray):
        w = ray.origin - self.a
        dv = ray.direction.cross(self.ac)
        dvxab = dv.scalar(self.ab) # d•v x b-a

        if dvxab == 0.0: return None

        wxu = w.cross(self.ab)

        r = dv.scalar(w) / dvxab
        s = wxu.scalar(ray.direction) / dvxab

        if 0 <= r <= 1 and 0 <= s <= 1 and r+s <= 1:
            return wxu.scalar(self.ac) / dvxab

        return None

    def __repr__(self): return "Triangle({}, {}, {})".format(repr(self.a), repr(self.b), repr(self.c))

class Plane(object):

    def __init__(self, point, normal):
        self.point, self.normal = point, normal.normalize()

    def intersection(self, ray):
        op_n = (ray.origin - self.point).scalar(self.normal)
        d_n = ray.direction.scalar(self.normal)

        if d_n: return -(op_n/d_n)
        return None

    def normalAt(self): return self.normal

    def __repr__(self):
        return "Plane({},{})".format(repr(self.point), repr(self.normal))

class Sphere(object):

    def __init__(self, rad, center):
        self.rad, self.center = rad, center # rad:=number; center:=point

    def __repr__(self):
        return "Sphere({}, {})".format(self.rad, repr(self.center))

    def intersection(self, ray):
        co = self.center - ray.origin #co = c-o
        v = co.cross(ray.direction)

        discriminant = v**2 - co.scalar(co) + self.rad**2

        if discriminant < 0: return None
        else: return  v - sqrt(discriminant) # nur wenn der punkt vor der camera ist; nicht hinter

    def normalAt(self, point):
        return (point - self.center).normalize()


####

class Ray(object):

    def __init(self, origin, direction):
        self.origin, self.direction = origin, direction.normalize() #origin = point; direction = vector

    def pointAt(self, t): return self.origin + (self.direction * t)

    def __repr__(self):
        return "Ray({}, {})".format(repr(self.origin), repr(self.direction))

class Material(object):

    def __init__(self, r, g, b, ambient, ambientLvl, diffuse, diffuseLvl, spec, specLvl):
        self.r, self.g, self.b = r, g, b
        self.ambient = ambient
        self.ambientLvl = ambientLvl
        self.diffuse = diffuse
        self.diffuseLvl = diffuseLvl
        self.spec = spec
        self.specLvl = specLvl

    def color(self): return

    def __repr__(self):
        return "Material({},{},{},{},{},{},{},{},{})".format(
            self.r, self.g, self.b,
            self.ambient, self.ambientLvl,
            self.diffuse, self.diffuseLvl,
            self.spec, self.specLvl)

class Camera(object):

    def __init__(self, origin, width, height, fieldOfView, up, focus):
        self.origin = origin  # point
        self.width, self.height = width, height
        self.fieldOfView = fieldOfView
        self.c = focus
        self.up = up  # the center of an object

        ce = self.c - self.origin
        self.f = ce/ce.length()
        fup = self.f.cross(up)
        self.s = fup/fup.length()

        u = self.s.cross(self.f)

    def __repr__(self):
        return "Camera({},{},{},{},{},{})".format(
            self.origin, self.width, self.height,
            self.fieldOfView, self.up, self.c)

    def ratio(self): return self.width / self.height


####

if __name__ == "__main__":
    v0 = Vector(2, 3, 4)
    v1 = Vector(3, 6, 2)

    v0 = Vector(1, 2, 3)
    v1 = Vector(2, 1, 3)

    v0 = Vector(1, -2, 1)
    v1 = Vector(4, 3, 0)

    print(v0, v1)
    print(v0.length(), v1.length())
    print(v0.tuple(), v1.tuple())
    print(v0.cross(v1))
    print(v0.scalar(v1))

    print("Hess'che", v0.normalize())

    print("DIVISION", v0 /4)

    print("ADD:", (v0 + v1))

    t = Triangle(3, 2, 4)

    print(t)