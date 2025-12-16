import random
import csv
from src.utils import BOARD_SIZE,  SHIP_SIZES, neighbours_8, in_bounds
from src.ship_input import valid_all


def generate_bot_ships():
    """
    Generates a valid set of ships for the bot.

    Ships are generated randomly according to SHIP_SIZES.
    Each new ship is validated together with previously
    generated ships to ensure correct placement.

    Returns:
        list: List of ships, where each ship is a list of
        (row, col) coordinate tuples.
    """
    ships = []
    
    for size in SHIP_SIZES:
        while True:
            ship = random_ship(size)
            ships.append(ship)
            
            if valid_all(ships):
                break
            ships.pop()
    return ships


def random_ship(size):
    """
    Generates a random ship of a given size.

    The ship is placed either horizontally or vertically
    within the board boundaries.

    Args:
        size (int): Length of the ship.

    Returns:
        list: List of (row, col) coordinate tuples
        representing the ship.
    """
    
    direction = random.choice(["H", "V"])
    
    if direction == "H":
        row = random.randint(0, BOARD_SIZE-1)
        col = random.randint(0, BOARD_SIZE-size)
        return [(row, col+i) for i in range(size)]
    
    else:
        row = random.randint(0, BOARD_SIZE-size)
        col = random.randint(0, BOARD_SIZE-1)
        return [(row+i, col) for i in range(size)]
    

def save_bot_ships(ships, path):
    """
    Saves bot ship positions to a CSV file.

    Each ship is assigned a unique ship_id. Every row
    in the CSV file represents a single ship cell.

    Args:
        ships (list): List of ships, where each ship is a list
        of (row, col) coordinate tuples.
        path (str): Path to the output CSV file.
    """
    
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ship_id", "row", "col"])
        
        for i, ship in enumerate(ships):
            for r, c in ship:
                writer.writerow([i, r, c])