# minesweeper_game.py

# This file contains the main 'MIndsweeper' class, which acts as the game engine.


import random
from collections import deque

class Minesweeper:
    """
    Minesweeper game engine.
    ... (docstring) ...
    """

    def __init__(self, difficulty=None, rows=None, cols=None, nBombs=None):
        
        
        if rows is not None and cols is not None and nBombs is not None:
            self.rows, self.cols, self.nBombs = rows, cols, nBombs
        else:
            if difficulty == 0:
                self.rows, self.cols, self.nBombs = 9, 9, 10
            elif difficulty == 1 or difficulty is None:
                self.rows, self.cols, self.nBombs = 16, 16, 40
            elif difficulty == 2:
               
                self.rows, self.cols, self.nBombs = 30, 16, 99
            else:
                self.rows, self.cols, self.nBombs = 16, 16, 40

        # Game state
        self.revealed = set()
        self.flags = set()
        self.mines = set()
        # 'values' holds the pre-calculated state of the solved board
        # -1 = Mine
        #  0 = Blank
        # 1-8 = Number
        self.values = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.first_click = False # Flag to track if the timer should start

    def inside(self, r, c):
        """Helper function to check if a coordinate is within the board bounds."""
        return 0 <= r < self.rows and 0 <= c < self.cols

    def neighbors(self, r, c):
        """
        Yield 8-connected neighbors for a given cell (r, c).
        This is a generator, which is efficient.
        """
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                
                
                neighbor_r, neighbor_c = r + dr, c + dc
                
                if self.inside(neighbor_r, neighbor_c):
                    yield neighbor_r, neighbor_c

    def place_mines(self, safe=None):
        """
        Place mines on the board.
        If 'safe' is provided (e.g., (r, c)), no mine will be placed
        on that cell or its 8 neighbors. This is for the "safe-first-click" rule.
        If 'safe' is None (for analytics), mines are placed completely randomly.
        """
        all_cells = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        
        if safe is None:
            # Analytics mode: no safe area
            candidates = all_cells[:]
        else:
            # Gameplay mode: create a "safe zone"
            avoid = {safe, *self.neighbors(*safe)}
            candidates = [c for c in all_cells if c not in avoid]
            if len(candidates) < self.nBombs:
                # This is a rare edge case (e.g, 3x3 board with 8 mines)
                candidates = all_cells[:]

        self.mines = set(random.sample(candidates, self.nBombs))

        # After placing mines, pre caculate the 'values' for all cells
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) in self.mines:
                    self.values[r][c] = -1 # -1 represents a mine
                else:
                    # Count mines in the 8-cell neighborhood
                    self.values[r][c] = sum((nr, nc) in self.mines for nr, nc in self.neighbors(r, c))

    def reveal(self, r, c):
        """
        Reveal a cell. Returns True if a mine was hit (loss), False otherwise.
        If the cell is '0', this function triggers a "flood-fill" (using BFS)
        to reveal all adjacent '0's and their neighboring numbers.
        """
        if (r, c) in self.flags:
            # Cannot reveal a flagged cell
            return False

        if (r, c) in self.mines:
            self.revealed.add((r, c))
            return True  # B-O-O-M! Hit a mine.

        # Use a queue for a Breadth-First Search (BFS) to flood-fill
        queue = deque([(r, c)])

        while queue:
           
            current_r, current_c = queue.popleft()
            
            if (current_r, current_c) in self.revealed:
                continue
                
            self.revealed.add((current_r, current_c))

            # If this cell is a '0' (blank), add its neighbors to the queue
            if self.values[current_r][current_c] == 0:
                
                for neighbor_r, neighbor_c in self.neighbors(current_r, current_c):
                    if (neighbor_r, neighbor_c) not in self.revealed and (neighbor_r, neighbor_c) not in self.flags:
                        queue.append((neighbor_r, neighbor_c))
        return False # No mine hit

    def toggle_flag(self, r, c):
        """Flag or unflag a cell. Cannot flag a revealed cell."""
        if (r, c) in self.revealed:
            return # Don't allow flagging a revealed cell
            
        if (r, c) in self.flags:
            self.flags.remove((r, c))
        else:
            self.flags.add((r, c))

    def won(self):
        """Win condition: all non-mine cells are revealed."""
        return len(self.revealed) == self.rows * self.cols - self.nBombs

    def display(self, reveal_mines=False):
        """Textual board display."""
        # Column headers
        print("\n   " + " ".join(f"{i:2d}" for i in range(self.cols)))
        
        for r in range(self.rows):
            
            row_str_parts = []
            for c in range(self.cols):
                if (r, c) in self.revealed:
                   
                    cell_value = self.values[r][c]
                    # Use '.' for 0 (blank) and the number otherwise
                    row_str_parts.append(". " if cell_value == 0 else f"{cell_value} ")
                elif (r, c) in self.flags:
                    row_str_parts.append("F ") # 'F' for Flag
                else:
                    if reveal_mines and (r, c) in self.mines:
                        row_str_parts.append("* ") # '*' for Mine (on game over)
                    else:
                        row_str_parts.append("# ") # '#' for Unrevealed
            print(f"{r:2d} " + "".join(row_str_parts))
        print()