from numpy import *
from PIL import Image
import time


#### objects

class GraphicsObject(object):

    def intersection(self, ray):
        return

    def colorAt(self, ray):
        return Color(255, 200, 100)



class Vector(object):

    # TODO: flexible amount of coordinates; in list

    def __init__(self, x, y, z):
        # self.x, self.y, self.z, self.point = float(x), float(y), float(z), float(point)
        self.coordinates = [x, y, z]

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

        return eval( self.vectorTempl() % tuple(output) )

    def tuple(self):
        """Returns a tuple with all components (implicit)."""
        return tuple(self.coordinates)

    def length(self): return sqrt(sum(list(map(lambda x: x**2, self.coordinates))))

    def vectorTempl(self): return "Vector(%f, %f, %f)"

    def normalize(self):
        return eval( self.vectorTempl() % tuple(
            map(lambda x: x / self.length(), self.coordinates)))

    def scale(self, t):
        return eval( self.vectorTempl() % tuple(map(lambda x: x * t, self)) )

    def __add__(self, other):
        return eval( self.vectorTempl() % tuple( list(map(lambda x,y: x+y, self, other))) )

    def __sub__(self, other): return eval( self.vectorTempl() % tuple(map(lambda x,y: x-y, self.coordinates, other)) )

    def __mul__(self, t):
        return self.scalar(t) if type(t) == Vector else self.scale(t)

    def __getitem__(self, item):
        if type(item) == int:
            return self.coordinates[item]
        elif type(item) == slice:
            return self.coordinates[item]

    def __len__(self): return len(self.coordinates)

    def __repr__(self): return self.vectorTempl() % self.tuple()

    def __truediv__(self, t): return self.scale(t)


class Triangle(GraphicsObject):

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


class Plane(GraphicsObject):

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

class Light(object):
    def __init__(self, origin, intensity, color):
        self.origin, self.intensity = origin, intensity
        self.color = color

class Sphere(GraphicsObject):

    def __init__(self, rad, center):
        self.rad, self.center = rad, center # rad:=number; center:=point

    def __repr__(self):
        return "Sphere({}, {})".format(self.rad, repr(self.center))

    def intersection(self, ray):
        co = self.center - ray.origin #co = c-o
        v = co.scalar(ray.direction)

        discriminant = v**2 - co.scalar(co) + self.rad**2

        if discriminant < 0: return None
        else: return  v - sqrt(discriminant) # nur wenn der punkt vor der camera ist; nicht hinter

    def normalAt(self, point):
        return (point - self.center).normalize()


####

class Ray(object):

    def __init__(self, origin, direction):
        self.origin, self.direction = origin, direction.normalize() #origin = point; direction = vector

    def pointAt(self, t): return self.origin + (self.direction * t)

    def __repr__(self):
        return "Ray({}, {})".format(repr(self.origin), repr(self.direction))


class Material(object):

    def __init__(self, color, ambient, ambientLvl, diffuse, diffuseLvl, spec, specLvl):
        self.color = color
        self.ambient = ambient
        self.ambientLvl = ambientLvl
        self.diffuse = diffuse
        self.diffuseLvl = diffuseLvl
        self.spec = spec
        self.specLvl = specLvl

    def color(self): return

    def __repr__(self):
        return "Material({},{},{},{},{},{},{})".format(
            repr(self.color),
            self.ambient, self.ambientLvl,
            self.diffuse, self.diffuseLvl,
            self.spec, self.specLvl)


class Camera(object):

    def __init__(self, pxX, pxY, origin, fieldOfView, up, c):
        self.origin, self.c = origin, c # points, c:=the center of an object
        self.fieldOfView = fieldOfView
        self.alpha = self.fieldOfView / 2

        self.pxX, self.pxY = pxX, pxY
        self.ratio = self.pxX / self.pxY

        self.height = 2 * tan(self.alpha)
        self.width = self.ratio * self.height

        self.up = up # global up-vector

        ce = self.c - self.origin
        self.f = ce/ce.length()
        fup = self.f.cross(up)
        self.s = fup/fup.length()

        self.u = self.s.cross(self.f)


    def __repr__(self):
        return "Camera({},{},{},{},{},{})".format(
            self.origin, self.width, self.height,
            self.fieldOfView, self.up, self.c)


class Color(object):

    def __init__(self, r, g, b):
        self.r, self.g, self.b = r, g, b

    def toRGB(self):
        return int(self.r), int(self.g), int(self.b)

    def __str__(self):
        return "Color: rgba({}, {}, {}, 1.0)".format(self.r, self.g, self.b)

    def __repr__(self):
        return "Color({},{},{})".format(self.r, self.g, self.b)


####

class Picture(object):

    def __init__(self, camera, light, objects):
        self.camera = camera
        self.objects = []
        self.objects.append(objects)
        self.image = Image.new("RGB", (self.camera.pxX, self.camera.pxY))

    def castRays(self):
        total = 0
        colorTotal = 0
        for x in range(self.camera.pxX):
            for y in range(self.camera.pxY):
                total += 1
                ray = self.calcRay(x, y)
                maxDistance = float('inf')
                color = black
                for object in self.objects:
                    hitdist = object.intersection(ray)
                    if hitdist:
                        if hitdist < maxDistance:
                            colorTotal += 1
                            maxDistance = hitdist
                            color = object.colorAt(ray)
                            s = str(total) + "-" + str(colorTotal)
                            print(s)
                            self.image.putpixel((x, y), color.toRGB())
        self.image.save("/Users/HxA/PycharmProjects/RayTracer" + "TEST_" + str(int(round(time.time() * 1000))) + ".jpg", "JPEG", quality=90)

    def sendRay(self):
        pxWidth = self.width / (self.pxX - 1)
        pxHeight = self.height / (self.pxY - 1)

        for y in range(self.pxY):
            for x in range(self.pxX):
                xComp = self.s.scale(x * pxWidth - self.camera.width / 2) # scales width of each pixel
                yComp = self.u.scale(y * pxHeight - self.camera.height / 2) # scales height of each pixel
                ray = Ray(self.origin, self.f + xComp + yComp)

    def calcRay(self, x, y):
        xComp = self.camera.s.scale(x * self.camera.pxX - self.camera.pxX / 2)  # scales width of each pixel
        yComp = self.camera.u.scale(y * self.camera.pxY - self.camera.pxY / 2)  # s# cales height of each pixel

        r = Ray(self.camera.origin, (self.camera.f + xComp )+ yComp)
        #return Ray(self.camera.origin, self.camera.f + xComp + yComp)
        return r



#### colors

black = Color(0, 0, 0)