from gencg.hareg001.objects import *

WIDTH = 400
HEIGHT = 300

if __name__ == '__main__':
    up = Vector(0, -1, 0)
    focus_point = Vector(0, 0, 250)

    m = Mater(red, 0.8, red*0.4, 0.6, white, 0.8)

    sphere = Sphere(30, Vector(0, 0, 100),
                    m)
    plane = Plane(
            Vector(0, 60, 0),
            Vector(0, -1, 0),
            Mater(green, 0.4, blue, 0.71, white, 0.9)
    )

    camera = Camera(Vector(0,20,-150),focus_point, up, 120)
    light = Light(Vector(10, 100, 0), 0.8, lightgrey)

    img = Picture(WIDTH, HEIGHT, camera, light, [sphere, plane], reflection=1)
    img.castRays()
