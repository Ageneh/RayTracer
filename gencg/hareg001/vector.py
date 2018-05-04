import re

from numpy.linalg import linalg


class Vector:

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