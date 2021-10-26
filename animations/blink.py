import curses
import random

from toolkit.sleep import sleep


async def blink(canvas, row, column, symbol='*'):
    await sleep(random.randint(0, 100))
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await sleep(20)
        canvas.addstr(row, column, symbol)
        await sleep(3)
        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await sleep(5)
        canvas.addstr(row, column, symbol)
        await sleep(3)
