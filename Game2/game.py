import sys
import random
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

gravity = -0.02
TIMEEVENT = pygame.USEREVENT + 1


class Cube(object):
    sides = ((0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4),
             (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6))

    def __init__(self, position, size, color):
        self.position = position
        self.color = color
        x, y, z = map(lambda i: i / 2, size)
        self.vertices = (
            (x, -y, -z), (x, y, -z),
            (-x, y, -z), (-x, -y, -z),
            (x, -y, z), (x, y, z),
            (-x, -y, z), (-x, y, z))

    def render(self):
        glPushMatrix()
        glTranslatef(*self.position)
        glBegin(GL_QUADS)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.color)
        for side in Cube.sides:
            for v in side:
                glVertex3fv(self.vertices[v])
        glEnd()
        glPopMatrix()


class Block(Cube):
    color = (0, 0.25, 0, 1)
    speed = 0.02

    def __init__(self, position, size):
        super(Block, self).__init__(position, (size, size, size), Block.color)
        self.size = size

    def update(self, dt):
        x, y, z = self.position
        z += Block.speed * dt
        self.position = x, y, z


class Light(object):
    enabled = False
    colors = [(1., 1., 1., 1.),
              (1., 0.5, 0.5, 1.),
              (0.5, 1., 0.5, 1.),
              (0.5, 0.5, 1., 1.)]

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


# class Player(Cube):
#     def __init__(self, position, size, color):
#         super().__init__(position, size, color)
#         x, y, z = position
#         self.x = x
#         self.y = y
#         self.z = z
#         self.velocity = 0
#         self.falling = True
#         self.on_ground = False
#
#     def jump(self):
#         if not self.on_ground:
#             return
#         else:
#             self.velocity = 0.6
#             self.on_ground = False
#
#     def update(self):
#         if self.y < 0:
#             if self.falling:
#                 self.on_ground = True
#                 self.velocity = 0
#                 self.falling = False
#
#         if not self.on_ground:
#             if self.velocity < 0:
#                 self.falling = True
#             self.velocity += gravity
#             self.y += self.velocity
#             self.position = (self.x, self.y, self.z)


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
            self.velocity = 0.6
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
            self.velocity += gravity
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
        self.textdata = ""
        self.blocks = []
        # timer variables
        self.milliseconds = 0
        self.minutes = 0
        self.seconds = 0
        self.time = "0:0"
        self.clock = pygame.time.Clock()
        self.light = Light(GL_LIGHT0, (0, 15, -25, 1))
        self.player = Player(radius=1, position=(0, 3, 0), color=(0.25, 0, 1, 0))
        # self.player = Player(position=(0, 3, 0), size=(2, 2, 2), color=(1, 1, 1, 1))
        self.ground = Cube(position=(0, -1, -20),
                           size=(16, 1, 60),
                           color=(1, 1, 1, 1))

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
        pygame.time.set_timer(TIMEEVENT, 1000)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            if not self.game_over:
                self.display()
                dt = clock.tick(self.fps)
                for block in self.blocks:
                    block.update(dt)
                self.add_random_block(dt)
                self.clear_past_blocks()
                self.player.update()
                self.check_collisions()
                self.process_events()

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0, 10, 10,
                  0, 0, -5,
                  0, 1, 0)
        self.light.render()
        for block in self.blocks:
            block.render()
        self.player.update()
        self.player.render()
        self.ground.render()
        self.drawtext(self.time)
        pygame.display.flip()

    def drawtext(self, text):
        font = pygame.font.Font(None, 30)
        textSurface = font.render(text, True, (255, 255, 255, 255), (104, 104, 104, 104))
        self.textdata = pygame.image.tostring(textSurface, "RGBA", True)
        glRasterPos3d(*(5, -1, 0))
        glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, self.textdata)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
            if event.type == TIMEEVENT:
                self.set_time()

    def check_collisions(self):
        blocks = filter(lambda x: 0 < x.position[2] < 1, self.blocks)
        # My player current position
        y = self.player.position[1]
        r = self.player.radius

        for block in blocks:
            y1 = block.position[1]
            s = block.size / 2
            if y1 + s > y - r:
                self.save_score()
                self.game_over = True
                print("Game over!")

    def add_random_block(self, dt):
        self.random_dt += dt
        if self.random_dt >= 800:
            r = random.random()
            if r < 0.1:
                self.random_dt = 0
                self.generate_block()

    def generate_block(self):
        size = 2
        offset = 0
        self.blocks.append(Block((offset, 0, -40), size))

    def clear_past_blocks(self):
        blocks = filter(lambda x: x.position[2] > 5, self.blocks)
        for block in blocks:
            self.blocks.remove(block)
            del block

    def set_time(self):
        if self.milliseconds > 1000:
            self.seconds += 1
            self.milliseconds -= 1000
        if self.seconds > 60:
            self.minutes += 1
            self.seconds -= 60

        self.time = ("{}:{}".format(self.minutes, self.seconds))
        self.milliseconds += self.clock.tick_busy_loop(60)

    def save_score(self):
        file = open("score.txt", "a")
        file.write('\n' + self.time)
        file.close()


if __name__ == '__main__':
    app = App()
    app.start()
