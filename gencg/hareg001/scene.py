from numpy import arccos, cos, tan, sqrt
from numpy import linalg
import re

from gencg.hareg001 import vector
from gencg.hareg001.color import *


class Origin:

	def __init__(self, *components, x=0, y=0, z=0):
		self.components = [x, y, z]
		if len(components) > 0: self.components = components[0:3]


class Vector(vector.Vector):

	def __init__(self, *components, x=0, y=0, z=0):
		super().__init__(components[:], x=x, y=y, z=z)

	def __mul__(self, other):
		if type(other) in (int, float):
			return self.scale(other)
		elif type(other) == Vector:
			return self.scalar(other)
		elif type(other) in (list, tuple):
			return self.scalar(Vector(other))

	def className(self): return

	def length(self):
		return sum([x**2 for x in self])**(1/2)

	def scalar(self, vector): return linalg.linalg.dot(self, vector)

	def scale(self, t): return Vector([x * t for x in self])

	def cross(self, vector):
		"""Calculates the cross product of the vector (self) and another given vector (vector)."""
		e = (0,) * len(vector)
		v1 = self
		v2 = vector
		output = []

		for n in range(len(vector)):
			for i in range(len(vector)):
				if i != n:
					for j in range(1, len(vector) - i):
						if i + j != n: break

					output.append((v1[i] * v2[i + j]) - (v1[i + j] * v2[i]))
					break
		return Vector(output)

	def normalize(self): return self / self.length()


class Ray:

	def __init__(self, origin, direction):
		self.origin = origin
		self._direction_orig = direction
		self.direction = self._direction_orig.normalize()

	def __repr__(self): return "Ray(" + str(self) + ")"

	def __str__(self): return str(self.origin) + ", " + str(self._direction_orig)

	def pointAt(self, t): return self.origin + self.direction * t if type(t) in (int, float) else None


class GraphicsObject(object):

	def __init__(self, origin, mat):
		self.origin = origin
		self.mat = mat  # material

	def intersection(self, ray): return

	def normalAt(self, point): return

	def colorAt(self, ray): return


class Sphere(GraphicsObject):

	def __init__(self, center, radius, mat=black):
		super().__init__(center, mat)
		self.radius = radius

	def __repr__(self):
		return "Sphere({},{},{})".format(repr(self.origin), self.radius, repr(self.mat))

	def intersection(self, ray):
		co = self.origin - ray.origin  # co = c-o
		v = co.scalar(ray.direction)

		discriminant = v ** 2 - co.scalar(co) + self.radius ** 2

		if discriminant < 0:
			return None
		else:  # nur wenn der punkt vor der camera ist; nicht hinter
			return v - sqrt(discriminant)

	def normalAt(self, point):
		return (point - self.origin).normalize()


class Triangle(GraphicsObject):

	def __init__(self, a, b, c, mat=black):
		super().__init__(self.calcMidpoint((a, b, c)), mat)  # saves the origin in super
		self.a, self.b, self.c = a, b, c  # points a, b and c
		self.ab = self.b - self.a  # vector from a to b
		self.ac = self.c - self.a  # vector from a to c
		self.mat = mat  # material

	def calcMidpoint(self, points):
		s = Vector(0, 0, 0)
		for i in range(len(points)):
			n = i + 1
			a = points[i] / n
			s += a
		return s

	def normal(self):
		return self.ab.cross(self.ac).normalize()

	def intersection(self, ray):
		w = ray.origin - self.a
		dv = ray.direction.cross(self.ac)
		dvxab = dv.scalar(self.ab)  # d•v x b-a

		if dvxab == 0.0: return None

		wxu = w.cross(self.ab)

		r = dv.scalar(w) / dvxab
		s = wxu.scalar(ray.direction) / dvxab

		if 0 <= r <= 1 and 0 <= s <= 1 and r + s <= 1:
			return wxu.scalar(self.ac) / dvxab
		return None

	def __repr__(self):
		return "Triangle({},{},{},{})".format(repr(self.a), repr(self.b), repr(self.c), repr(self.mat))


class Plane(GraphicsObject):

	def __init__(self, point, normal, mat=black):
		super().__init__(point, mat)  # saves the origin in super
		self.normal = normal.normalize()
		self.mat = mat  # material

	def __repr__(self): return "Plane({},{},{})".format(repr(self.origin), repr(self.normal), repr(self.mat))

	def intersection(self, ray):
		op_n = (ray.origin - self.origin).scalar(self.normal)
		d_n = ray.direction.scalar(self.normal)

		return -(op_n / d_n) if d_n else  None

	def normal(self): return self.normal


class Light:

	def __init__(self, origin, intensity, color=white):
		self.origin = origin
		self.intensity = intensity  # origin = vector
		self.color = color


class Camera:

	def __init__(self, origin, focus, up, fov=100):
		self.origin = origin  # points

		if type(focus) == Vector:
			self.focus = focus  # the point to which the camera is aiming at
		elif type(focus) in (Triangle, Sphere, Plane, Light):
			self.focus = focus.origin  # focus on the center point of an object instead of a vector

		self.up = up  # global up vector/direction of up
		self.fov = fov  # field of view
		self.alpha = self.fov / 2

		ce = self.focus - self.origin
		self.f = ce / ce.length()  # perpendicular u vector (x-axis)

		fxup = self.f.cross(self.up)
		self.s = fxup / fxup.length()  # s vector (z-axis)
		self.u = self.s.cross(self.f)  # f vector (y-axis)

	def __repr__(self):
		return "Camera({},{},{},fov={})".format(
				repr(self.origin), repr(self.focus),
				repr(self.up), self.fov)


v1 = Vector([2, 3])
v2 = Vector(3, 5, 2)
c = Color(244, 235, 63)
c2 = Color(244, 235, 63)
c3 = c + c2

r = Ray(Vector(), v1)

print(v1.cross(v2))