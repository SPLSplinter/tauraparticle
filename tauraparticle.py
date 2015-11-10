#############################################
# Copyright (c) 2015 Fabricio JC Montenegro #
# 10th november 2015                        #
# Version 1.0                               #
#############################################
"""
This package allows the creation of a 2D particle simulation.
"""

from math import *
from taurapoint import Point2

__all__ = ['Particle', 'ParticleSimulation']

class Particle:
    """The class represents a circular particle in 2D space. Attributes are:
        - id: int. For utility
        - size: int. Radius of the circle
        - position: Point2. Position of the particle in 2D space
        - movement: Point2. Movement vector
        - mass: float. Mass of the particle
    """
    def __init__(self):
        self.id = 0
        self.size = 20
        self.position = Point2()
        self.movement = Point2()
        self.mass = 1

    def setPosition(self, pos):
        """Receives a taurapoint.Point2 as position"""
        self.position = Point2(pos)
        return self

    def setMovement(self, mov):
        """Receives a taurapoint.Point2 as movement"""
        self.movement = Point2(mov)
        return self

    def move(self, friction=0):
        """Updates the particle position using its movement as increment"""
        self.position += self.movement
        self.movement *= 1 - friction
        return self

    def bounce(self, width, height):
        """If the particle goes out of the boundaries, it bounces back in. The boundaries are:
            - x = 0
            - x = width
            - y = 0
            - y = height"""

        # right_wall  = width - self.size
        # left_wall   = self.size
        # top_wall    = self.size
        # bottom_wall = height - self.size
        # vert_wall  = pi
        # horiz_wall = 0

        # if went right
        if self.position.x > (width - self.size):
            self.position.x = 2*(width - self.size) - self.position.x
            self.movement.a = pi - self.movement.a

        # if went left
        elif self.position.x < self.size:
            self.position.x = 2*self.size - self.position.x
            self.movement.a = pi - self.movement.a

        # if went down
        if self.position.y > (height - self.size):
            self.position.y = 2*(height - self.size) - self.position.y
            self.movement.a = 0 - self.movement.a

        # if went up
        elif self.position.y < self.size:
            self.position.y = 2*self.size - self.position.y
            self.movement.a = 0 - self.movement.a

        return self

    def collide(self, p2):
        """If the particle collides with another given particle, calculates the movement vectors after the collision."""
        p1 = self
        collision = (p2.position - p1.position)
        distance = collision.r
        if distance < (p1.size + p2.size):

            col_ang = collision.a
            v1 = Point2(p1.movement.x, p1.movement.y)
            v2 = Point2(p2.movement.x, p2.movement.y)

            v1.a -= col_ang
            v2.a -= col_ang

            m1 = p1.mass * 100
            m2 = p2.mass * 100
            M = m1 + m2

            # v1 = v1 * (m1 - m2) + 2*m2*v2/M
            v1.x, v2.x = (v1.x*(m1 - m2) + 2*m2*v2.x)/M, (v2.x*(m2 - m1) + 2*m1*v1.x)/M

            v1.a += col_ang
            v2.a += col_ang

            p1.movement.x, p1.movement.y = v1.x, v1.y
            p2.movement.x, p2.movement.y = v2.x, v2.y

            collision.r = p1.size + p2.size + 1
            if p2.mass < p1.mass:
                p2.position = (p1.position + collision)
            else:
                p1.position = (p2.position - collision)
        return self

class ParticleSimulation:
    """This class manages the 2D particle simulation"""
    def __init__(self, width, height):
        """Besides width and height, you can later set a friction rate. For example, friction = 0.1 will make the particle lose 10% of its velocity each cycle.
        """
        self.width  = width
        self.height = height

        self.friction = 0
        self.particles = []

    def find(self, point):
        """If the point is inside a particle, returns this particle"""
        for p in self.particles:
            if (p.position - point).r <= p.size:
                return p
        return None

    def findById(self, id):
        """Searches for a particle with the given id"""
        for p in self.particles:
            if p.id == id:
                return p
        return None

    def add(self, particle):
        """Adds a partice to the simulation"""
        self.particles.append(particle)
        return self

    def remove(self, particle):
        """Removes a particle from the simulation"""
        self.particles.remove(particle)
        return self

    def update(self):
        """Calculates the movement, the friction, the bouncing and the colliding of particles and updates the simulation"""
        for i, p in enumerate(self.particles):
            p.move(self.friction)
            p.bounce(self.width, self.height)
            for c in self.particles[i+1:]:
                c.collide(p)
        return self
