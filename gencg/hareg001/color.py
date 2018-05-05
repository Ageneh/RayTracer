from gencg.hareg001 import vector


class Color(vector.Vector):
	_dict = { "r":0, "g":1, "b":2 }

	def __init__(self, *components, r=0, g=0, b=0):
		super().__init__(components, r, g, b)

	#def __add__(self, other): return
	def __add__(self, other):
		return _check_(Color(super().__add__(other)))

	def __sub__(self, other): return self + (other * -1)

	def __mul__(self, other):
		return _check_(Color(super().__mul__(other)))

	def __truediv__(self, other):
		return self * (1/other)

def _check_(color):
	a, b = _MAX(), _MIN()
	for i in color:
		if i > a: return Color(a, a, a)
		if i < b: return Color(b, b, b)
	return color

def _MAX(): return 255

def _MIN(): return 0


black = Color(0, 0, 0)
white = Color(255, 255, 255)