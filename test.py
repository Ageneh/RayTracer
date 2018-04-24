def a(aspect=False):
	print("–>",aspect)
	aspectR = 1.0
	if aspect == False:
		print("1:1")
	else:
		print(1/aspectR)


a(aspect=False)
a(aspect=2)