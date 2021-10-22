import asyncio

from itertools import cycle
from toolkit.curses_tools import read_controls, draw_frame, get_frame_size
from toolkit.frames import get_frames

SPACESHIP_FRAMES = get_frames('rocket')


async def animate_spaceship(canvas, row, column, max_row, max_column, ):
    frame_height, frame_width = get_frame_size(SPACESHIP_FRAMES[0])

    row = max_row // 2 - frame_height // 2
    column = max_column // 2 - frame_width // 2

    for frame in cycle(SPACESHIP_FRAMES):
        draw_frame(canvas, row, column, frame)
        await asyncio.sleep(0)
        rows_direction, columns_direction, space_pressed = read_controls(canvas)

        draw_frame(canvas, row, column, frame, negative=True)

        row = row + rows_direction
        if row == max_row - frame_height:
            row = row - 1
        elif row == 1:
            row = row + 1

        column = column + columns_direction
        if column == max_column - frame_width:
            column = column - 1
        elif column == 1:
            column = column + 1

