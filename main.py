from gencg.hareg001.picture import *

WIDTH = 200
HEIGHT = 200

if __name__ == '__main__':
    up = Vector(0, 1, 0)
    focus_point = Vector(0, 0, 250)

    sphere_top = Sphere(30, Vector(0, 20, 550), Material(red + green, 0.7, 0.6, 0.1, 27))
    sphere_left = Sphere(30, Vector(-40, -40, 550), Material(green, 0.7, 0.4, 0.2))
    sphere_right = Sphere(30, Vector(40, -40, 550), Material(green, 0.3, 0.3, 0.2))

    triangle = Triangle(
            Vector(-100, 200, 100),
            Vector(0, 300, 200),
            Vector(100, 200, 100),
            Material(green, 0.1, 0.8, 0.4)
    )

    plane = Plane(
            Vector(0, 55, 70),
            Vector(0, 1, 0),
            Material(grey, 0.2, 0.71, 0.3)
    )

    plane2 = Plane(
            Vector(0, 55, 70),
            Vector(0, 1, 0),
            Texture_Checkerboard(0.3, 0.1, 0.42)
    )

    camera = Camera(Vector(0, 0, 10), Vector(0, -20, 250), up, 100)
    light = Light(Vector(-100, -100, 550), 1)

    objects = [sphere_top, sphere_left, sphere_right, plane]

    img = Picture(WIDTH, HEIGHT, camera, light, objects, reflection=0)
    img.castRays()
