from numpy import *
from PIL import Image
import time


# objects


class Vector(object):

	# TODO: flexible amount of coordinates; in list

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

		return eval(self.vectorTempl() % tuple(output))

	def tuple(self):
		"""Returns a tuple with all components (implicit)."""
		return tuple(self.coordinates)

	def length(self):
		return sqrt(sum(list(map(lambda x: x ** 2, self.coordinates))))

	def vectorTempl(self):
		return "Vector(%f, %f, %f)"

	def normalize(self):
		length = self.length()
		return eval(
				self.vectorTempl() %
				tuple( map(lambda x: x/length, self.coordinates) )
		)

	def scale(self, t):
		return eval(self.vectorTempl() % tuple(map(lambda x: x * t, self)))

	def __add__(self, other):
		return eval(self.vectorTempl() % tuple(list(map(lambda x, y: x + y, self, other))))

	def __sub__(self, other):
		return eval(self.vectorTempl() % tuple(map(lambda x, y: x - y, self.coordinates, other)))

	def __mul__(self, t):
		return self.scalar(t) if type(t) == Vector else self.scale(t)

	def __getitem__(self, item):
		if type(item) == int:
			return self.coordinates[item]
		elif type(item) == slice:
			return self.coordinates[item]

	def __len__(self):
		return len(self.coordinates)

	def __repr__(self):
		return self.vectorTempl() % self.tuple()

	def __truediv__(self, t):
		return self.scale(t)


class GraphicsObject(object):

	def intersection(self, ray):
		return

	def colorAt(self, ray):
		return Color(255, 200, 100)


class Triangle(GraphicsObject):

	def __init__(self, a, b, c):
		self.a, self.b, self.c = a, b, c  # points a, b and c
		self.ab = self.b - self.a  # vector from a to b
		self.ac = self.c - self.a  # vector from a to c

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
		return "Triangle({}, {}, {})".format(repr(self.a), repr(self.b), repr(self.c))


class Plane(GraphicsObject):

	def __init__(self, point, normal):
		self.point, self.normal = point, normal.normalize()

	def intersection(self, ray):
		op_n = (ray.origin - self.point).scalar(self.normal)
		d_n = ray.direction.scalar(self.normal)

		if d_n: return -(op_n / d_n)
		return None

	def normalAt(self): return self.normal

	def __repr__(self):
		return "Plane({},{})".format(repr(self.point), repr(self.normal))


class Sphere(GraphicsObject):

	def __init__(self, rad, center):
		self.rad, self.center = rad, center  # rad:=number; center:=point

	def __repr__(self):
		return "Sphere({}, {})".format(self.rad, repr(self.center))

	def intersection(self, ray):
		co = self.center - ray.origin  # co = c-o
		v = co.scalar(ray.direction)

		discriminant = v**2 - co.scalar(co) + self.rad ** 2

		if discriminant < 0:
			return None
		else:
			return v - sqrt(discriminant)  # nur wenn der punkt vor der camera ist; nicht hinter

	def normalAt(self, point):
		return (point - self.center).normalize()


# –––––––––––––––– - –––––––––––––––– #


class Ray(object):

	def __init__(self, origin, direction):
		self.origin, self.direction = origin, direction.normalize()  # origin = point; direction = vector

	def pointAt(self, t): return self.origin + (self.direction * t)

	def __repr__(self):
		return "Ray({}, {})".format(repr(self.origin), repr(self.direction))


class Light(object):

	def __init__(self, origin, intensity, color):
		self.origin, self.intensity = origin, intensity
		self.color = color


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

	def __init__(self, origin, focus, up, fieldOfView):
		self.origin = origin  # points
		self.focus = focus # the point to which the camera is aiming at
		self.up = up # global up vector/direction of up
		self.fov = fieldOfView # field of view
		self.alpha = self.fov / 2

		ce = self.focus - self.origin
		self.f = ce / ce.length() # perpendicular u vector (x-axis)

		fxup = self.f.cross(self.up)
		self.s = fxup / fxup.length() # s vector (z-axis)

		self.u = self.s.cross(self.f) # f vector (y-axis)

	def __repr__(self):
		return "Camera({},{},{},{},{},{})".format(
				self.origin, self.width, self.height,
				self.fieldOfView, self.up, self.c)


class Color(object):

	def __init__(self, r=0, g=0, b=0):
		self.r, self.g, self.b = r, g, b

	def  toRGB(self):
		return int(self.r), int(self.g), int(self.b)

	def __str__(self):
		return "Color: rgba({}, {}, {}, 1.0)".format(self.r, self.g, self.b)

	def __repr__(self):
		return "Color({},{},{})".format(self.r, self.g, self.b)


# –––––––––––––––– - –––––––––––––––– #


class Picture(object):

	def __init__(self, resX, resY, camera, light, *objects, aspectRatio=False):
		self.resX, self.resY = resX, resY

		if aspectRatio != False and type(aspectRatio) == int:
			try:
				aspectRatio = float(aspectRatio)
				self.ratio = 1.0 / aspectRatio
			except ValueError: aspectRatio = False

		if aspectRatio == False:
			self.ratio = float(resX) / float(resY)

		self.light = light
		self.objects = list(objects)
		self.camera = camera

		self.height = 2 * tan(self.camera.alpha)
		self.width = self.ratio * self.height

	def castRays(self):
		self.image = Image.new("RGB", (self.resX, self.resY))

		total = colorTotal = 0

		for x in range(self.resX):
			for y in range(self.resY):
				# for each pixel of the image ...
				total += 1
				ray = self.calcRay(x, y) # .. cast a ray
				maxDistance = float('inf')
				color = black.toRGB()
				for obj in self.objects:
					hitdist = obj.intersection(ray)
					if x == 140 and y == 163:
						print()
					if hitdist:
						# if the ray intersected an object ...
						if hitdist < maxDistance:
							# continue until its closest point has been found
							# and then color the pixel
							maxDistance = hitdist
							color = white.toRGB()

					self.image.putpixel((x, y), color)

				if color != black:
					colorTotal += 1
					s = str(total) + "-" + str(colorTotal)
					print(s)

		self.image.save("/Users/HxA/PycharmProjects/RayTracer" + str(int(round(time.time() * 1000))) + ".jpg",
						"JPEG", quality=90)
		self.image.show()

	def sendRay(self):
		pxWidth = self.width / (self.pxX - 1)
		pxHeight = self.height / (self.pxY - 1)

		for y in range(self.pxY):
			for x in range(self.pxX):
				xComp = self.s.scale(x * pxWidth - self.camera.width / 2)  # scales width of each pixel
				yComp = self.u.scale(y * pxHeight - self.camera.height / 2)  # scales height of each pixel
				ray = Ray(self.origin, self.f + xComp + yComp)

	def calcRay(self, x, y):
		height = 2 * tan(self.camera.alpha)
		width = (self.width / self.height) * height

		pixelWidth = self.width / (self.resX - 1)
		pixelHeight = self.height / (self.resY - 1)

		xComp = self.camera.s.scale(x * pixelWidth - self.width / 2)  # scales width of each pixel
		yComp = self.camera.u.scale(y * pixelHeight - self.height / 2)  # s# cales height of each pixel

		# return Ray(self.camera.origin, self.camera.f + xComp + yComp)
		return Ray(self.camera.origin, (self.camera.f + xComp) + yComp)


# colors


white = Color(255, 255, 255)
grey = Color(128, 128, 128)
lightgrey = Color(219, 219, 219)
darkgrey = Color(20, 20, 20)
black = Color(0, 0, 0)
red = Color(255, 0, 0)
green = Color(0, 255, 0)
blue = Color(0, 0, 255)
yellow = Color(255,255,0)
