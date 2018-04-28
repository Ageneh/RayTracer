from gencg.hareg001.objects import *

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

	def calcRay(self, x, y):
		xComp = self.camera.s * (x * self.pixelW - self.width / 2)  # scales width of each pixel
		yComp = self.camera.u * (y * self.pixelH - self.height / 2)  # s# cales height of each pixel
		return Ray(self.camera.origin, self.camera.f + xComp + yComp)

	def castRays(self):
		_prop_str = "_".join([str("W" + str(self.resX)), str("H" + str(self.resY)), str("FOV" + str(self.camera.fov))])

		self.image = Image.new("RGB", (self.resX, self.resY))
		total = colorTotal = 0

		for x in range(self.resX):
			for y in range(self.resY):
				color = self._BG_COLOR
				# for each pixel of the image ...
				ray = self.calcRay(x, y) # calculate a ray

				maxDist = self.intersect(0, ray)
				if maxDist:
					color = self.traceRay(0, ray) # follow ray and find color of pixel at its intersection
				self.image.putpixel((x, y), color.toRGB()) # color the pixel in image

		self.image.save(
			"/Users/HxA/PycharmProjects/RayTracer" + str(int(round(time.time() * 1000))) + "_" + _prop_str + ".jpg",
			"JPEG", quality=75)
		self.image.show()

	def computeDirectLight(self, object, ray, dist):
		# angel between two vectors: <v,w> / ||v||*||w||
		light_origin = self.light.origin
		light_intensity = self.light.intensity
		# intersectionP = ray.direction * ((1)*dist)  # vector towards the object/intersection point #vector
		intersectionP = ray.pointAt(dist)  # vector towards the object/intersection point #vector
		l = (light_origin - intersectionP).normalize()
		n = object.normalAt(intersectionP)
		l_r = l.reflect(n)
		d = ray.origin - intersectionP

		_diff_scalar = light_origin.normalize().scalar(object.normalAt(intersectionP))

		# phi = l.normalize().scalar(n) / (l.length() * n.length())
		# theta = phi - n.normalize().scalar(d) / (n.length() * d.length())
		#_diff = l.scalar(n) / (l.length() * n.length())
		#_spec = _diff - n.scalar(d) / (n.normalize().length() * d.normalize().length())

		_diff = (l * n) * light_intensity
		_l_r = l_r * ray.direction.normalize()
		_spec = _l_r * light_intensity

		return object.mat.color(diffMulti=_diff, specMulti=_spec)

	def computeReflectedRay(self, object, ray, dist):
		s = ray.pointAt(dist) # intersection
		n = object.normalAt(s) # normal at intersection

		return Ray(s, ray.direction.reflect(n).normalize()) # reflected ray

	def intersect(self, level, ray, max_level=3):

		if level >= max_level: return None

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

		return HitPointData(obj=_obj, ray=ray, dist=maxDist) if _obj != None else None

	def traceRay(self, level, ray):
		hitPointData = self.intersect(level, ray, max_level=1)
		if hitPointData != None:
			return self.shade(level, hitPointData["obj"], hitPointData["ray"], hitPointData["dist"])
		return self._BG_COLOR

	def shade(self, level, object, ray, dist):
		directC = self.computeDirectLight(object, ray, dist); # the color where the direct light is illuminating # color
		reflectedR = self.computeReflectedRay(object, ray, dist); # compute reflection of ray # ray
		reflectedC = self.traceRay(level+1, reflectedR) # color of reflection # color

		s = directC + reflectedC * self.reflection
		return s