from numpy import *


# objects

# –––––––––––––––– - COLORS - –––––––––––––––– #
class Color(object):
	_VALDICT = {"r": 0, "g": 1, "b": 2}
	_REPR = "Color(%d,%d,%d)"

	def __init__(self, r, g, b, alpha=1.0):
		self.values = []
		min, max = self.MIN_VAL(), self.MAX_VAL()
		for val in [r, g, b]:
			if val < min: self.values.append(min)
			elif val > max: self.values.append(max)
			else: self.values.append(val)
		self.alpha = alpha

	def __repr__(self):
		return self._REPR % tuple(self.values)

	def toRGB(self): return tuple(self.values)

	def toRGBA(self): return self.toRGB() + (self.alpha,)

	def MIN_VAL(*v): return 0

	def MAX_VAL(*v): return 255

	def __add__(self, other):
		if type(other) == Color:
			return eval(self._REPR % tuple(map(lambda x, y: x + y, self.values, other)))

	def __getitem__(self, item):
		if type(item) == int:
			return self.values[item]
		elif item in self._VALDICT.keys():
			return self.values[self._VALDICT[item]]

	def __mul__(self, other):
		# if type(other) != Color:
		if type(other) in (int, float, float64):
			other = float(other)
			return eval(self._REPR % tuple(map(lambda x: x * other, self)))

	def __truediv__(self, other):
		return eval(self.__mul__(1 / other))


white = Color(255, 255, 255)
lightgrey = Color(219, 219, 219)
grey = Color(128, 128, 128)
darkgrey = Color(20, 20, 20)
black = Color(0, 0, 0)
red = Color(242, 7, 7)
green = Color(5, 210, 25)
blue = Color(5, 80, 210)
yellow = Color(255, 255, 0)


# –––––––––––––––– END COLORS –––––––––––––––– #


class Material(object):

	def __init__(self, color, ambientLvl, diffuseLvl, specLvl, surface=1):
		self.color = color  # color
		self.ambientLvl = ambientLvl  # coefficient
		self.diffuseLvl = diffuseLvl  # coefficient
		self.specLvl = specLvl  # coefficient
		self.surface = surface


	def __repr__(self):
		return "Material({},{},{},{},{},{})".format(
				self.ambient, self.ambientLvl,
				self.diffuse, self.diffuseLvl,
				self.spec, self.specLvl)

class Texture_Checkerboard(Material):


	def __init__(self, ambientLvl, diffuseLvl, specularLvl, color1=black, color2=white, tilesize=5):
		super().__init__(black, ambientLvl, white, diffuseLvl, specularLvl)
		self.colors = (color1, color2)
		self.tileSize = tilesize

		return

	def color(self, point, diffMulti, specMulti):
		dM = diffMulti
		sM = specMulti ** self.surface

		if (int(abs(point["x"]) + 0.5) + int(abs(point["y"]) + 0.5) + int(abs(point["z"]) + 0.5)) % 2:
			diffuse = self.colors[1] * self.diffuseLvl * dM
		else:
			diffuse = self.colors[0] * self.diffuseLvl

		specular = self.spec * sM * self.specLvl

		colors = [diffuse, specular]

		for color in range(len(colors)):
			for i in range(len(colors[color].toRGB())):
				val = colors[color].toRGB()[i]
				if Color.MIN_VAL() <= val <= Color.MAX_VAL(): continue
				if val < Color.MIN_VAL(): colors[color] = black
				elif val > Color.MAX_VAL(): colors[color] = white
				break
		diffuse, specular = colors[0], colors[1]

		ambient = self.ambient * self.ambientLvl

		return ambient + diffuse + specular


# –––––––––––––––– - –––––––––––––––– #

class Vector(object):
	_REPR = "Vector(%f, %f, %f)"

	def __init__(self, x, y, z):
		# self.x, self.y, self.z, self.point = float(x), float(y), float(z), float(point)
		self.coordinates = [x, y, z]

	def scalar(self, vector):
		"""Calculates the scalar of two vectors."""
		return sum(list(map(lambda x, y: x * y, self, vector)))

	def scale(self, t):
		"""Multiplies the vector by the factor t."""
		return eval(self._REPR % tuple(map(lambda x: x * t, self.coordinates)))

	def cross(self, vector):
		"""Calculates the cross product of the vector (self) and another given vector (vector)."""
		vector1 = self.tuple()
		vector2 = vector.tuple()

		output = []

		for n in range(len(vector)):
			for i in range(len(vector)):
				if i != n:
					j = 1
					for j in range(j, len(vector) - i):
						if i + j != n:
							break

					sum = (vector1[i] * vector2[i + j]) - (vector1[i + j] * vector2[i])
					output.append(sum)
					break

		return eval(self._REPR % tuple(output))

	def tuple(self):
		"""Returns a tuple with all components (implicit)."""
		return tuple(self.coordinates)

	def length(self):
		"""Returns the length of a vector."""
		return sqrt(sum(list(map(lambda x: x ** 2, self))))

	def normalize(self):
		"""Returns a normalized vector by dividing each component of the vector."""

		# length = self.length() # length of the vector;
		# return eval(self._REPR % tuple(map(lambda x: x / length, self.coordinates)))
		return self / self.length()

	def reflect(self, reflection_axis):
		return self - (2 * (self.scalar(reflection_axis)) * reflection_axis)  # (S48)

	def calcAngle(self, w):
		"""Calculates the angle between two vectors."""
		return (self * w) / (self.length() * w.length())

	def __add__(self, other):
		return eval(self._REPR % tuple(list(map(lambda x, y: x + y, self, other))))

	def __sub__(self, other):
		return eval(self._REPR % tuple(list(map(lambda x, y: x - y, self, other))))

	def __mul__(self, t):
		return self.scalar(t) if type(t) == Vector else self.scale(t)

	def __getitem__(self, item):
		if type(item) == int:
			return self.coordinates[item]
		elif type(item) == str:
			if item.lower() == "x": return self.coordinates[0]
			elif item.lower() == "y": return self.coordinates[1]
			elif item.lower() == "z": return self.coordinates[2]
		elif type(item) == slice:
			return self.coordinates[item]

	def __len__(self):
		"""Returns the amount of components."""
		return len(self.coordinates)

	def __pow__(self, exp, modulo=None):
		"""Calculates the """
		return eval(self._REPR % tuple(map(lambda x: x ** exp, self.coordinates)))

	def __repr__(self):
		return self._REPR % self.tuple()

	def __truediv__(self, t):
		return self.scale(1 / t)


class GraphicsObject(object):

	def __init__(self, origin):
		self.origin = origin

	def intersection(self, ray): return

	def normalAt(self, point): return

	def colorAt(self, ray): return


class Triangle(GraphicsObject):

	def __init__(self, a, b, c, mat):
		super().__init__(self.calcMidpoint((a, b, c)))  # saves the origin in super
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

	def __init__(self, point, normal, mat):
		super().__init__(point)  # saves the origin in super
		self.point, self.normal = point, normal.normalize()
		self.mat = mat  # material

	def intersection(self, ray):
		op_n = (ray.origin - self.point).scalar(self.normal)
		d_n = ray.direction.scalar(self.normal)

		if d_n: return -(op_n / d_n)
		return None

	def normalAt(self, point): return self.normal

	def __repr__(self): return "Plane({},{},{})".format(repr(self.point), repr(self.normal), repr(self.mat))


class Sphere(GraphicsObject):

	def __init__(self, rad, center, mat):
		super().__init__(center)  # saves the origin in super
		self.rad, self.center = rad, center  # rad:=number; center:=point
		self.mat = mat  # material

	def __repr__(self):
		return "Sphere({},{},{})".format(self.rad, repr(self.center), repr(self.mat))

	def intersection(self, ray):
		co = self.center - ray.origin  # co = c-o
		v = co.scalar(ray.direction)

		discriminant = v ** 2 - co.scalar(co) + self.rad ** 2

		if discriminant < 0:
			return None
		else:  # nur wenn der punkt vor der camera ist; nicht hinter
			return v - sqrt(discriminant)

	def normalAt(self, point):
		return (point - self.center).normalize()


# –––––––––––––––– - –––––––––––––––– #

class Ray(object):
	_REPR = "Ray({}, {})"

	def __init__(self, origin, direction):
		self.origin, self.direction = origin, direction.normalize()  # origin = point; direction = vector

	def pointAt(self, t):
		"""Returns a point (vector)."""
		return self.origin + (self.direction * t)

	def __repr__(self): return self._REPR.format(repr(self.origin), repr(self.direction))

	def __mul__(self, other):
		return self.origin + self.direction * other


class Light(GraphicsObject):

	def __init__(self, origin, intensity):
		super().__init__(origin)
		self.intensity = intensity  # origin = vector
# self.origin, self.intensity = origin, intensity  # origin = vector


class Camera(object):

	def __init__(self, origin, focus, up, fieldOfView):
		self.origin = origin  # points

		if type(focus) == Vector:
			self.focus = focus  # the point to which the camera is aiming at
		elif type(focus) in (Triangle, Sphere, Plane, Light):
			self.focus = focus.origin  # focus on the center point of an object instead of a vector
		self.up = up  # global up vector/direction of up
		self.fov = fieldOfView  # field of view
		self.alpha = self.fov / 2

		ce = self.focus - self.origin
		self.f = ce / ce.length()  # perpendicular u vector (x-axis)

		fxup = self.f.cross(self.up)
		self.s = fxup / fxup.length()  # s vector (z-axis)

		self.u = self.s.cross(self.f)  # f vector (y-axis)

	def __repr__(self):
		return "Camera({},{},{},{},{},{})".format(
				self.origin, self.width, self.height,
				self.fieldOfView, self.up, self.c)


# –––––––––––––––– - –––––––––––––––– #

class HitPointData:

	def __init__(self, ray=None, obj=None, dist=None):
		self._RAY = ray
		self._OBJ = obj
		self._DIST = dist
