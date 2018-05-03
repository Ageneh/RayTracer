from math import tan, acos

from PIL import Image
from gencg.hareg001.objects import *
import time

class Picture(object):

	MAXREC = 0

	_BG_COLOR = Color(0, 0, 0)

	def __init__(self, resX, resY, camera, light, objects, reflection=0):
		self.resX, self.resY = resX, resY
		self.ratio = float(resX) / float(resY)

		self.reflection = reflection

		self.light = light
		self.objects = objects
		self.camera = camera
		self.image = None

		self.height = 2 * tan(self.camera.alpha)
		self.width = self.ratio * self.height

		self.pixelW, self.pixelH = self.width / (self.resX - 1), self.height / (self.resY - 1)

	def castRays(self):
		_prop_str = "_".join([str("W" + str(self.resX)), str("H" + str(self.resY)), str("FOV" + str(self.camera.fov)), str("LIGHT" + str(self.light.origin))])

		self.image = Image.new("RGB", (self.resX, self.resY))
		
		for x in range(self.resX):
			for y in range(self.resY):
				# for each pixel of the image ...
				ray = self.calcRay(x, y) # calculate a ray in the image
				color = self.traceRay(0, ray) # follow ray and find color of pixel at its intersection
				self.image.putpixel((x, y), color.toRGB()) # color the pixel in image

		self.image.save(
			"/Users/HxA/PycharmProjects/RayTracer" + str(int(round(time.time() * 1000))) + "_" + _prop_str + ".jpg",
			"JPEG", quality=90)
		self.image.show()

	def calcRay(self, x, y):
		xComp = self.camera.s.scale((x * self.pixelW - self.width / 2))  # scales width of each pixel
		yComp = self.camera.u.scale((y * self.pixelH - self.height / 2))  # s# cales height of each pixel
		return Ray(self.camera.origin, self.camera.f + xComp + yComp)

	# check if there is an object between light and intersection
	def objectBetween(self, hit):
		ray = hit._RAY
		obj = hit._OBJ
		dist = hit._DIST

		# ################## #
		p = ray.pointAt(dist)  # intersection
		l = (p - self.light.origin)  # vector from light source to p
		l_ray = Ray(self.light.origin, l)  # ray from p to light
		l_dist = obj.intersection(l_ray)  # distance from light to intersection
		# ################## #
		if l_dist is None: return False
		for obj in self.objects:
			hitdist = obj.intersection(l_ray)
			if hitdist and l_dist:
				if 0.01 < hitdist < l_dist:
					return True
		return False

	def computeShadedColor(self, hit):
		ray = hit._RAY
		object = hit._OBJ
		dist = hit._DIST

		# ################## #
		p = ray.pointAt(dist)  # intersection
		n = object.normalAt(p).normalize()
		l = (self.light.origin - p).normalize()  # vector from p to light source
		lr = l.reflect(n).normalize()  # reflected l vector
		l_ray = Ray(p, l)  # ray from p to light
		d_ = (ray.origin - p).normalize()  # vector from p to camera origin
		# ################## #

		return object.mat.color*0.2 # * l.scalar(n)

	def computeDirectLight(self, hit):
		ray = hit._RAY
		object = hit._OBJ
		dist = hit._DIST

		# angle between two vectors: <v,w> / ||v||*||w||

		light_origin = self.light.origin
		intersection = ray.pointAt(dist)  # the point where the ray intersects the object #vector

		# (S44)
		l = (light_origin - intersection).normalize()
		n = object.normalAt(intersection).normalize()
		l_reflected = l.reflect(n).normalize()
		d = (ray.origin - intersection).normalize()

		phi = l.scalar(n)
		# angle between the normal of the intersection point and
		# the light vector; used as the factor by which the
		# diffusion color will be multiplied

		theta = l_reflected.scalar(d * -1)
		# angle between the nxormal of the intersection point and
		# the light vector; used as the factor by which the
		# diffusion color will be multiplied

		if type(object.mat) == CheckerBoard:
			return object.mat.baseColorAt(intersection).color(diffMulti=phi, specMulti=theta)

		return object.mat.color(diffMulti=phi, specMulti=theta)

	def computeReflectedRay(self, hit):
		ray = hit._RAY
		object = hit._OBJ
		dist = hit._DIST

		s = ray.pointAt(dist) # intersection
		n = object.normalAt(s) # normal at intersection

		return Ray(s, ray.direction.reflect(n)) # reflected ray

	def color(self, hit):
		ray = hit._RAY
		object = hit._OBJ
		dist = hit._DIST

		s = ray.pointAt(dist)
		to_light = self.light.origin - s  # intersection to light source

		objectBetween = self.intersect(1, Ray(s, to_light))
		if objectBetween:
			# if there is an object between, shadow
			return 0.1
		return 1

	def intersect(self, level, ray):
		if level > self.MAXREC: return None

		maxDist = float('inf')
		_obj = None

		for obj in self.objects:
			hitdist = obj.intersection(ray)
			if hitdist:
				# if the ray intersected an object ...
				if 0 < hitdist < maxDist:
					# continue until its closest point has been found
					maxDist = hitdist
					_obj = obj

		# return HPD if there an intersection with an object
		if _obj == None:
			return None
		return HitPointData(obj=_obj, ray=ray, dist=maxDist)

	def traceRay(self, level, ray):
		# (S47)
		hitPointData = self.intersect(level, ray)
		if hitPointData:  #if the ray intersects an object
			hit = self.objectBetween(hitPointData)
			if hit == True:
				ray = hitPointData._RAY
				obj = hitPointData._OBJ
				dist = hitPointData._DIST
				if type(obj.mat) == CheckerBoard:
					mat = obj.mat.baseColorAt(ray.pointAt(dist))
					return mat.color(0, 0) * mat.ambientLvl
				return hitPointData._OBJ.mat.color(0, 0) * hitPointData._OBJ.mat.ambientLvl
			else:
				return self.shade(level, hitPointData)

		return self._BG_COLOR

	def shade(self, level, hit):# (S47)
		directC = self.computeDirectLight(hit) # the color where the direct light is illuminating # color
		reflectedR = self.computeReflectedRay(hit) # compute reflection of ray # ray
		reflectedC = self.traceRay(level+1, reflectedR) # color of reflection # color
		s = directC + (reflectedC * self.reflection)
		return s