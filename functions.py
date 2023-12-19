import pygame
import math

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 80
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_a,
    K_d
)


class Spline(pygame.sprite.Sprite):
    pointCount = 0

    def __init__(self, points):
        super(Spline, self).__init__()
        # points is a lise of dots
        self.points = points
        for point in points:
            Spline.pointCount += 1
        self.f_marker = 0

    def getSplinePoint(self, t, looped):
        if looped is False:
            p1 = int(t) + 1
            p2 = p1 + 1
            p3 = p2 + 1
            p0 = p1 - 1
        else:
            p1 = int(t)
            p2 = (p1 + 1) % Spline.pointCount
            p3 = (p2 + 1) % Spline.pointCount
            if p1 >= 1:
                p0 = p1 - 1
            else:
                p0 = Spline.pointCount - 1
        t = t - int(t)

        t_sq = t * t
        t_cb = t * t * t

        q1: float = -t_cb + (2.0 * t_sq) - t
        q2: float = (3.0 * t_cb) - (5.0 * t_sq) + 2.0
        q3: float = (-3.0 * t_cb) + (4.0 * t_sq) + t
        q4: float = t_cb - t_sq

        tx = (self.points[p0].x * q1) + (self.points[p1].x * q2) + (self.points[p2].x * q3) + (self.points[p3].x * q4)
        ty = (self.points[p0].y * q1) + (self.points[p1].y * q2) + (self.points[p2].y * q3) + (self.points[p3].y * q4)

        return dot((0.5 * tx, 0.5 * ty), (2, 2))

    def getSplineGradient(self, t, looped):
        if looped is False:
            p1 = int(t) + 1
            p2 = p1 + 1
            p3 = p2 + 1
            p0 = p1 - 1
        else:
            p1 = int(t)
            p2 = (p1 + 1) % Spline.pointCount
            p3 = (p2 + 1) % Spline.pointCount
            if p1 >= 1:
                p0 = p1 - 1
            else:
                p0 = Spline.pointCount - 1
        t = t - int(t)

        t_sq = t * t

        d1 = (-3.0 * t_sq) + (4.0 * t) - 1
        d2 = (9.0 * t_sq) - (10.0 * t)
        d3 = (-9.0 * t_sq) + (8.0 * t) + 1
        d4 = (3.0 * t_sq) - (2.0 * t)

        tx = (self.points[p0].x * d1) + (self.points[p1].x * d2) + (self.points[p2].x * d3) + (self.points[p3].x * d4)
        ty = (self.points[p0].y * d1) + (self.points[p1].y * d2) + (self.points[p2].y * d3) + (self.points[p3].y * d4)

        return dot((0.5 * tx, 0.5 * ty), (2, 2))

    def addPoint(self, point):
        self.points.append(point)

    def update(self, index, pressed_keys, looped, screen):
        self.points[index].update(pressed_keys)

        for point in self.points:
            screen.blit(point.surf, (point.x, point.y))
            point.changeColor(WHITE)
        self.points[index].changeColor(RED)

        # Draw Spline
        itr: float = 0
        if looped is False:
            while itr < float(Spline.pointCount) - 3:
                psub = Spline.getSplinePoint(self, t=itr, looped=looped)
                screen.blit(psub.surf, (psub.x, psub.y))
                itr += 0.01
        else:
            while itr < float(Spline.pointCount):
                psub = Spline.getSplinePoint(self, t=itr, looped=looped)
                screen.blit(psub.surf, (psub.x, psub.y))
                itr += 0.01

        if pressed_keys[K_a]:
            self.f_marker -= 0.001
        if pressed_keys[K_d]:
            self.f_marker += 0.001

        if (self.f_marker >= Spline.pointCount):
            self.f_marker = 0
        if (self.f_marker < 0):
            self.f_marker = 0
        # Draw Marker
        p1 = Spline.getSplinePoint(self, self.f_marker, looped)
        g1 = Spline.getSplineGradient(self, self.f_marker, looped)
        theta: float = math.atan(-g1.y / g1.x)
        print(theta)
        pygame.draw.line(screen, GREEN, (10.0 * math.sin(theta) + p1.x, 10.0 * math.cos(theta) + p1.y),
                         (-10.0 * math.sin(theta) + p1.x, -10.0 * math.cos(theta) + p1.y))


class dot(pygame.sprite.Sprite):
    def __init__(self, location, size):
        super(dot, self).__init__()
        self.x = location[0] + (size[0] / 2)
        self.y = location[1] + (size[1] / 2)
        self.surf = pygame.Surface((size[0], size[1]))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.y -= 2
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            self.y += 2
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
            self.x -= 2
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
            self.x += 2

    def changeColor(self, color):
        self.surf.fill(color)
