import pygame
from Classes import dot, Spline
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_z
)

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

P0 = dot((1, 1), (20, 20))
P1 = dot((5, 5), (20, 20))
P2 = dot((10, 10), (20, 20))
P3 = dot((20, 20), (20, 20))
P4 = dot((40,40), (20, 20))
P5 = dot((80,80), (20, 20))
curve = Spline([P0, P1, P2, P3, P4, P5])
pressed_keys = pygame.key.get_pressed()
running = True
index = 0
timer = 0
placed = False
available = False
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_z] and (index+1) < Spline.pointCount and available:
        index += 1
        placed = True
        available = False
    elif pressed_keys[K_z] and (index+1) >= Spline.pointCount and available:
        timer = 0
        index = 0
        placed = True
        available = False
    elif available is False:
        timer += 1
        if timer > 500:
            timer = 0
            available = True
    screen.fill((0, 0, 0))
    curve.update(index, pressed_keys, True, screen)
    # Updates frame
    pygame.display.flip()
