#!/usr/bin/python3
"""
A Curses implementation of Conway's Game Of Life.

This automation is governed by simple rules:
    --> Live cells
        (+) If a cell has 0 or 1 neighbours, it dies
        (+) If a cell has 2 or 3 neighbours, it lives
        (+) If a cell has 4 or more neighbours, it dies

    --> Dead cells
        (+) If a cell has 3 neighbours, it comes to life

    Each 'tick' happens simultaneously.
"""

import curses
import time

DEAD = 0
ALIVE = 1
TICK_LENGTH = 0.2


def setup_curses():
    curses.start_color()
    curses.use_default_colors()
    curses.cbreak()  # No need for [Return]
    curses.noecho()  # Stop keys being printed
    curses.curs_set(0)  # Invisible cursor


def add_to_board(board, pattern):
    for point in pattern:
        board[point] = ALIVE


def get_neighbours(point):
    x, y = point
    yield x + 1, y
    yield x + 1, y + 1
    yield x, y + 1
    yield x - 1, y + 1
    yield x - 1, y
    yield x - 1, y - 1
    yield x, y - 1
    yield x + 1, y - 1


def clear_display(stdscr):
    curses.nocbreak()
    curses.echo()
    curses.curs_set(1)
    stdscr.keypad(False)
    stdscr.clear()
    curses.endwin()


def next_iteration(board, custom_size):
    # Initialise a blank board to copy results onto
    newboard = new_board(custom_size)
    for coord, alive in board.items():
        neighbours = get_neighbours(coord)

        # Count the number of living neighbours
        alive_neighbours = 0
        for neighbour in neighbours:
            try:
                if board[neighbour] == ALIVE:
                    alive_neighbours += 1
            except KeyError:
                # value isn't on the board
                pass
        if alive:
            if alive_neighbours in [0, 1]:
                # Cell is underpopulated and dies
                newboard[coord] = DEAD
            elif alive_neighbours in [2, 3]:
                # Cell is healthy and lives
                newboard[coord] = ALIVE
            else:
                # Cell is overpopulated and dies
                newboard[coord] = DEAD
        else:
            if alive_neighbours == 3:
                # Neighbours reproduce
                newboard[coord] = ALIVE
    return newboard
    

def print_board(stdscr, board):
    stdscr.refresh()
    for (x, y), alive in board.items():
        stdscr.addstr(y, x, "@" if alive else " ")
    stdscr.refresh()


def new_board(custom_size):
    import os
    if custom_size is None:
        termsize = os.get_terminal_size()
        maxx, maxy = termsize.columns - 1, termsize.lines - 1
    else:
        maxx, maxy = custom_size[0], custom_size[1]
    return {(x, y): DEAD for x in range(maxx) for y in range(maxy)}


def parse_file(filename):
    pattern = []
    with open(filename) as f:
        lines = f.readlines()
        # Test all lines are same length
        if len(set(len(line.strip()) for line in lines)) == 1:
            # Find custom size of board (x, y)
            custom_size = (len(lines[0]), len(lines))
            for line_no, line in enumerate(lines):
                for char_no, char in enumerate(line):
                    if char == "@":
                        pattern.append((char_no, line_no))
            return pattern, custom_size

        else:
            raise FileNotFoundError



def main(pattern=None, custom_size=None):
    board = new_board(custom_size)
    if pattern is None:
        # Basic Gosper Glider:
        pattern = [(0, 2), (1, 0), (1, 2), (2, 1), (2, 2)]
        # pattern = [(0, 3), (1, 3), (2, 1), (2, 3), (3, 1), (3, 3), (4, 1), (4, 3), (5, 3), (6, 3)]

    add_to_board(board, pattern)
    stdscr = curses.initscr()
    setup_curses()

    while True:
        try:
            print_board(stdscr, board)
            time.sleep(TICK_LENGTH)
            board = next_iteration(board, custom_size)

        except KeyboardInterrupt:
            break
        except:
            clear_display(stdscr)
            raise


    clear_display(stdscr)
    print("Thanks for playing!")



if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        input_file = sys.argv[1]
        try:
            main(*parse_file(input_file))
        except FileNotFoundError:
            print("File was not found or inconsistent.")
    elif len(sys.argv) > 2:
        print(__doc__)
        quit()
    else:
        main()
