import curses
import random
import time

from animations.blink import blink
from animations.fire import fire
from animations.space_garbage import fill_orbit_garbage
from animations.spaceship import animate_spaceship
from toolkit.frames import get_garbage_frame

TIC_TIMEOUT = 0.1
STARS_AMOUNT = 150
STARS_SYMBOLS = '+*.:'
COROUTINES = []
GARBAGE_AMOUNT = 10

garbage_frame = get_garbage_frame('hubble.txt')


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

    coroutine_spaceship = animate_spaceship(canvas, max_row, max_column)
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
