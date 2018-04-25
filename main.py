from gencg.hareg001.objects import *

WIDTH = 400
HEIGHT = 300

if __name__ == "__main__":
    up = Vector(0, -1, 0)
    focus_point = Vector(0, 0, 250)

    sphere = Sphere(30, Vector(0, 0, 100),
                    mat=Material(red, 0.1, green, 0.3, blue, 0.4))
    plane = Plane(
            Vector(0, -60, 0),
            Vector(0, 1, 0),
            mat=Material(red, 0.4, green, 0.71, blue, 0.3)
    )

    camera = Camera(Vector(0,0,-50),focus_point, up, 120)
    light = Light(Vector(100, 200, -75), 1, white)

    img = Picture(WIDTH, HEIGHT, camera, light, [sphere, plane])
    img.castRays()
