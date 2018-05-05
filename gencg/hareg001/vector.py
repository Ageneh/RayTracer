import re


class Vector:

	_dict = { "x":0, "y":1, "z":2 }

	def __init__(self, components, x=0, y=0, z=0):
		self._classname_ = _classname_(self)
		self.components = (x, y, z)
		count = 3
		if len(components) > 0:
			content = ()
			if type(components[0]) in (list, tuple):
				content = tuple(components[0][:])
			else: content = tuple(components[:])
			content += (0,) * (count - len(content))
			self.components = tuple(content[:count])

	def __getitem__(self, item):
		if item in self._dict:
			return self[self._dict[item.lower()]]
		elif type(item) in (int, slice):
			return self.components[item]

	def __len__(self):
		return len(self.components)

	def __mul__(self, other):
		if type(other) in (int, float):
			return self.scale(other)

	def __truediv__(self, other):
		return self * (1/other)

	def __iter__(self):
		for val in self.components: yield val
		raise StopIteration

	def __add__(self, other):
		#return Vector(list(map(lambda x, y: x+y, self, other)))
		return tuple(map(lambda x, y: x+y, self, other))

	def __sub__(self, other):
		return self + (-1) * other

	def __str__(self):
		return str(self.components)

	def __repr__(self):
		return self._classname_ + str(self)

	def scale(self, t):
		return Vector([x * t for x in self])

def _classname_(self):
	return re.findall(".([\w]+)\'>", str(self.__class__))[0]