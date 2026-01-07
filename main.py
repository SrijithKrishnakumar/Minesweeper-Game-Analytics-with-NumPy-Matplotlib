# main.py

# This is the main entry point of the application.
# It handles the user interface CLI menu and the main game loop.
# It imports all the components from our other modules.2

import time
from minesweeper_game import Minesweeper
from highscores import print_highscores_for_config, qualifies_for_top10, update_highscores_config
from analytics import analytics_mode

# -----------------------
# Gameplay mode
# -----------------------

def play_game_with_config(rows, cols, nBombs):
    """Play a text-based game with explicit configuration."""
    

    current_game = Minesweeper(rows=rows, cols=cols, nBombs=nBombs)
    
    # Show highscores for this config before starting
    print_highscores_for_config(rows, cols, nBombs)

    print("\nCommands:")
    print("  r row col – reveal")
    print("  f row col – flag/unflag")
    print("  exit      – quit\n")

    start_time = None
    while True:
        current_game.display()
        cmd = input(">>> ").lower().strip()

        if cmd == "exit":
            print("Exiting game.")
            return

        parts = cmd.split()
        if len(parts) != 3:
            print("Invalid command. Use: r/f row col")
            continue

        action, r_str, c_str = parts[0], parts[1], parts[2]
        if not (r_str.isdigit() and c_str.isdigit()):
            print("Row and col should be numbers.")
            continue
            
        r, c = int(r_str), int(c_str)
        
        if not current_game.inside(r, c):
            print("Coordinates out of bounds.")
            continue

        # --- First Click Handling ---
        if not current_game.first_click:
            # This is the first move. Place mines *now*
            # using the 'safe' parameter to avoid this click.
            current_game.place_mines(safe=(r, c))
            current_game.first_click = True
            start_time = time.time() # Start timer on first *valid* click

        # --- Game Actions ---
        if action == "r":
            
            hit_mine = current_game.reveal(r, c)
            
            if hit_mine:
                # --- Game Over (Loss) ---
                current_game.display(reveal_mines=True) # Show all mines
               
                elapsed_time = time.time() - start_time if start_time else 0.0
                print("💥 You clicked a mine! Game Over!")
                print(f"Time: {elapsed_time:.2f} seconds")
                return

            if current_game.won():
                # --- Game Over (Win) ---
                current_game.display()
                elapsed_time = time.time() - start_time
                print("🎉 You win!")
                print(f"Time: {elapsed_time:.2f} seconds")
                
                # Check highscores
                if qualifies_for_top10(rows, cols, nBombs, elapsed_time):
                    name = input("You made the top 10! Enter your name: ").strip() or "Anonymous"
                    update_highscores_config(rows, cols, nBombs, name, elapsed_time)
                    print_highscores_for_config(rows, cols, nBombs)
                else:
                    print("Not in top 10. Better luck next time!")
                return

        elif action == "f":
            current_game.toggle_flag(r, c)

        else:
            print("Unknown command. Use 'r' or 'f'.")


def play_game(difficulty):
    """Play using one of three preset difficulties (0,1,2)."""
    if difficulty not in (0, 1, 2):
        difficulty = 1 # Default to Normal
        
    if difficulty == 0:
        rows, cols, mines = 9, 9, 10
    elif difficulty == 1:
        rows, cols, mines = 16, 16, 40
    else:  # difficulty == 2
         rows, cols, mines = 30, 16, 99

    play_game_with_config(rows, cols, mines)


# -----------------------
# CLI entrypoint
# -----------------------
def input_int(prompt, default=None, min_val=None, max_val=None):
    """Utility to prompt for integer input with validation."""
    try:
        
        raw_input = input(prompt).strip()
        if raw_input == "" and default is not None:
            return default
            
       
        numeric_value = int(raw_input)
        
        if (min_val is not None and numeric_value < min_val) or \
           (max_val is not None and numeric_value > max_val):
            print(f"Value out of allowed range ({min_val}..{max_val}).")
            return default
            
        return numeric_value
    except Exception:
        print("Invalid input; using default.")
        return default


if __name__ == "__main__":
    # This block is the first thing that runs
    print("--- Minesweeper ---")
    print("Select mode:")
    print("1 - Play Game")
    print("2 - Analytics Mode")
    mode = input("> ").strip()

    if mode == "1":
        # --- Play Mode ---
        print("Select difficulty or custom configuration:")
        print("  a) Preset difficulties: 0 = Easy, 1 = Normal, 2 = Expert")
        print("  b) Or enter 'custom' to specify rows, cols, mines")
        choice = input("> ").strip().lower()
        
        if choice == "custom":
            
            custom_rows = input_int("Rows (e.g., 9): ", default=16, min_val=1)
            custom_cols = input_int("Cols (e.g., 9): ", default=16, min_val=1)
            max_mines = (custom_rows * custom_cols - 9) # At least 9 safe cells for first click
            custom_mines = input_int(f"Mines (e.g., 10): ", default=40, min_val=1, max_val=max_mines)
            
            if custom_mines is None or custom_mines >= custom_rows * custom_cols:
                print("Invalid mine count; defaulting to 40.")
                custom_mines = 40
                
            play_game_with_config(custom_rows, custom_cols, custom_mines)
        else:
            
            difficulty_input_str = choice if choice in ["0", "1", "2"] else input("Enter difficulty (0,1,2): ").strip()
            
            if difficulty_input_str not in ["0", "1", "2"]:
                print("Invalid difficulty. Defaulting to Normal (1).")
                difficulty_input_str = "1"
                
            
            difficulty_level = int(difficulty_input_str)
            play_game(difficulty_level)

    elif mode == "2":
        # -- Analytics Mode --
        print("Enter analytics configuration.")
        preset = input("Use preset difficulty? (y/n) ").strip().lower()
        
        if preset == "y":
            difficulty_input_str = input("Select difficulty: 0=Easy, 1=Normal, 2=Expert: ").strip()
            if difficulty_input_str not in ["0", "1", "2"]:
                print("Invalid difficulty. Defaulting to Normal (1).")
                difficulty_input_str = "1"
                
            difficulty_level = int(difficulty_input_str)
            
            if difficulty_level == 0:
                r, c, m = 9, 9, 10
            elif difficulty_level == 1:
                r, c, m = 16, 16, 40
            else: # 2
                
                r, c, m = 30, 16, 99
        else:
            # Custom analytics config
            r = input_int("Rows (e.g., 16): ", default=16, min_val=1)
            c = input_int("Cols (e.g., 16): ", default=16, min_val=1)
            max_mines = r * c - 1
            m = input_int(f"Mines (1..{max_mines}): ", default=40, min_val=1, max_val=max_mines)
            if m is None: m = 40 # Handle default case

        
        num_boards_input = input_int("Enter number of boards to generate (e.g., 1000): ", 1000, 1)
        
        analytics_mode(r, c, m, num_boards_input)

    else:
        print("Unknown mode selected. Exiting.")