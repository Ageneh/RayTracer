from gencg.hareg001.picture import *

WIDTH = 500
HEIGHT = 500

if __name__ == '__main__':
    up = Vector(0, 1, 0)
    focus_point = Vector(0, 0, 250)

    sphere_top = Sphere(30, Vector(0, 20, 550), Material(red, 0.4, red * 0.4, 0.6, grey, 0.1, 27))
    sphere_left = Sphere(30, Vector(-40, -40, 550), Material(green, 0.3, grey, 0.3, grey, 0.2))
    sphere_right = Sphere(30, Vector(40, -40, 550), Material(green, 0.3, grey, 0.2, grey, 0.2))

    triangle = Triangle(
            Vector(0, 20, 550),
            Vector(-40, -40, 550),
            Vector(40, -40, 550),
            Material(yellow, 0.4, yellow*0.3, 0.3, grey, 0.4)
    )

    plane = Plane(
            Vector(0, -55, 70),
            Vector(0, 1, 0),
            Material(grey, 0.4, grey*0.3, 0.1, grey, 0.3)
    )

    camera = Camera(Vector(0, 0, 0), Vector(0, -20, 250), up, 120)
    light = Light(Vector(50, 120, 500), 1)

    objects = [sphere_top, sphere_left, sphere_right, triangle, plane]

    img = Picture(WIDTH, HEIGHT, camera,
                  light, objects, reflection=1)
    img.castRays()
