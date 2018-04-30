from gencg.hareg001.picture import *

WIDTH = 400
HEIGHT = 300

if __name__ == '__main__':
    up = Vector(0, -1, 0)
    focus_point = Vector(0, 0, 250)

    sphere_top = Sphere(30, Vector(0, 20, 250), Material(red, 0.4, red * 0.4, 0.6, grey, 0.1, 27))
    sphere_left = Sphere(30, Vector(-40, -40, 250), Material(green, 0.3, grey, 0.8, grey, 0.2))
    sphere_right = Sphere(30, Vector(40, -40, 250), Material(green, 0.3, grey, 0.8, grey, 0.2))

    triangle = Triangle(
            Vector(-100, 200, 100),
            Vector(0, 300, 200),
            Vector(100, 200, 100),
            Material(green, 1, green*0.3, 0.8, grey, 0.4)
    )

    plane = Plane(
            Vector(0, 55, 70),
            Vector(0, 1, 0),
            Material(grey, 0.4, grey*0.3, 0.71, grey, 0.3)
    )

    camera = Camera(Vector(0, 0, 0), Vector(0, -20, 250), up, 120)
    light = Light(Vector(-100, -300, 150), 1)

    objects = [sphere_top, sphere_left, sphere_right, plane]

    img = Picture(WIDTH, HEIGHT, camera,
                  light, objects, reflection=0)
    img.castRays()
