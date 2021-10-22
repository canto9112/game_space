from toolkit.curses_tools import draw_frame
import asyncio
from toolkit.frames import get_garbage_frame
import random
import os

GARBAGE_DELAY = 50
GARBAGE_DIRECTORY = 'frames/garbage/'


def get_random_garbage(canvas, max_column):
    files = os.listdir(GARBAGE_DIRECTORY)
    garbage_frame = get_garbage_frame(random.choice(files))
    coroutine_garbage = fly_garbage(canvas, random.randint(0, max_column), garbage_frame)
    return coroutine_garbage


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    while row < rows_number:
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed


async def fill_orbit_garbage(canvas, column):
    while True:
        for _ in range(0, random.randint(0, GARBAGE_DELAY)):
            await asyncio.sleep(0)
        await get_random_garbage(canvas, column)

