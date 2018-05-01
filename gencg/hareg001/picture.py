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

	def start(self):
		_prop_str = "_".join([str("W" + str(self.resX)), str("H" + str(self.resY)), str("FOV" + str(self.camera.fov)), str("LIGHT" + str(self.light.origin))])
		self.image = Image.new("RGB", (self.resX, self.resY))

		self.castRays()  # start raytracing

		self.image.save( "/Users/HxA/PycharmProjects/RayTracer" + str(int(round(time.time() * 1000))) + "_" + _prop_str + ".jpg", "JPEG")
		self.image.show()

	# #############################################

	def castRays(self):
		for x in range(self.resX):
			for y in range(self.resY):
				# for each pixel of the image ..
				ray = self.calcRay(x, y)  # calculate a ray in the image
				color = self.traceRay(1, ray)  # follow ray and find color of pixel at its intersection

				self.image.putpixel((x, y), color.toRGB())  # color the pixel in image

	def traceRay(self, level, ray):  # (S47)
		hitPointData = self.intersect(level, ray)

		if hitPointData:  #if the ray intersects an object
			return self.shade(level, hitPointData)

		return self._BG_COLOR

	# get intersection data on whether the ray intersects an object or not
	def intersect(self, level, ray, maxlevel=5): # depth := recursion depth
		if level > maxlevel: return

		maxDist = float('inf')
		obj = None  # the intersected object
		for object in self.objects:
			hit = object.intersection(ray)
			if hit:
				if hit < maxDist:
					maxDist, obj = hit, object

		if obj:
			return HitPointData(obj=obj, dist=maxDist, ray=ray)
		return None

	def shade(self, level, hit):  # (S47)
		# shade = dot_product( light_vector, normal_vector )
		#if ( shade < 0 )
		# 	shade = 0
		# point_color = object_color * ( ambient_coefficient +
		# diffuse_coefficient * shade )

		ray = hit._RAY
		dist = hit._DIST
		obj = hit._OBJ

		# intersection = ray.pointAt(dist)
		# l = (self.light.origin - intersection).normalize()
		# shade = l.scalar(obj.normalAt(intersection))  # shade factor
		# if shade < 0: shade = 0
		# hit._SHADE = shade

		directColor = self.computeDirectLight_angle(hit)
		reflectedRay = self.computeReflectedRay(hit)
		reflectColor = self.traceRay(level+1, reflectedRay)

		#print(directColor, " + ", reflectColor, " * ", self.reflection)
		return directColor + reflectColor * self.reflection

	def computeDirectLight(self, hit):
		ray = hit._RAY
		dist = hit._DIST
		obj = hit._OBJ
		shade = 1

		intersection = ray.pointAt(dist)
		l = (self.light.origin - intersection).normalize()  # vector from intersection to light source
		n = obj.normalAt(intersection).normalize()
		l_reflected = l.reflect(n).normalize()
		d = (ray.origin - intersection).normalize()

		# check if object is shadowed

		reflectedRay = Ray(intersection, l_reflected)
		if self.intersect(1, reflectedRay):
			shade *= 0.3

		###

		diffMulti = l.scalar(n) * shade
		specMulti = l_reflected.scalar(d) * shade

		return obj.mat.color(diffMulti=diffMulti, specMulti= specMulti)

	def computeDirectLight_angle(self, hit):
		# v • w / ||v|| * ||w|| = alpha

		ray = hit._RAY
		dist = hit._DIST
		obj = hit._OBJ

		light = self.light
		intersection = ray.pointAt(dist)
		l = (light.origin - intersection).normalize()
		n = obj.normalAt(intersection).normalize()
		to_d = (ray.origin - intersection).normalize()
		reflected = l.reflect(n).normalize()
		reflectedRay = Ray(intersection, reflected)

		# check if point is facing light source
		diff = n.scalar(l)
		spec = reflected.scalar(to_d)
		print(str(True if diff <= 0 else False), diff, "\t\t\t", str(True if spec <= 0 else False), spec)
		return obj.mat.color_(diff, spec)

	def computeReflectedRay(self, hit):
		ray = hit._RAY
		dist = hit._DIST
		obj = hit._OBJ

		intersection = ray.pointAt(dist)
		n = obj.normalAt(intersection)
		d = (ray.origin - intersection)  # ray from intersection to camera

		reflected = d.reflect(n)  # reflected ray

		return Ray(intersection, reflected)

	def calcRay(self, x, y):
		xComp = self.camera.s.scale((x * self.pixelW) - (self.width / 2))  # scales width of each pixel
		yComp = self.camera.u.scale((y * self.pixelH) - (self.height / 2))  # s# cales height of each pixel
		return Ray(self.camera.origin, self.camera.f + xComp + yComp)
