"""
Utility functions and constants for the Battleship game.

This module defines board settings, ship sizes, direction vectors,
and helper functions for coordinate validation and board display.
"""

BOARD_SIZE = 10

SHIP_SIZES = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

DIRECTIONS_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]

DIRECTIONS_8 = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                (0, 1), (1, -1), (1, 0), (1, 1)]


def in_bounds(r, c):
    """
    Checks whether given coordinates are inside the game board.

    Args:
        r (int): Row index.
        c (int): Column index.

    Returns:
        bool: True if the coordinates are within the board,
        False otherwise.
    """
    return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE


def neighbours_8(r, c):
    """
    Returns all valid neighboring cells in 8 directions.

    Neighbors are limited to cells that are within the board.

    Args:
        r (int): Row index.
        c (int): Column index.

    Returns:
        list: List of (row, col) coordinate tuples.
    """
    return [(r+dr, c+dc) 
            for dr, dc in DIRECTIONS_8 
            if in_bounds(r+dr, c+dc)]


def print_table(board, title):
    """
    Prints the game board to the console.

    Args:
        board (list): 2D list representing the game board.
        title (str): Title printed above the board.
    """
    
    print(f"\n{title}")
    print(" 0 1 2 3 4 5 6 7 8 9")
    i = 0
    for row in board:
        line = ""
        for cell in row:
            line += cell + " "
        print(i, line)
        i += 1