# **Battleship Game**

## **Input Format**
- The player enters a move as row column (e.g., 3 5).
- Ships are read from CSV files (ship_id,row,col).
- Bot ships are generated automatically and saved in bot_ships.csv.


## **Ship Placement Validation**
- Board boundaries are checked: 0 ≤ row, column < 10.
- Ship overlapping is not allowed.
- Ships must have the correct length.
- Invalid or duplicate coordinates are ignored.


## **Updating and Displaying Game State**
- The board is 10×10, with symbols:
    - ~ — empty cell
    - S — ship (hidden on the bot’s board)
    - X — hit
    - M — miss

After each move:
    - Check if a ship is hit or destroyed.
    - If a ship is destroyed, the 8 surrounding cells are automatically marked as M.
    - Update the CSV file data/game_state.csv with columns:
        turn, player_move, player_result, bot_move, bot_result, player_board, bot_board.
    - Both boards are displayed in the terminal with the current state.


## **Bot Logic**
- The bot uses target mode: after a hit, it checks neighboring cells.
- After destroying a ship, it returns to randomly selecting a cell.
 
 
## **Design Decisions & Trade-offs**
- Using CSV to store game state: convenient for analysis, but the file can grow quickly.
- Separation of functions: for displaying, updating boards, and saving the state.
- Simple input validation: prevents errors without complex user input handling.
- Bot strategy: efficient but simple for finding ships.
