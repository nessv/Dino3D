from pygame.locals import *
import os
import pygame
import re
import pygameMenu
from pygameMenu.locals import *
import game

ABOUT = ['PygameMenu {0}'.format(pygameMenu.__version__),
         'Author: {0}'.format(pygameMenu.__author__), TEXT_NEWLINE,
         'Email: {0}'.format(pygameMenu.__email__)]
COLOR_BACKGROUND = (0, 0, 0)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
FPS = 60.0
MENU_BACKGROUND_COLOR = (148, 146, 148)
WINDOW_SIZE = (800, 600)

# -----------------------------------------------------------------------------
# Init pygame
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Create pygame screen and objects
surface = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Dinosaurito 3D')
clock = pygame.time.Clock()
dt = 1 / FPS


# -----------------------------------------------------------------------------

def start():
    app = game.App()
    app.start()


def main_background():
    surface.fill(COLOR_BACKGROUND)


# -----------------------------------------------------------------------------
# PLAY MENU
play_menu = pygameMenu.Menu(surface,
                            window_width=WINDOW_SIZE[0],
                            window_height=WINDOW_SIZE[1],
                            font=pygameMenu.fonts.FONT_BEBAS,
                            title='Play menu',
                            menu_alpha=100,
                            font_size=30,
                            menu_width=int(WINDOW_SIZE[0] * 0.6),
                            menu_height=int(WINDOW_SIZE[1] * 0.6),
                            bgfun=main_background,
                            menu_color=MENU_BACKGROUND_COLOR,
                            option_shadow=False,
                            font_color=COLOR_BLACK,
                            color_selected=COLOR_WHITE,
                            onclose=PYGAME_MENU_DISABLE_CLOSE
                            )

play_menu.add_option('Play', start)

# ABOUT MENU
about_menu = pygameMenu.TextMenu(surface,
                                 window_width=WINDOW_SIZE[0],
                                 window_height=WINDOW_SIZE[1],
                                 font=pygameMenu.fonts.FONT_BEBAS,
                                 font_title=pygameMenu.fonts.FONT_8BIT,
                                 title='About',
                                 # Disable menu close (ESC button)
                                 onclose=PYGAME_MENU_DISABLE_CLOSE,
                                 font_color=COLOR_BLACK,
                                 text_fontsize=20,
                                 font_size_title=30,
                                 menu_color_title=COLOR_WHITE,
                                 menu_color=MENU_BACKGROUND_COLOR,
                                 menu_width=int(WINDOW_SIZE[0] * 0.6),
                                 menu_height=int(WINDOW_SIZE[1] * 0.6),
                                 option_shadow=False,
                                 color_selected=COLOR_WHITE,
                                 text_color=COLOR_BLACK,
                                 bgfun=main_background)

file = open("score.txt", "r")
scores = []
for n in file:
    scores.append(int(re.sub(":", "", n)))

scores = sorted(scores, reverse=True)
for m in scores[0:4]:
    about_menu.add_line(str(m) + "  SEGUNDOS")

file.close()
about_menu.add_option('Return to menu', PYGAME_MENU_BACK)

# MAIN MENU
main_menu = pygameMenu.Menu(surface,
                            window_width=WINDOW_SIZE[0],
                            window_height=WINDOW_SIZE[1],
                            font=pygameMenu.fonts.FONT_BEBAS,
                            title='Main menu',
                            menu_alpha=100,
                            font_size=30,
                            menu_width=int(WINDOW_SIZE[0] * 0.6),
                            menu_height=int(WINDOW_SIZE[1] * 0.6),
                            onclose=PYGAME_MENU_DISABLE_CLOSE,  # ESC disabled
                            bgfun=main_background,
                            menu_color=MENU_BACKGROUND_COLOR,
                            option_shadow=False,
                            font_color=COLOR_BLACK,
                            color_selected=COLOR_WHITE,
                            )
main_menu.add_option('Play', play_menu)
main_menu.add_option('Statistics', about_menu)
main_menu.add_option('Quit', PYGAME_MENU_EXIT)

# -----------------------------------------------------------------------------
# Main loop
while True:

    # Tick
    clock.tick(60)

    # Application events
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            exit()

    # Main menu
    main_menu.mainloop(events)

    # Flip surface
    pygame.display.flip()