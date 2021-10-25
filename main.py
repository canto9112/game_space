import curses
import random
import time

from animations.blink import blink
from animations.fire import fire
from animations.space_garbage import fill_orbit_garbage, obstacles
from animations.spaceship import animate_spaceship
from toolkit.obstacles import show_obstacles


TIC_TIMEOUT = 0.1
STARS_AMOUNT = 150
STARS_SYMBOLS = '+*.:'
COROUTINES = []
GARBAGE_AMOUNT = 3


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
    COROUTINES.append(animate_spaceship(canvas, max_row, max_column, COROUTINES))
    COROUTINES.append(fire(canvas, row_center, column_center))
    COROUTINES.extend(fill_orbit_garbage(canvas, max_column, COROUTINES) for _ in range(GARBAGE_AMOUNT))
    COROUTINES.append(show_obstacles(canvas, obstacles))

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
