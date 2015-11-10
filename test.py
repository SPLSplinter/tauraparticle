from tauraparticle import *
from taurapoint    import *

import pygame
from pygame.locals import *
from pygame.time import Clock

pygame.init()
WIDTH  = 800
HEIGHT = 600
FPS = 24
clock = Clock()
mouse_position = (0, 0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
quit = False

simulation = ParticleSimulation(WIDTH, HEIGHT)
simulation.friction = 0.005


p1 = Particle()
p1.setPosition(Point2(50,50))
p1.setMovement(Point2(0,0))
p1.mass = 9999
simulation.add(p1)

p2 = Particle()
p2.setPosition(Point2(200,52))
p2.setMovement(Point2(-10,0))
p2.mass = 1
simulation.add(p2)


while not quit:

    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == QUIT:
            quit = True
        elif event.type == KEYDOWN:
            if event.key == K_q:
                quit = True
            else:
                print(event.key, "---")

    for p in simulation.particles:
        pygame.draw.circle(screen, (0,255,0), p.position.rect(asInt=True), p.size,1)

    pygame.display.flip()
    simulation.update()
    clock.tick(FPS)