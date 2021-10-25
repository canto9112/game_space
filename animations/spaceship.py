import asyncio

from itertools import cycle
from toolkit.curses_tools import read_controls, draw_frame, get_frame_size
from toolkit.frames import get_frames
from toolkit.physics import update_speed
from animations.fire import fire

SPACESHIP_FRAMES = get_frames('rocket')


async def animate_spaceship(canvas, max_row, max_column, coroutines):
    frame_height, frame_width = get_frame_size(SPACESHIP_FRAMES[0])
    row = max_row // 2 - frame_height // 2
    column = max_column // 2 - frame_width // 2
    row_speed, column_speed = 0, 0
    for frame in cycle(SPACESHIP_FRAMES):
        draw_frame(canvas, row, column, frame)
        await asyncio.sleep(0)
        rows_direction, columns_direction, space_pressed = read_controls(canvas)
        draw_frame(canvas, row, column, frame, negative=True)
        row_speed, column_speed = update_speed(row_speed, column_speed, rows_direction, columns_direction)
        row = row + rows_direction + row_speed
        if row == max_row - frame_height:
            row = row - 1
        elif row == 1:
            row = row + 1
        column = column + columns_direction + column_speed
        if column == max_column - frame_width:
            column = column - 1
        elif column == 1:
            column = column + 1

        if space_pressed:
            coroutine_fire = fire(canvas, row, column)
            coroutines.append(coroutine_fire)

