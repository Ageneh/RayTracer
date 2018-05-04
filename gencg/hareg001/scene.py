from numpy import arccos, cos, tan
from numpy import linalg
import re

from gencg.hareg001 import vector

print(
	linalg.linalg.dot(
		(2, 3, 4),
		(3, 5, 2)
	)
)

class Origin:
	def __init__(self, *components, x=0, y=0, z=0):
		self.components = [x, y, z]
		if len(components) > 0: self.components = components[0:3]

class Vector(vector.Vector):

	_dict = { "x":0, "y":1, "z":2 }

	def __init__(self, *components, x=0, y=0, z=0):
		self.components = (x, y, z)
		count = 3
		if len(components) > 0:
			if type(components[0]) in (list, tuple): components = components[0][:]
			for i in range(count - len(components)): components.append(0)
			self.components = tuple(components[:count])

	def __getitem__(self, item):
		if item in self._dict:
			return self[self._dict[item.lower()]]
		elif type(item) in (int, slice):
			return self.components[item]

	def __len__(self): return len(self.components)

	def __mul__(self, other):
		if type(other) in (int, float):
			return self.scale(other)
		elif type(other) == Vector:
			return self.scalar(other)
		elif type(other) in (list, tuple):
			return self.scalar(Vector(other))

	def __truediv__(self, other):
		return self * (1/other)

	def __iter__(self):
		for val in self.components: yield val
		raise StopIteration

	def __add__(self, other):
		#if type(other) in (list, tuple): other = Vector(other)
		return linalg.linalg.add(self, other)

	def className(self): return

	def __sub__(self, other): return self + (-1) * other

	def __str__(self): return str(self.components)

	def __repr__(self):
		pat = re.findall(".([\w]+)\'>", str(self.__class__))[0]
		return pat + "(" + str(self) + ")"

	def length(self): return sum([x**2 for x in self])**(1/2)

	def scalar(self, vector): return linalg.linalg.dot(self, vector)

	def scale(self, t): return Vector([x * t for x in self])

	def cross(self, vector):
		"""Calculates the cross product of the vector (self) and another given vector (vector)."""
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

class Color(vector.Vector):
	_dict = { "r":0, "g":1, "b":2 }

	def __init__(self, *components, r=0, g=0, b=0):
		super().__init__(components, r, g, b)

	def __iter__(self):
		for val in self.components: yield val
		raise StopIteration

	def __getitem__(self, item):
		if type(item) in self._dict:
			return self[self._dict[item.tolower()]]
		elif type(item) in (int, slice):
			return self.components[item]

	def __add__(self, other):
		result = super().__add__(other)
		return Color(result.components)

	def cross(self, vector): raise NotImplementedError

	def scalar(self, vector): raise NotImplementedError

	def length(self): raise NotImplementedError



v1 = Vector([2, 3])
v2 = Vector(3, 5, 2)
c = Color(244, 235, 63)
c2 = Color(244, 235, 63)
c3 = c + c2

r = Ray(Vector(), v1)

print(v1, v2)
print(repr(v1))
print(repr(r))
print("z", v1["z"])
print(repr(c))

print(v1 + v2)
print(v1.normalize())