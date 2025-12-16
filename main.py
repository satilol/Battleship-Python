"""
Entry point for the Battleship game.

Starts the game and runs the main gameplay loop.
"""

from src.gameplay import gameplay_loop

def main():
    """
    Launches the Battleship game.
    """
    
    print("Welcome to Battleship! May the odds be ever in your favor.")
    gameplay_loop()
    print("Game over!")
    
if __name__ == "__main__":
    main()