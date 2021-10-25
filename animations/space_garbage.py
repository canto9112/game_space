import asyncio
import os
import random

from toolkit.curses_tools import draw_frame, get_frame_size
from toolkit.frames import get_garbage_frame
from toolkit.obstacles import Obstacle
from toolkit.sleep import sleep

GARBAGE_DELAY = 50
GARBAGE_DIRECTORY = 'frames/garbage/'

obstacles = []
obstacles_in_last_collisions = []


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    frame_row, frame_column = get_frame_size(garbage_frame)
    obstacle = Obstacle(row, column, frame_row, frame_column)
    obstacles.append(obstacle)

    try:
        while row < rows_number:
            if obstacle in obstacles_in_last_collisions:
                return
            draw_frame(canvas, row, column, garbage_frame)
            await asyncio.sleep(0)
            draw_frame(canvas, row, column, garbage_frame, negative=True)
            row += speed
            obstacle.row = row

    finally:
        obstacles.remove(obstacle)
        if len(obstacles_in_last_collisions) > 0:
            obstacles_in_last_collisions.clear()


async def fill_orbit_garbage(canvas, max_column, coroutines):
    while True:
        await sleep(random.randint(0, GARBAGE_DELAY))
        files = os.listdir(GARBAGE_DIRECTORY)
        garbage_frame = get_garbage_frame(random.choice(files))
        coroutine_garbage = fly_garbage(canvas, random.randint(0, max_column), garbage_frame)
        coroutines.append(coroutine_garbage)
        await sleep(2)
