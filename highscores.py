# highscores.py

# This module handles all highscores (reading/writing to JSONfile).

import json
import os

# This constant is now defined the module that uses it.
HIGHSCORES_FILE = "minesweeper_highscores.json"

def load_highscores():
    """
    Load highscores JSON from disk.
    The data structure is a dictionary, e.g.:
    { 
      "9x9x10": [{"name": "Alice", "time": 12.34}, ...],
      "16x16x40": [...]
    }
    """
    if os.path.exists(HIGHSCORES_FILE):
        try:
            with open(HIGHSCORES_FILE, "r") as f:
                return json.load(f)
        except Exception:
            # If file is corupted, return an empty structure
            return {}
    return {}


def save_highscores(data):
    """Saves the highscores data (dictionary) back to the JSON file."""
    with open(HIGHSCORES_FILE, "w") as f:
        json.dump(data, f, indent=2)


def update_highscores_config(rows, cols, nBombs, name, elapsed_time):
    """
    Inserts a new score into the highscore list for a specific configuration.
    This function reads, updates, sorts, truncates (top 10), and saves.
    """
    data = load_highscores()
    
    # The key uniquely identifies the board configuration
    key = f"{rows}x{cols}x{nBombs}"
    scores = data.get(key, [])
    
    scores.append({"name": name, "time": round(elapsed_time, 2)})
    
    # Sort the list of scores by time (ascending) and keep only the top 10
    scores = sorted(scores, key=lambda x: x["time"])[:10]
    
    data[key] = scores
    save_highscores(data)
    return scores


def qualifies_for_top10(rows, cols, nBombs, elapsed_time):
    """
    Checks if a given time is fast enough to make the top 10.
    This avoids asking for a name if the player didn't win fast enough.
    """
    data = load_highscores()
    key = f"{rows}x{cols}x{nBombs}"
    scores = data.get(key, [])
    
    if len(scores) < 10:
        # If there are fewer than 10 scores, any win qualifies
        return True
        
    # Check if the new time is faster than the slowest time in the top 10
    # The slowest time is the last one in the sorted list.
    return elapsed_time < scores[-1]["time"]


def print_highscores_for_config(rows, cols, nBombs):
    """Pretty-prints the highscore table for a specific configuration."""
    data = load_highscores()
    key = f"{rows}x{cols}x{nBombs}"
    scores = data.get(key, [])
    
    if not scores:
        print(f"No highscores recorded yet for {key}.")
        return
        
    print(f"\nTop {len(scores)} highscores for {key}:")
   
    for i, score_entry in enumerate(scores, 1):
        print(f"{i}. {score_entry['name']} — {score_entry['time']:.2f} seconds")
    print()