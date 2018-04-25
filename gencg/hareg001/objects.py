from PIL import Image
from numpy import *
import time


# objects

# TODO: shading und dann farben!! @see: Picture.shade()


class Color(object):
	_VALDICT = {"r": 0, "g": 1, "b": 2}
	_REPR = "Color(%d,%d,%d)"

	def __init__(self, r, g, b):
		self.values = (r, g, b)

	def __repr__(self):
		return self._REPR % tuple(self.values)

	def toRGB(self):
		return tuple(self.values)

	def __add__(self, other):
		if type(other) == Color:
			return eval(self._REPR % tuple(map(lambda x, y: x + y, self.values, other)))

	def __getitem__(self, item):
		if type(item) == int:
			return self.values[item]
		elif item in self._VALDICT.keys():
			return self.values[self._VALDICT[item]]

	def __mul__(self, other):
		return eval(self._REPR % tuple(map(lambda x: x * other, self.values)))

	def __truediv__(self, other):
		return eval(self.__mul__(1 / other))


class Mater(object):

	def __init__(self, ambient, ambientLvl, diffuse, diffuseLvl, spec, specLvl):
		self.ambient = ambient  # color
		self.ambientLvl = ambientLvl  # coefficient
		self.diffuse = diffuse  # color
		self.diffuseLvl = diffuseLvl  # coefficient
		self.spec = spec  # color
		self.specLvl = specLvl  # coefficient

	def color(self, diffMulti=1, specMulti=1):
		diffMulti = cos(diffMulti)
		specMulti = cos(specMulti)

		diffuse = self.diffuse * self.diffuseLvl * diffMulti
		spec = self.spec * self.specLvl * specMulti
		_ambient = self.ambient * self.ambientLvl

		components = [diffuse, spec]

		for c in components:
			for val in c.toRGB():
				if val < 0:
					c = black
					break
				elif val > 255:
					c = 255
					break

		_diffuse = diffuse * diffMulti * self.diffuseLvl
		_specular = spec * specMulti * self.specLvl

		return _ambient + _diffuse + _specular

	def __repr__(self):
		return "Material({},{},{},{},{},{},{})".format(
				repr(self.color),
				self.ambient, self.ambientLvl,
				self.diffuse, self.diffuseLvl,
				self.spec, self.specLvl)


white = Color(255, 255, 255)
grey = Color(128, 128, 128)
lightgrey = Color(219, 219, 219)
darkgrey = Color(20, 20, 20)
black = Color(0, 0, 0)
red = Color(255, 0, 0)
green = Color(0, 255, 0)
blue = Color(0, 0, 255)
yellow = Color(255, 255, 0)


class Vector(object):
	_REPR = "Vector(%f, %f, %f)"

	def __init__(self, x, y, z):
		# self.x, self.y, self.z, self.point = float(x), float(y), float(z), float(point)
		self.coordinates = [x, y, z]

	def scalar(self, vector):
		return sum(list(map(lambda x, y: x * y, self, vector)))

	def cross(self, vector):
		"""Calculates the cross product of the vector self and another given vector vector."""
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
		return sqrt(sum(list(map(lambda x: x ** 2, self.coordinates))))

	def normalize(self):
		length = self.length()
		return eval(self._REPR %
					tuple(map(lambda x: x / length, self.coordinates)))

	def scale(self, t):
		return eval(self._REPR % tuple(map(lambda x: x * t, self.coordinates)))

	def __add__(self, other):
		return eval(self._REPR % tuple(list(map(lambda x, y: x + y, self, other))))

	def __sub__(self, other):
		return eval(self._REPR % tuple(map(lambda x, y: x - y, self.coordinates, other)))

	def __mul__(self, t):
		return self.scalar(t) if type(t) == Vector else self.scale(t)

	def __getitem__(self, item):
		if type(item) == int:
			return self.coordinates[item]
		elif type(item) == slice:
			return self.coordinates[item]

	def __len__(self):
		return len(self.coordinates)

	def __pow__(self, exp, modulo=None):
		return eval(self._REPR % tuple(map(lambda x: x ** exp, self.coordinates)))

	def __repr__(self):
		return self._REPR % self.tuple()

	def __truediv__(self, t):
		return self.scale(1 / t)


class GraphicsObject(object):

	def intersection(self, ray): return

	def normalAt(self, point): return

	def colorAt(self, ray): return Color(255, 200, 100)


class Triangle(GraphicsObject):

	def __init__(self, a, b, c, mat):
		self.a, self.b, self.c = a, b, c  # points a, b and c
		self.ab = self.b - self.a  # vector from a to b
		self.ac = self.c - self.a  # vector from a to c
		self.mat = mat

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
		self.point, self.normal = point, normal.normalize()
		self.mat = mat

	def intersection(self, ray):
		op_n = (ray.origin - self.point).scalar(self.normal)
		d_n = ray.direction.scalar(self.normal)

		if d_n: return -(op_n / d_n)
		return None

	def normalAt(self, point): return self.normal

	def __repr__(self): return "Plane({},{},{})".format(repr(self.point), repr(self.normal), repr(self.mat))


class Sphere(GraphicsObject):

	def __init__(self, rad, center, mat):
		self.rad, self.center = rad, center  # rad:=number; center:=point
		self.mat = mat

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

	def __init__(self, origin, direction):
		self.origin, self.direction = origin, direction.normalize()  # origin = point; direction = vector

	def pointAt(self, t): return self.origin + (self.direction * t)

	def __repr__(self): return "Ray({}, {})".format(repr(self.origin), repr(self.direction))


class Light(object):

	def __init__(self, origin, intensity, color):
		self.origin, self.intensity = origin, intensity  # origin = vector
		self.color = color


class Camera(object):

	def __init__(self, origin, focus, up, fieldOfView):
		self.origin = origin  # points
		self.focus = focus  # the point to which the camera is aiming at
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


class Picture(object):

	def __init__(self, resX, resY, camera, light, objects):
		self.resX, self.resY = resX, resY
		self.ratio = float(resX) / float(resY)

		self.light = light
		self.objects = objects
		self.camera = camera
		self.image = None

		self.height = 2 * tan(self.camera.alpha)
		self.width = self.ratio * self.height

		self.pixelW, self.pixelH = self.width / (self.resX - 1), self.height / (self.resY - 1)

	def castRays(self):
		# _prop_str = "_".join([str("W" + str(self.resX)), str("H" + str(self.resY)), str("FOV" + str(self.camera.fov))])
		_prop_str = ""
		self.image = Image.new("RGB", (self.resX, self.resY))

		total = colorTotal = 0

		for x in range(self.resX):
			for y in range(self.resY):
				# for each pixel of the image ...
				color = black
				maxDistance = float('inf')

				total += 1

				ray = self.calcRay(x, y)  # .. cast a ray
				hitdist = None
				obj_ = None
				for obj in self.objects:
					obj_ = obj
					hitdist = obj.intersection(ray)
					if hitdist:
						# if the ray intersected an object ...

						if hitdist < maxDistance:
							# continue until its closest point has been found
							# and then color the pixel
							maxDistance = hitdist
							#color = self.calcIllumination(obj, ray, hitdist)
				if hitdist:
					color = self.calcIllumination(obj_, ray, hitdist)
				self.image.putpixel((x, y), color.toRGB())

				if color != black:
					colorTotal += 1
			# print("%.2f%%" % (colorTotal / total * 100))

		self.image.save(
			"/Users/HxA/PycharmProjects/RayTracer" + str(int(round(time.time() * 1000))) + "_" + _prop_str + ".jpg",
			"JPEG", quality=75)
		self.image.show()

	def calcRay(self, x, y):
		xComp = self.camera.s.scale(x * self.pixelW - self.width / 2)  # scales width of each pixel
		yComp = self.camera.u.scale(y * self.pixelH - self.height / 2)  # s# cales height of each pixel
		return Ray(self.camera.origin, self.camera.f + xComp + yComp)

	def calcIllumination(self, object, ray, dist):
		# angel between two vectors: <v,w> / ||v||*||w||
		light_vect = self.light.origin

		intersectionP = ray.direction * ((1)*dist)  # vector towards the object/intersection point #vector
		l = light_vect - intersectionP
		n = object.normalAt(intersectionP)
		d = ray.origin - intersectionP

		_diff_scalar = light_vect.normalize().scalar(object.normalAt(intersectionP))

		phi = l.normalize().scalar(n) / (l.length() * n.length())

		theta = phi - n.normalize().scalar(d) / (n.length() * d.length())

		return object.mat.color(diffMulti=phi, specMulti=theta)

	def shade(self):
		#TODO shading
		return
