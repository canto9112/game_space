import asyncio
import curses
import random

async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(0, 20):
            await asyncio.sleep(0)
        canvas.addstr(row, column, symbol)
        for _ in range(0, 3):
            await asyncio.sleep(0)
        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(0, 5):
            await asyncio.sleep(0)
        canvas.addstr(row, column, symbol)
        for _ in range(0, 3):
            await asyncio.sleep(0)
        for _ in range(0, random.randint(0, 10)):
            await asyncio.sleep(0)