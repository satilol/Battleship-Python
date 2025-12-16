import csv
from src.utils import BOARD_SIZE, SHIP_SIZES, neighbours_8, in_bounds


def read_player_ships():
    """
    Reads ship positions entered by the player from standard input.

    The player is prompted to enter ship coordinates for each ship
    size defined in SHIP_SIZES. Input is validated to ensure correct
    ship size, board boundaries, and that ships do not touch each other.

    Returns:
        list: List of ships, where each ship is a list of
        (row, col) coordinate tuples.
    """
    
    ships = []
    print("Enter the ships in format r c, r c, ...: ")

    for size in SHIP_SIZES:
        while True:
            raw = input(f"Ship size {size}: ")
            coords = [tuple(map(int, x.split())) for x in raw.split(",")] 

            if len(coords) != size:
                print("Wrong size.")
                continue
            
            if not all(in_bounds(r,c) for r, c in coords):
                print("Out of the bounds.")
                continue
            
            ships.append(coords)
            if valid_all(ships):
                break
            ships.pop()
            print("Ships touch each other.")
            
    return ships


def valid_all(ships):
    """
    Validates that ships do not overlap or touch each other.

    Ships are considered invalid if any of their cells overlap
    or touch another ship, including diagonally.

    Args:
        ships (list): List of ships, where each ship is a list
        of (row, col) coordinate tuples.

    Returns:
        bool: True if all ships are placed correctly,
        False otherwise.
    """
    
    occupied = set()
    for ship in ships:
        for r, c in ship:
            for nr, nc in neighbours_8(r, c):
                if(nr, nc) in occupied:
                    return False
        for r, c in ship:
            occupied.add((r, c))
    return True


def save_ships(ships, path):
    """
    Saves player ship positions to a CSV file.

    Each ship is assigned a unique ship_id. Every row in the
    CSV file represents a single ship cell.

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