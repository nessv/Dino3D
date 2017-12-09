import sys
import math
import random

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


class Light(object):
    enabled = False
    colors = [(1.,1.,1.,1.),
              (1.,0.5,0.5,1.),
              (0.5,1.,0.5,1.),
              (0.5,0.5,1.,1.)]

    def __init__(self, light_id, position):
        self.light_id = light_id
        self.position = position
        self.current_color = 0

    def render(self):
        light_id = self.light_id
        color = Light.colors[self.current_color]
        glLightfv(light_id, GL_POSITION, self.position)
        glLightfv(light_id, GL_DIFFUSE, color)
        glLightfv(light_id, GL_CONSTANT_ATTENUATION, 0.1)
        glLightfv(light_id, GL_LINEAR_ATTENUATION, 0.05)

    def switch_color(self):
        self.current_color += 1
        self.current_color %= len(Light.colors)

    def enable(self):
        if not Light.enabled:
            glEnable(GL_LIGHTING)
            Light.enabled = True
        glEnable(self.light_id)


class Sphere(object):
    slices = 40
    stacks = 40

    def __init__(self, radius, position, color):
        self.radius = radius
        self.position = position
        self.color = color
        self.quadratic = gluNewQuadric()
        self.on_ground = False
        self.velocity = 0

    def render(self):
        glPushMatrix()
        glTranslatef(*self.position)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.color)
        gluSphere(self.quadratic, self.radius, Sphere.slices, Sphere.stacks)
        glPopMatrix()


class Player(Sphere):
    def __init__(self, radius, position, color):
        super().__init__(radius, position, color)
        x, y, z = position
        self.x = x
        self.y = y
        self.z = z
        self.velocity = 0
        self.falling = True
        self.on_ground = False

    def jump(self):
        if not self.on_ground:
            return
        else:
            self.velocity = 0.7
            self.on_ground = False

    def update(self):
        if self.y < 0:
            if self.falling:
                self.on_ground = True
                self.velocity = 0
                self.falling = False

        if not self.on_ground:
            if self.velocity < 0:
                self.falling = True
            self.velocity += -0.04
            self.y += self.velocity
            self.position = (self.x, self.y, self.z)

class App(object):
    def __init__(self, width=800, height=600):
        self.title = 'My first OpenGL game'
        self.fps = 60
        self.width = width
        self.height = height
        self.game_over = False
        self.random_dt = 0
        self.light = Light(GL_LIGHT0, (0, 15, -25, 1))
        self.player = Player(radius=1, position=(0, 3, 0), color=(0, 1, 0, 1))

    def start(self):
        pygame.init()
        pygame.display.set_mode((self.width, self.height), OPENGL | DOUBLEBUF)
        pygame.display.set_caption(self.title)
        self.light.enable()
        glEnable(GL_DEPTH_TEST)
        glClearColor(.1, .1, .1, 1)
        glMatrixMode(GL_PROJECTION)
        aspect = self.width / self.height
        gluPerspective(45, aspect, 1, 100)
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_CULL_FACE)
        self.main_loop()

    def main_loop(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            if not self.game_over:
                self.display()
                dt = clock.tick(self.fps)
                self.process_input()

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0, 10, 10,
                  0, 0, -5,
                  0, 1, 0)
        self.light.render()
        self.player.update()
        self.player.render()
        pygame.display.flip()

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()


if __name__ == '__main__':
    app = App()
    app.start()
