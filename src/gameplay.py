import csv
import random
from src.utils import BOARD_SIZE, in_bounds, neighbours_8
from src.ship_input import read_player_ships, save_ships
from src.bot_generation import generate_bot_ships, save_bot_ships

GAME_STATE_FILE = "data/game_state.csv"

def init_game_state_csv():
    """
    Initializes the CSV file used to store game state history.

    Creates the file and writes the header row.
    """
    
    with open(GAME_STATE_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["turn",
                         "player_move",
                         "player_result",
                         "bot_move",
                         "bot_result",
                         "player_board",
                         "bot_board"])
        
        
def save_game_state(turn, player_move, player_result, 
                    bot_move, bot_result, player_board, bot_board):
    """
    Appends the current game state to the CSV file.

    Args:
        turn (int): Current turn number.
        player_move (tuple): Player move coordinates (row, col).
        player_result (str): Result of the player's move.
        bot_move (tuple): Bot move coordinates (row, col).
        bot_result (str): Result of the bot's move.
        player_board (list): Player board state.
        bot_board (list): Bot board state.
    """
    
    with open(GAME_STATE_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([turn,
                         f"{player_move[0]} {player_move[1]}",
                         player_result,
                         f"{bot_move[0]} {bot_move[1]}",
                         bot_result,
                         "".join("".join(row) for row in player_board),
                         "".join("".join(row) for row in bot_board)])


def init_board():
    """
    Creates an empty game board.

    Returns:
        list: 2D list filled with water symbols ("~").
    """
    return [["~"]*BOARD_SIZE for _ in range(BOARD_SIZE)]


def place_ships_on_board(board, ships):
    """
    Places ships on the board.

    Args:
        board (list): Game board.
        ships (dict): Dictionary of ships with coordinates.
    """
    for ship in ships.values():
        for r, c in ship:
            board[r][c] = "S"


def print_board(board, hide_ships=False):
    """
    Prints the board to the console.

    Args:
        board (list): Game board.
        hide_ships (bool): If True, ship cells are hidden.
    """
    print(" " + " ".join(str(i) for i in range(BOARD_SIZE)))
    for i, row in enumerate(board):
        display_row = []
        for cell in row:
            if hide_ships and cell == "S":
                display_row.append("~")
            else:
                display_row.append(cell)
        print(str(i) + " " + " ".join(display_row))
        
        
def mark_misses(board, ship):
    """
    Marks cells around a destroyed ship as misses.

    Args:
        board (list): Game board.
        ship (list): List of ship coordinates.
    """
    for r, c in ship:
        for nr, nc in neighbours_8(r, c):
            if in_bounds(nr, nc) and board[nr][nc] == "~":
                board[nr][nc] = "M"
                
                
def read_ships_from_csv(path):
    """
    Reads ship positions from a CSV file.

    Args:
        path (str): Path to the CSV file.

    Returns:
        dict: Dictionary mapping ship_id to coordinate lists.
    """
    ships = {}
    with open(path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ship_id = int(row["ship_id"])
            r = int(row["row"])
            c = int(row["col"])
            ships.setdefault(ship_id, []).append((r, c))
    return ships


def update_board(board, ships, hits):
    """
    Updates the board with hit markers.

    Args:
        board (list): Game board.
        ships (dict): Dictionary of ships.
        hits (set): Set of hit coordinates.
    """
    for ship in ships.values():
        for r, c in ship:
            if (r, c) in hits:
                board[r][c] = "X"
                
                
def gameplay_loop():
    """
    Runs the main gameplay loop.

    Handles player input, bot moves, hit detection,
    ship destruction, and win condition checking.
    """
    player_board = init_board()
    bot_board = init_board()
    
    player_hits = set()
    bot_hits = set()
    
    destroyed_bot_ships = set()
    destroyed_player_ships = set()
    
    target_mode = False
    target_stack = []
    
    player_ships = read_player_ships()
    save_player_path = "data/player_ships.csv"
    save_ships(player_ships, save_player_path)
    
    bot_ships = generate_bot_ships()
    save_bot_path = "data/bot_ships.csv"
    save_bot_ships(bot_ships, save_bot_path)
    
    player_ships_dict = read_ships_from_csv(save_player_path)
    bot_ships_dict = read_ships_from_csv(save_bot_path)
    
    place_ships_on_board(player_board, player_ships_dict)
    
    init_game_state_csv()
    
    turn = 1
    while True:
        print(f"\n--- Turn {turn} ---")
        print("\nPlayer Board:")
        print_board(player_board)
        print("\nBot Board:")
        print_board(bot_board)
    
    
        while True:
            move = input("Enter your move r c: ")
            try:
                r, c = map(int, move.split())
                if in_bounds(r, c) and (r, c) not in player_hits:
                    break
                else:
                    print("Invalid or repeated move.")
            except:
                print("Wrong format.")
            
        player_hits.add((r, c))
        player_result = "Miss"
        hit_ship = None    
        for ship_id, ship in bot_ships_dict.items():
            if (r, c) in ship:
                hit_ship = ship
                break
                
        if hit_ship:
            print("Hit.")
            bot_board[r][c] = "X"
            player_result = "Hit"
            for ship_id, ship in bot_ships_dict.items():
                if all(cell in player_hits for cell in ship) and ship_id not in destroyed_player_ships:
                    print("Ship destroyed.")
                    destroyed_player_ships.add(ship_id)
                    mark_misses(bot_board, ship)
                    player_result = "Ship destroyed"
        
        else:
            print("Miss.")
            bot_board[r][c] = "M"
            player_result = "Miss"
        
        
        if target_mode and target_stack:
            r_bot, c_bot = target_stack.pop()
        else:
            while True:
                r_bot = random.randint(0, BOARD_SIZE-1)
                c_bot = random.randint(0, BOARD_SIZE-1)
                if(r_bot, c_bot) not in bot_hits:
                    break
        
        print(f"Bot moves: {r_bot} {c_bot}")
        bot_hits.add((r_bot, c_bot))
        hit_ship = None 
        for ship_id, ship in player_ships_dict.items():
            if (r_bot, c_bot) in ship:
                hit_ship = ship
                break
               
        bot_result = "Miss"
        if hit_ship:
            print("Bot hit!")
            player_board[r_bot][c_bot] = "X"
            bot_result = "Hit"
            for nr, nc in neighbours_8(r_bot, c_bot):
                if in_bounds(nr, nc) and (nr, nc) not in bot_hits:
                    target_stack.append((nr, nc))
            target_mode = True
                
        else:
            print("Bot miss.")
            player_board[r_bot][c_bot] = "M"
            bot_result = "Miss"
        
        for ship_id, ship in player_ships_dict.items():
            if all(cell in bot_hits for cell in ship) and ship_id not in destroyed_bot_ships:
                print("Bot destroyed a ship.")
                destroyed_bot_ships.add(ship_id)
                mark_misses(player_board, ship)
                bot_result = "Ship destroyed"
                target_stack.clear()
                target_mode = False

        save_game_state(turn, (r, c), player_result,
                        (r_bot, c_bot), bot_result,
                        player_board, bot_board)

        if all(all(cell in player_hits for cell in ship) for ship in bot_ships_dict.values()):
            print("Player wins.")
            break
    
        if all(all(cell in bot_hits for cell in ship) for ship in player_ships_dict.values()):
            print("Bot wins.")
            break
    
        turn += 1
        
    print("\n--- Final Boards ---")
    print("\nPlayer Board:")
    print_board(player_board)
    print("\nBot Board:")
    print_board(bot_board, hide_ships=False)
