import asyncio
import curses
import random
import time
from itertools import cycle

from animations.blink import blink
from animations.fire import fire
from animations.space_garbage import fill_orbit_garbage
from toolkit.curses_tools import draw_frame, get_frame_size, read_controls
from toolkit.frames import get_frames
from toolkit.physics import update_speed
from toolkit.obstacles import Obstacle, show_obstacles
from animations.spaceship import animate_spaceship


TIC_TIMEOUT = 0.1
STARS_AMOUNT = 150
STARS_SYMBOLS = '+*.:'
COROUTINES = []
GARBAGE_AMOUNT = 10


# async def animate_spaceship(canvas, max_row, max_column):
#     SPACESHIP_FRAMES = get_frames('rocket')
#     frame_height, frame_width = get_frame_size(SPACESHIP_FRAMES[0])
#     row = max_row // 2 - frame_height // 2
#     column = max_column // 2 - frame_width // 2
#     row_speed, column_speed = 0, 0
#     for frame in cycle(SPACESHIP_FRAMES):
#         draw_frame(canvas, row, column, frame)
#         await asyncio.sleep(0)
#         rows_direction, columns_direction, space_pressed = read_controls(canvas)
#         draw_frame(canvas, row, column, frame, negative=True)
#         row_speed, column_speed = update_speed(row_speed, column_speed, rows_direction, columns_direction)
#         row = row + rows_direction + row_speed
#         if row == max_row - frame_height:
#             row = row - 1
#         elif row == 1:
#             row = row + 1
#         column = column + columns_direction + column_speed
#         if column == max_column - frame_width:
#             column = column - 1
#         elif column == 1:
#             column = column + 1
#         if space_pressed:
#             coroutine_fire = fire(canvas, row, column)
#             COROUTINES.append(coroutine_fire)


def draw(canvas):
    curses.curs_set(False)
    canvas.nodelay(True)
    canvas.border()

    rows, columns = canvas.getmaxyx()
    row_center = rows // 2
    column_center = columns // 2
    max_row = rows - 1
    max_column = columns - 1

    COROUTINES.extend(
        blink(canvas, random.randint(0, max_row), random.randint(0, max_column), random.choice(STARS_SYMBOLS)) for _ in
        range(STARS_AMOUNT))

    coroutine_fire = fire(canvas, row_center, column_center)
    COROUTINES.append(coroutine_fire)

    coroutine_spaceship = animate_spaceship(canvas, max_row, max_column, COROUTINES)
    COROUTINES.append(coroutine_spaceship)

    COROUTINES.extend(fill_orbit_garbage(canvas, max_column) for _ in range(GARBAGE_AMOUNT))

    while True:
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)
        for coroutine in COROUTINES.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                COROUTINES.remove(coroutine)
        if len(COROUTINES) == 0:
            break


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
