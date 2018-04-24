from gencg.hareg001.objects import *

WIDTH = 300
HEIGHT = 300

if __name__ == "__main__":

    print(black.toRGB())

    up = Vector(0, 1, 0)
    focus_point = Vector(0, 45, 250)

    sphere = Sphere(30, Vector(0, 0, 100), Material(red, red, green, red, red, red))

    camera = Camera(Vector(0,0,-50),focus_point, up, 70)
    light = Light(100, 200, -75)

    img = Picture(WIDTH, HEIGHT, camera, light, sphere)
    img.castRays()

else :
    v0 = Vector(2, 3, 4)
    v1 = Vector(3, 6, 2)

    v0 = Vector(1, 2, 3)
    v1 = Vector(2, 1, 3)

    v0 = Vector(1, -2, 1)
    v1 = Vector(4, 3, 0)

    print(v0, v1)
    print(v0.length(), v1.length())
    print(v0.tuple(), v1.tuple())
    print(v0.cross(v1))
    print(v0.scalar(v1))

    print("Hess'che", v0.normalize())

    print("ADD:", (v0 + v1))

    t = Triangle(3, 2, 4)

    c = Camera(v0, 400, 400, 60, v1, Vector(300, 200, 132))
    print(c)

    print(t)