import asyncio
import curses
import os
import random
import time
from itertools import cycle

from animations.blink import blink
from animations.fire import fire
from animations.space_garbage import fly_garbage, obstacles, obstacles_in_last_collisions
from toolkit.curses_tools import draw_frame, get_frame_size, read_controls
from toolkit.frames import get_frames, get_frame
from toolkit.game_scenario import get_garbage_delay_tics, PHRASES
from toolkit.obstacles import show_obstacles
from toolkit.physics import update_speed
from toolkit.sleep import sleep

GARBAGE_DIRECTORY = 'frames/garbage/'
SPACESHIP_FRAMES = 'frames/rocket'
GAME_OVER_DIRECTORY = 'frames/game_over/'
TIC_TIMEOUT = 0.1
STARS_AMOUNT = 150
STARS_SYMBOLS = '+*.:'
COROUTINES = []
GARBAGE_AMOUNT = 3
YEAR = 1957
WEAPON_PERMIT_YEAR = 2020
DEBUG = False


async def show_game_over(canvas):
    rows, columns = canvas.getmaxyx()
    file = os.listdir(GAME_OVER_DIRECTORY)
    game_over_frame = get_frame(GAME_OVER_DIRECTORY, file[0])
    frame_rows, frame_columns = get_frame_size(game_over_frame)
    while True:
        draw_frame(canvas, (rows - frame_rows) / 2, (columns - frame_columns) / 2, game_over_frame)
        await sleep(1)


async def animate_spaceship(canvas, max_row, max_column, coroutines, obstacles):
    spaceship_frames = get_frames(SPACESHIP_FRAMES)
    frame_height, frame_width = get_frame_size(spaceship_frames[0])
    row = max_row // 2 - frame_height // 2
    column = max_column // 2 - frame_width // 2
    row_speed, column_speed = 0, 0
    for frame in cycle(spaceship_frames):
        draw_frame(canvas, row, column, frame)
        await asyncio.sleep(0)
        rows_direction, columns_direction, space_pressed = read_controls(canvas)
        draw_frame(canvas, row, column, frame, negative=True)
        row_speed, column_speed = update_speed(row_speed, column_speed, rows_direction, columns_direction)

        for obstacle in obstacles:
            if obstacle.has_collision(row, column, frame_height, frame_width):
                obstacles_in_last_collisions.append(obstacle)
                coroutines.append(show_game_over(canvas))
                return

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

        if space_pressed and YEAR >= WEAPON_PERMIT_YEAR:
            coroutines.append(fire(canvas, row, column+2, obstacles))


async def count_years(canvas):
    global YEAR
    rows, columns = canvas.getmaxyx()
    row, column = rows - 2, 5
    while True:
        phrase = PHRASES.get(YEAR, '')
        message = f'Year {YEAR}. {phrase}'
        canvas.addstr(row, column, message)
        await sleep(10)
        YEAR += 1


async def fill_orbit_garbage(canvas, max_column):
    while True:
        garbage_delay_tics = get_garbage_delay_tics(YEAR)
        files = os.listdir(GARBAGE_DIRECTORY)
        garbage_frame = get_frame(GARBAGE_DIRECTORY, random.choice(files))
        coroutine_garbage = fly_garbage(canvas, random.randint(0, max_column), garbage_frame)
        COROUTINES.append(coroutine_garbage)
        await sleep(garbage_delay_tics)


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
    COROUTINES.extend([
        animate_spaceship(canvas, max_row, max_column, COROUTINES, obstacles),
        fire(canvas, row_center, column_center, obstacles),
        count_years(canvas.derwin(max_row // 3, max_column // 3)),
        fill_orbit_garbage(canvas, max_column)
    ])

    if DEBUG:
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
