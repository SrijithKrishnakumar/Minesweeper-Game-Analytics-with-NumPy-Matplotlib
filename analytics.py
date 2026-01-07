# analytics.py

# This module contains all logic for the Analytic mode.


from collections import deque, Counter
import numpy as np
import matplotlib.pyplot as plt
import os
from minesweeper_game import Minesweeper 

def count_mine_clusters(mines_set, rows, cols):
    """
    Counts 8-connected clusters of mines using a BFS.
    'mines_set' is a set of (r, c) tuples.
    """
    visited = set()
    clusters = 0
    
    for mine_cell in mines_set:
        if mine_cell in visited:
            # This mine is already part of a cluster we've counted
            continue
            
        # Found the start of a new cluster
        clusters += 1
        
        # Use BFS to find all connected mines in this cluster
        queue = deque([mine_cell])
        visited.add(mine_cell)
        
        while queue:
       
            current_r, current_c = queue.popleft()
            
            # Check all 8 neighbors
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    
                    
                    neighbor_r, neighbor_c = current_r + dr, current_c + dc
                    neighbor_cell = (neighbor_r, neighbor_c)
                    
                    if neighbor_cell in mines_set and neighbor_cell not in visited:
                        # This neighbor is a mine and haven't been noticed yet
                        visited.add(neighbor_cell)
                        queue.append(neighbor_cell)
    return clusters


def analytics_mode(rows, cols, nBombs, num_boards=1000):
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    """
    Runs analytics for a given configuration by generating 'num_boards'.
    Saves the 4 plots to .png files.
    """
    print(f"\nRunning analytics: {num_boards} boards of size {rows}x{cols} with {nBombs} mines...")

  
    board_generator = Minesweeper(rows=rows, cols=cols, nBombs=nBombs)

    # --- Data acummulators ---
    empty_counts = [] # Stores count of '0' cells for each board
    number_counts = Counter() # Stores total counts of '0', '1', '2' etc.
    cluster_counts = [] # Stores cluster count for each board
    # This 2D array will sum the 3x3 neighborhood mine counts for all boards
    neighbourhood_sum = np.zeros((rows, cols), dtype=int)

  
    for _ in range(num_boards):
        # Place mines with 'safe=None' for an unbiased random distribution
        board_generator.place_mines(safe=None)

        # -- 1. White Cells --
        empty_count = sum(1 for r in range(rows) for c in range(cols) if board_generator.values[r][c] == 0)
        empty_counts.append(empty_count)

        # -- 2. Number Distribution --
        for r in range(rows):
            for c in range(cols):
                val = board_generator.values[r][c]
                if val >= 0: # Only count 0-8, not -1 (mines)
                    number_counts[val] += 1

        # -- 3. Mine Clusters --
        clusters = count_mine_clusters(board_generator.mines, rows, cols)
        cluster_counts.append(clusters)

        # -- 4. Neighborhood Heatmap --
        for r in range(rows):
            for c in range(cols):
              
                neighborhood_mine_count = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) in board_generator.mines:
                            neighborhood_mine_count += 1
                # Add this cell's 3x3 count to the total sum
                neighbourhood_sum[r, c] += neighborhood_mine_count

    # --- Plotting ---
    print("Analytics complete. Saving plots...")

    # 1) Histogram of empty (white) cells
    plt.figure(figsize=(10, 6))
    plt.hist(empty_counts, bins=range(min(empty_counts), max(empty_counts) + 2), alpha=0.7, edgecolor='black')
    plt.title(f"Distribution of Empty (0) Cells Per Board ({rows}x{cols}, {nBombs} mines)")
    plt.xlabel("Number of Empty Cells")
    plt.ylabel("Frequency (out of {num_boards} boards)")
    plt.grid(True)
    hist_fname = f"empty_cells_hist_{rows}x{cols}x{nBombs}.png"
    plt.savefig(hist_fname)
    plt.close()

    # 2) Distribution of cell numbers
    numbers = sorted(k for k in number_counts.keys() if k >= 0)
    # Get the *average* count per board by dividing by num_boards
    counts = [number_counts[k] / num_boards for k in numbers]
    plt.figure(figsize=(10, 6))
    plt.bar(numbers, counts, edgecolor='black')
    plt.title(f"Average Cell Values Per Board ({rows}x{cols}, {nBombs} mines)")
    plt.xlabel("Cell Value (0 = blank)")
    plt.ylabel("Average Count Per Board")
    plt.grid(True)
    numbers_fname = f"number_cells_dist_{rows}x{cols}x{nBombs}.png"
    plt.savefig(numbers_fname)
    plt.close()

    # 3) Histogram of mine clusters
    plt.figure(figsize=(10, 6))
    plt.hist(cluster_counts, bins=range(min(cluster_counts), max(cluster_counts) + 2), alpha=0.7, edgecolor='black')
    plt.title(f"Distribution of Mine Clusters Per Board ({rows}x{cols}, {nBombs} mines)")
    plt.xlabel("Number of Mine Clusters")
    plt.ylabel("Frequency (out of {num_boards} boards)")
    plt.grid(True)
    clusters_fname = f"mine_clusters_hist_{rows}x{cols}x{nBombs}.png"
    plt.savefig(clusters_fname)
    plt.close()

    # 4) Heatmap of 3x3 neighborhood mine count
    plt.figure(figsize=(12, 9)) # Adjusted figsize for better layout
    # Get the average by dividing the sum by num_boards
    neighbourhood_avg = neighbourhood_sum / num_boards
    plt.imshow(neighbourhood_avg, interpolation='nearest', cmap='viridis')
    plt.colorbar(label="Average mines in 3x3 neighbourhood")
    plt.title(f"Average 3x3 Neighbourhood Mine Count ({rows}x{cols}, {nBombs} mines)")
    heatmap_fname = f"mine_neighbourhood_heatmap_{rows}x{cols}x{nBombs}.png"
    plt.savefig(heatmap_fname)
    plt.close()

    print("Plots saved:")
    print(f" - {hist_fname}")
    print(f" - {numbers_fname}")
    print(f" - {clusters_fname}")
    print(f" - {heatmap_fname}\n")