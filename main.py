import curses
import time
import random
from animations.blink import blink
from animations.fire import fire
from animations.spaceship import animate_spaceship

TIC_TIMEOUT = 0.1
STARS_AMOUNT = 25
STARS_SYMBOLS = '+*.:'
COROUTINES = []


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

    coorutine_spaceship = animate_spaceship(canvas, row_center, column_center, max_row, max_column)
    COROUTINES.append(coorutine_spaceship)

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
