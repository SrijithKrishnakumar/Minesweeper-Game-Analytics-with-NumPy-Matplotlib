## Project Overview

- Text-based Minesweeper engine with configurable board size and mine count (including preset difficulties: Easy, Normal, Expert).[file:4][file:5]  
- High score tracking with JSON persistence by configuration (rows × columns × mines).[file:3]  
- Analytics mode that simulates many boards and produces data-driven visualizations of game structure and mine distribution.[file:1][file:5]

## Repository Structure

- `main.py` – Entry point with menu for Play Mode and Analytics Mode, difficulty selection, and custom configuration input.[file:5]  
- `minesweeper_game.py` – Core `Minesweeper` engine (board generation, mine placement, flood-fill reveal, flags, win condition, console display).[file:4]  
- `analytics.py` – Analytics pipeline that simulates boards and generates plots using NumPy and Matplotlib.[file:1]  
- `highscores.py` – High score load/save logic using a JSON file keyed by board configuration.[file:3]  
- `MIS41110-Project-Report-Group-7-2.pdf` – Project report with background, design, and results (for academic reference).[file:2]

## Analytics Mode

The **Analytics Mode** is designed to treat Minesweeper boards as a dataset and extract patterns that help understand difficulty and board dynamics.[file:1][file:5] For a given configuration `(rows, cols, nBombs)`, it:

### 1. Board Simulation

- Generates `numboards` random boards using the same game engine as in Play Mode, but without a safe-first-click constraint for unbiased mine distributions.[file:1][file:4]  
- Uses the `Minesweeper` class to place mines and compute the numeric values for all cells on each board.[file:1][file:4]

### 2. Key Metrics

- **Empty cell count per board (0-cells)**  
  - Counts the number of cells with value `0` (no adjacent mines) on each generated board.[file:1]  
  - Interprets this as “open space” that makes a board more forgiving, analogous to low-friction paths in a business process.

- **Cell value distribution (0–8)**  
  - Aggregates how many cells show each number (0–8) across all boards and divides by `numboards` to get average counts.[file:1]  
  - Acts as a risk profile: higher counts of large numbers indicate denser local risk areas, similar to high-risk customer or event segments.

- **Mine cluster counts (8-connected components)**  
  - Identifies clusters of adjacent mines using a breadth-first search on 8-connected neighbors.[file:1]  
  - Counts the number of clusters per board, which shows whether risk is concentrated in a few large groups or spread across many small groups (paralleling clustering analysis in business analytics).

- **3×3 neighborhood mine heatmap**  
  - For every cell position, computes the total number of mines in its 3×3 neighborhood across all boards and averages it over `numboards`.[file:1]  
  - Produces a spatial heatmap of mine density that is conceptually similar to geographic or store-layout heatmaps used in business intelligence.

### 3. Visual Outputs

The analytics module saves four `.png` charts for each configuration:

- **Histogram of empty (0) cells per board**  
  - Shows the distribution of the number of zero-value cells across all simulated boards.[file:1]  
  - Highlights variability in board openness, which can be tied to variability in scenario difficulty.

- **Bar chart of average cell counts (0–8)**  
  - Displays the average number of cells with each value (0–8) per board.[file:1]  
  - Explains how the configuration’s mine density affects the frequency of different local risk levels.

- **Histogram of mine cluster counts**  
  - Plots how often boards have a given number of mine clusters.[file:1]  
  - Characterizes whether mines tend to form a few large clusters or many small ones, which is analogous to event clustering.

- **Heatmap of average 3×3 neighborhood mine counts**  
  - Uses a 2D color-coded grid (Viridis colormap) to show the average number of mines around each cell position.[file:1]  
  - Demonstrates spatial aggregation and visualization skills that are directly transferable to real-world business analytics tasks.

### Analytics Skills Demonstrated

- Experimental configuration (rows, cols, mines, number of simulations).  
- Data aggregation and feature engineering (zero counts, cluster counts, neighborhood features).  
- Distribution analysis and interpretation (histograms and averages).  
- Visualization and storytelling using Matplotlib (histograms, bar charts, heatmaps).  

These aspects make the project suitable to showcase capabilities for business analytics and data-driven decision-making roles.

## How to Run

### Requirements

- Python 3.x  
- Packages:
  - `numpy`  
  - `matplotlib`

Install dependencies:

```bash
pip install numpy matplotlib

Play Mode
Run:

bash
python main.py
Then:

Choose 1 – Play Game.[file:5]

Select:

Preset difficulty:

0 = Easy (e.g., 9×9, 10 mines)

1 = Normal (e.g., 16×16, 40 mines)

2 = Expert (e.g., 30×16, 99 mines)[file:5]

Or choose custom configuration and enter rows, cols, and mine count.[file:5]

Use:

r row col to reveal a cell.

f row col to flag/unflag a cell.[file:5]

If you win, your completion time is measured, and qualifying times are stored in a JSON-backed high score table for that specific configuration.[file:3][file:5]

Analytics Mode
From the same script:

Run:

bash
python main.py
Choose 2 – Analytics Mode.[file:5]

Either:

Use a preset difficulty (Easy / Normal / Expert), or

Enter custom rows, cols, mines and numboards (number of random boards to simulate).[file:5]

The script:

Generates numboards boards, computes metrics, and aggregates the results using NumPy.[file:1][file:4]

Saves four plot files:

emptycellshist<rows>x<cols>x<nBombs>.png

numbercellsdist<rows>x<cols>x<nBombs>.png

mineclustershist<rows>x<cols>x<nBombs>.png

mineneighbourhoodheatmap<rows>x<cols>x<nBombs>.png[file:1]