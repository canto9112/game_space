import asyncio
import os
import random

from animations.explosion import explode
from toolkit.curses_tools import draw_frame, get_frame_size
from toolkit.frames import get_garbage_frame
from toolkit.game_scenario import get_garbage_delay_tics
from toolkit.obstacles import Obstacle
from toolkit.sleep import sleep


GARBAGE_DIRECTORY = 'frames/garbage/'

obstacles = []
obstacles_in_last_collisions = []


async def fly_garbage(canvas, column, frame, speed=0.5):
    speed = max(speed, 0.1)
    sprite_rows, sprite_columns = get_frame_size(frame)
    row = 0
    obstacle = Obstacle(row, column, sprite_rows, sprite_columns)
    obstacles.append(obstacle)
    try:
        rows, columns = canvas.getmaxyx()
        max_row, max_column = rows - sprite_rows, columns - sprite_columns
        column = max(column, 0)
        column = min(column, max_column)
        while row < max_row:
            draw_frame(canvas, row, column, frame)
            await asyncio.sleep(0)
            draw_frame(canvas, row, column, frame, negative=True)
            if obstacle in obstacles_in_last_collisions:
                await explode(canvas, row + sprite_rows//2, column + sprite_columns//2)
                return
            row += speed
            obstacle.row = row
    finally:
        obstacles.remove(obstacle)
        if obstacle in obstacles_in_last_collisions:
            obstacles_in_last_collisions.remove(obstacle)

