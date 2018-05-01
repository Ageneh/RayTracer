from math import tan, acos

from PIL import Image
from gencg.hareg001.objects import *
import time

class Picture(object):

	_BG_COLOR = Color(0, 0, 0)

	def __init__(self, resX, resY, camera, light, objects, reflection=0):
		self.resX, self.resY = resX, resY
		self.ratio = float(resX) / float(resY)

		self.reflection = reflection  # reflectiveness of the objects

		self.light = light
		self.objects = objects
		self.camera = camera
		self.image = None

		self.height = 2 * tan(self.camera.alpha)
		self.width = self.ratio * self.height

		self.pixelW, self.pixelH = self.width / (self.resX - 1), self.height / (self.resY - 1)

	# given
	def castRays(self):
		_prop_str = "_".join([str("W" + str(self.resX)), str("H" + str(self.resY)), str("FOV" + str(self.camera.fov)), str("LIGHT" + str(self.light.origin))])
		self.image = Image.new("RGB", (self.resX, self.resY))
		
		for x in range(self.resX):
			for y in range(self.resY):
				# for each pixel of the image ...
				ray = self.calcRay(x, y) # calculate a ray in the image
				color = self.traceRay(1, ray) # follow ray and find color of pixel at its intersection
				self.image.putpixel((x, y), color.toRGB()) # color the pixel in image

		self.image.save(
			"/Users/HxA/PycharmProjects/RayTracer" + str(int(round(time.time() * 1000))) + "_" + _prop_str + ".jpg",
			"JPEG", quality=90)
		self.image.show()

	# given
	def calcRay(self, x, y):
		xComp = self.camera.s.scale((x * self.pixelW - self.width / 2))  # scales width of each pixel
		yComp = self.camera.u.scale((y * self.pixelH - self.height / 2))  # s# cales height of each pixel
		return Ray(self.camera.origin, self.camera.f + xComp + yComp)

	# given
	def traceRay(self, level, ray):
		"""Trace ray and check for intersection. Closest intersection will then be used in shade(level, hit)."""
		# (S47)
		hitPointData = self.intersect(level, ray, max_level=3)
		if hitPointData: # if there is an intersection (ray and object)
			shade = self.shade(level, hitPointData)
			return shade
		return self._BG_COLOR

	# given
	def shade(self, level, hit):
		"""Uses the data from the hit and calculates a color."""
		# (S47)
		directC = self.computeDirectLight(hit) # the color where the direct light is illuminating # color
		reflectedR = self.computeReflectedRay(hit) # compute reflection of ray # ray
		reflectedC = self.traceRay(level+1, reflectedR) # color of reflection # color
		return directC + (reflectedC * self.reflection)

	################################### # ################################### # ###################################

	def computeDirectLight(self, hit):
		# variables
		ray = hit[HitPointData._RAY]
		object = hit[HitPointData._OBJ]
		dist = hit[HitPointData._DIST]

		shadeMulti = -1
		diffMulti, specMulti = 1, 1

		p = ray.pointAt(dist)  # intersection
		n = object.normalAt(p)  # normal at point p
		l = (self.light.origin - p).normalize()  # vector from p to light source
		lr = l.reflect(n).normalize()  # reflected l vector
		l_ray = Ray(p, l)  # ray from p to light
		d_ = (ray.origin - p).normalize()  # vector from p to camera origin


		# check if light hits directly or not
		diffMulti = n.scalar(l)
		specMulti = lr.scalar(d_)
		shaded = self.intersect(1, l_ray, 3)
		if shaded and dist < shaded[HitPointData._DIST]:  # some other object is between current object and light
			shadeMulti = 0.9
			diffMulti *= shadeMulti
			specMulti *= shadeMulti

		return object.mat.color(shadeMulti, diffMulti, specMulti)  # calculated mat

	# DONE
	def computeReflectedRay(self, hit):
		"""Returns a reflected ray."""
		ray = hit[HitPointData._RAY]
		object = hit[HitPointData._OBJ]
		dist = hit[HitPointData._DIST]

		p = ray.pointAt(dist)  # intersection
		n = object.normalAt(p)  # normal at point p
		reflected = ray.direction.normalize().reflect(n).normalize()

		r = Ray(p, reflected)

		return r  # reflected ray

	def intersect(self, level, ray, max_level=3):
		if level > max_level: return None

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