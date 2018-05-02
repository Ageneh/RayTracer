from math import tan

from PIL import Image
from gencg.hareg001.objects import *
import time

class Picture:

	_BG_COLOR = Color(0, 0, 0)

	def __init__(self, resX, resY, camera, light, objects, reflection=0):
		self.resX, self.resY = resX, resY
		self.ratio = float(resX) / float(resY)

		self.reflection = reflection  # reflectiveness of the objects

		self.image = None
		self.light = light
		self.objects = objects
		self.camera = camera

		self.height = 2 * tan(self.camera.alpha)
		self.width = self.ratio * self.height

		self.pixelW = self.width / (self.resX - 1)
		self.pixelH = self.height / (self.resY - 1)

	# given
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
			"/Users/HxA/PycharmProjects/RayTracer" + str(int(round(time.time() * 1000))) + "_" + _prop_str + "" + ".jpg", "JPEG", quality=90)
		self.image.show()

	# given
	def calcRay(self, x, y):
		xComp = self.camera.s.scale((x * self.pixelW - self.width / 2.0))  # scales width of each pixel
		yComp = self.camera.u.scale((y * self.pixelH - self.height / 2.0))  # s# cales height of each pixel
		return Ray(self.camera.origin, self.camera.f + xComp + yComp)

	# given
	def traceRay(self, level, ray):
		"""Trace ray and check for intersection. Closest intersection will then be used in shade(level, hit)."""
		# (S47)
		hitPointData = self.intersect(level, ray, max_level=1)
		if hitPointData: # if there is an intersection (ray and object)
			if self.objectBetween(hitPointData):
				return self.computeShadedColor(hitPointData)
			shade = self.shade(level, hitPointData)
			return shade
		return self._BG_COLOR

	# given
	def shade(self, level, hit):  # (S47)
		"""Uses the data from the hit and calculates a color."""
		directC = self.computeDirectLight(hit)  # the color where the direct light is illuminating # color
		reflectedC = self.traceRay(level+1, self.computeReflectedRay(hit))  # color of reflection # color
		return directC + (reflectedC * self.reflection)

	# ################################## # ################################### # ################################## #

	# check if there is an object between light and intersection
	def objectBetween(self, hit):
		ray = hit._RAY
		dist = hit._DIST

		# ################## #
		p = ray.pointAt(dist)  # intersection
		l = (self.light.origin - p)  # vector from p to light source
		l_ray = Ray(p, l)  # ray from p to light
		# ################## #

		for obj in self.objects:
			hitdist = obj.intersection(l_ray)
			if hitdist and 0.001 < hitdist < l.length():
				return True
		return False

	def computeDirectLight(self, hit):
		lightColor = white
		# variables
		ray = hit._RAY
		object = hit._OBJ
		dist = hit._DIST

		p = ray.pointAt(dist)  # intersection
		n = object.normalAt(p).normalize()  # normal at point p
		l = (self.light.origin - p).normalize()  # vector from p to light source
		lr = l.reflect(n).normalize()  # reflected l vector
		l_ray = Ray(p, l)  # ray from p to light
		d_ = (ray.origin - p).normalize()  # vector from p to camera origin

		material = object.mat

		###########

		phi = l.scalar(n)
		theta = lr.scalar(d_)

		# ambient
		ambient = material.color
		# diffuse
		diffuse = lightColor * 0.3 * phi
		# specular
		specular = lightColor * 0.3 * theta

		# vals = [diffuse, specular]
		# for k in range(len(vals)):
		# 	for i in range(len(vals[k].toRGB())):
		# 		val = vals[k].toRGB()[i]
		# 		if 0 < val < 255: continue
		# 		if val < 0: vals[k] = darkgrey
		# 		elif val > 255: vals[k] = white
		# 		break
		# diffuse, specular = vals[0], vals[1]

		return ambient + diffuse + specular

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

		return object.mat.color * l.scalar(n)

	# DONE
	def computeReflectedRay(self, hit):
		"""Returns a reflected ray."""
		ray = hit._RAY
		object = hit._OBJ
		dist = hit._DIST

		p = ray.pointAt(dist)  # intersection
		n = object.normalAt(p).normalize()  # normal at point p
		reflected = (ray.origin - p).reflect(n)

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
				if 0.001 < hitdist < maxDist:
					# continue until its closest point has been found
					maxDist = hitdist
					_obj = obj

		# return HPD if there an intersection with an object
		if _obj == None:
			return None
		return HitPointData(obj=_obj, ray=ray, dist=maxDist)