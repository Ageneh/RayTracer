from math import tan, acos

from PIL import Image
from gencg.hareg001.objects import *
import time

class Picture(object):

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
				color = self._BG_COLOR

				ray = self.calcRay(x, y) # calculate a ray in the image
				maxDist = self.intersect(1, ray)

				if maxDist:
					color = self.traceRay(1, ray) # follow ray and find color of pixel at its intersection
					color *= self.color(maxDist)

				self.image.putpixel((x, y), color.toRGB()) # color the pixel in image

		self.image.save(
			"/Users/HxA/PycharmProjects/RayTracer" + str(int(round(time.time() * 1000))) + "_" + _prop_str + ".jpg",
			"JPEG", quality=90)
		self.image.show()

	def calcRay(self, x, y):
		xComp = self.camera.s.scale((x * self.pixelW - self.width / 2))  # scales width of each pixel
		yComp = self.camera.u.scale((y * self.pixelH - self.height / 2))  # s# cales height of each pixel
		return Ray(self.camera.origin, self.camera.f + xComp + yComp)

	# ORIGINAL
	def computeDirectLight(self, hit):
		ray = hit[HitPointData._RAY]
		object = hit[HitPointData._OBJ]
		dist = hit[HitPointData._DIST]

		# angle between two vectors: <v,w> / ||v||*||w||

		light_origin = self.light.origin
		light_intensity = self.light.intensity
		intersection = ray.pointAt(dist)  # the point where the ray intersects the object #vector

		# (S44)
		l = (light_origin - intersection).normalize()

		n = object.normalAt(intersection)
		l_reflected = l.reflect(n)
		d = ray.origin - intersection

		phi = n.calcAngle(l)
		# angle between the normal of the intersection point and
		# the light vector; used as the factor by which the
		# diffusion color will be multiplied

		theta = d.calcAngle(l_reflected)
		# angle between the normal of the intersection point and
		# the light vector; used as the factor by which the
		# diffusion color will be multiplied

		return object.mat.color(diffMulti=phi, specMulti=theta)

	def computeReflectedRay(self, hit):
		ray = hit[HitPointData._RAY]
		object = hit[HitPointData._OBJ]
		dist = hit[HitPointData._DIST]

		s = ray.pointAt(dist) # intersection
		n = object.normalAt(s) # normal at intersection

		return Ray(s, ray.direction.reflect(n).normalize()) # reflected ray

	def color(self, hit):
		ray = hit[HitPointData._RAY]
		object = hit[HitPointData._OBJ]
		dist = hit[HitPointData._DIST]

		s = ray.pointAt(dist)
		to_light = self.light.origin - s  # intersection to light source

		objectBetween = self.intersect(1, Ray(s, to_light))
		if objectBetween:
			# if there is an object between, shadow
			return 0.1
		return 1

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

	def traceRay(self, level, ray):
		# (S47)
		hitPointData = self.intersect(level, ray, max_level=3)
		if hitPointData: # if there is an intersection (ray and object)
			intersection = ray.pointAt(hitPointData[HitPointData._DIST])
			l = self.light.origin - intersection
			shade = self.shade(level, hitPointData)

			return shade
		return self._BG_COLOR

	def shade(self, level, hit):
		# (S47)

		directC = self.computeDirectLight(hit) # the color where the direct light is illuminating # color
		reflectedR = self.computeReflectedRay(hit) # compute reflection of ray # ray
		reflectedC = self.traceRay(level+1, reflectedR) # color of reflection # color

		s = directC + (reflectedC * self.reflection)
		return s