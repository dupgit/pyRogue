#!/usr/bin/env python3
# coding: utf-8
#
# $Id: rogue_test02.2.py 894 $
# SPDX-License-Identifier: BSD-2-Clause
#

"""
    from http://www.roguebasin.com/index.php?title=Roguelike_Tutorial,_using_python3%2Btdl,_part_2
"""

import tdl

# actual size of the window
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
REALTIME = False
LIMIT_FPS = 20  # 20 frames-per-second maximum, for realtime mode

MAP_WIDTH = 80
MAP_HEIGHT = 45

color_dark_wall = (0, 0, 100)
color_dark_ground = (50, 50, 150)


class Tile:
    """
        a tile of the map with its properties
    """
    def __init__(self, blocked, block_sight=None):
        """ """
        self.blocked = blocked

        # by default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked
        self.block_sight = block_sight


class GameObject:
    """
        this is a generic object: the player, a monster, an item, stairs...
        it's always represented by a character on screen.
    """
    def __init__(self, x, y, char, color):
        """ """
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy):
        """
            move by the given amount, if the destination is not blocked
        """
        if not my_map[self.x + dx][self.y + dy].blocked:
            self.x += dx
            self.y += dy

    def draw(self):
        """
            draw the character that represents this object at its position
        """
        con.draw_char(self.x, self.y, self.char, self.color, bg=None)

    def clear(self):
        """
            erase the character that represents this object
        """
        con.draw_char(self.x, self.y, ' ', self.color, bg=None)


def handle_keys(realtime):
    """ """
    if realtime:
        keypress = False
        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event
                keypress = True
        if not keypress:
            return

    else:  # turn-based
        user_input = tdl.event.key_wait()

    if user_input.key == 'ENTER' and user_input.alt:
        # Alt+Enter: toggle fullscreen
        tdl.set_fullscreen(not tdl.get_fullscreen())

    elif user_input.key == 'ESCAPE':
        return True  # exit game

    # movement keys
    if user_input.key == 'UP':
        player.move(0, -1)
    elif user_input.key == 'DOWN':
        player.move(0, 1)
    elif user_input.key == 'LEFT':
        player.move(-1, 0)
    elif user_input.key == 'RIGHT':
        player.move(1, 0)


def make_map():
    """ """
    global my_map

    # fill map with "unblocked" tiles
    # via comprehension list
    my_map = [[Tile(False)
               for y in range(MAP_HEIGHT)]
              for x in range(MAP_WIDTH)]

    # place two 'pillar', for test
    my_map[30][22].blocked = True
    my_map[30][22].block_sight = True
    my_map[50][22].blocked = True
    my_map[50][22].block_sight = True


def render_all():
    """ """
    # go through all tiles, and set their background color
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            wall = my_map[x][y].block_sight
            if wall:
                con.draw_char(x, y, None, fg=None, bg=color_dark_wall)
            else:
                con.draw_char(x, y, None, fg=None, bg=color_dark_ground)

    # draw all objects in the list
    for obj in objects:
        obj.draw()

    # blit the contents of "con" to the root console and present it
    root.blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)


##############################
# Initialization & Main Loop #
##############################

tdl.set_font('dejavu10x10_gs_tc.png', greyscale=True, altLayout=True)
root = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Roguelike", fullscreen=False)
con = tdl.Console(SCREEN_WIDTH, SCREEN_HEIGHT)
tdl.setFPS(LIMIT_FPS)

player = GameObject(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, '@', (255, 255, 255))
npc = GameObject(SCREEN_WIDTH // 2 - 5, SCREEN_HEIGHT // 2, '@', (255, 255, 0))
objects = [npc, player]

# generate map (at this point it's not drawn to the screen)
make_map()

while not tdl.event.is_window_closed():
    # draw all objects in the list
    render_all()

    tdl.flush()

    # erase all objects at their old locations, before they move
    for obj in objects:
        obj.clear()

    # handle keys and exit game if needed
    exit_game = handle_keys(REALTIME)
    if exit_game:
        break
