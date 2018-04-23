from gencg.hareg001.objects import *

if __name__ == "__main__":

    white = Color(255, 255, 255)
    grey = Color(128, 128, 128)
    darkgrey = Color(20, 20, 20)
    black = Color(0, 0, 0)

    up = Vector(0,-1,0)

    v = Vector(0, 50, -50)
    camera = Camera(200, 200, Vector(0, -5, 0), 90, up, up)

    light = Light(Vector(-100, 200, -40), 1, Color(255, 255, 255))
    sp = Sphere(100, Vector(20, 0, 100))

    img = Picture(camera, light, sp)

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