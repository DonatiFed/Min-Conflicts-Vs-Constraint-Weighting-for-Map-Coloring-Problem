# Map Coloring with Heuristic Local Search: Min-Conflicts vs. Constraint Weighting

## Project Overview

This repository provides the Python implementation for a comparative study of two prominent heuristic algorithms for solving Constraint Satisfaction Problems (CSPs): the **Min-Conflicts algorithm** and the **Constraint Weighting algorithm**. The focus of this implementation is on the classic **Map Coloring Problem**, where the goal is to assign colors to regions such that no adjacent regions share the same color.

This README focuses on the technical implementation details, including how the map is generated, the algorithms are executed, and how visualization is performed. For a comprehensive theoretical analysis, detailed experimental results, performance graphs, and conclusions, please refer to the accompanying PDF report: `Artificial_Intelligence_Project.pdf`.

## The Map Coloring Problem

The Map Coloring Problem is modeled as a connected graph where nodes represent regions and edges denote shared borders. Each region must be assigned one of three possible colors such that no adjacent regions share the same color.

## Implementation Highlights

This project includes the following key Python components:

### 1. Map Generation (`RandomMapGeneration.py`)

This module is responsible for dynamically generating the map's graph structure based on a given number of regions ($n$) and the maximum number of colors allowed.

* **`generate_map_coloring_problem(n, max_colors)`:** The main function for map generation. It creates random 2D points for regions and constructs connections (edges) using a modified Kruskal's algorithm. It ensures the graph is connected, adheres to a maximum degree for each node, and prevents intersecting edges for a realistic map layout.

* **`lines_intersect`:** A helper function to check for intersections between line segments, crucial for generating non-overlapping map borders.

* **`verify_connectivity`:** Verifies that all regions in the generated map are connected, forming a single component.

* **`verify_degrees`:** Ensures that no region exceeds the specified maximum degree (number of adjacent regions).

* **`plot_map_coloring_problem`:** Visualizes the generated map structure (points and connections) before any coloring algorithm is applied.

### 2. Algorithm Implementations

Both heuristic algorithms are implemented from scratch. Each algorithm has a dedicated script for single-run visualization and another for systematic performance testing.

#### Min-Conflicts Algorithm

* **`MinConflictMapColor.py`:**

    * **`MinConflicts(csp, max_steps, colours)`:** The core algorithm for a single run. It starts with a random initial coloring and iteratively selects a conflicting region, reassigning its color to minimize conflicts with neighbors. It includes calls to `plot_solution` for real-time visualization.

    * **`plot_solution(...)`:** Provides dynamic, step-by-step visualization of the map coloring process, highlighting conflicting edges in red.

    * **`IndextoChange(extended_points)`:** Selects a random region that is currently in conflict.

    * **`CheckSolution(connections, solution, extended_points)`:** Evaluates the current solution, identifies conflicting regions, and updates conflict status and neighbor color counts.

    * **`RandomSolution(n, coloursNumbers)`:** Generates an initial random color assignment for all regions.

* **`MinConflictTest.py`:**

    * **`MinConflicts(csp, max_steps, colours)`:** A version of the algorithm optimized for testing, without real-time visualization.

    * **`test_performance(max_n, step, max_steps)`:** Deals with multiple runs of the `MinConflicts` algorithm for varying problem sizes (`n`), measuring and plotting the execution time and final conflict counts.

    * Includes the same helper functions (`IndextoChange`, `CheckSolution`, `RandomSolution`) as `MinConflictMapColor.py`.

#### Constraint Weighting Algorithm

* **`ConstraintWeightingMapColor.py`:**

    * **`ConstraintWeighting(csp, max_steps, colours)`:** The main algorithm for a single run. It starts with a random coloring, assigns weights to constraints (edges), and iteratively adjusts colors to minimize the sum of weights of conflicting edges. It includes calls to `plot_solution` for real-time visualization.

    * **`plot_solution(...)`:** Provides dynamic, step-by-step visualization of the map coloring process, highlighting conflicting edges based on their weights.

    * **`NewColour(extended_connections, point, solution, coloursNumbers)`:** Determines the optimal new color for a selected region to minimize conflicts based on current constraint weights.

    * **`CheckSolution(extended_connections, solution)`:** Evaluates the current solution, updates the `is_in_conflict` status and `weight` of each connection, and returns the total sum of weights of conflicting edges.

    * **`RandomSolution(n, coloursNumbers)`:** Generates an initial random color assignment for all regions.

* **`ConstraintWeightingTest.py`:**

    * **`ConstraintWeighting(csp, max_steps, colours)`:** A version of the algorithm optimized for testing, without real-time visualization.

    * **`test_performance(max_n, step, max_steps)`:** Systematically runs the `ConstraintWeighting` algorithm for various problem sizes (`n`), collecting and plotting execution time and final conflict data.

    * Includes the same helper functions (`NewColour`, `CheckSolution`, `RandomSolution`) as `ConstraintWeightingMapColor.py`.

## Getting Started

To run the implementations and reproduce the experiments:

1.  **Clone the Repository:**

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Install Dependencies:**
    This project primarily uses `matplotlib` for plotting.

    ```bash
    pip install matplotlib
    ```

3.  **Run the Algorithms with Visualization:**
    To see a single execution of an algorithm with step-by-step visualization (e.g., for `n=500` and `max_steps=50` as configured in the `if __name__ == "__main__":` blocks):

    ```bash
    python MinConflictMapColor.py
    python ConstraintWeightingMapColor.py
    ```

    *(You can modify the `n` and `max_steps` variables directly within these files to adjust the problem size and iteration limit for individual runs.)*

4.  **Run Performance Tests:**
    To execute the performance tests and generate the summary graphs (e.g., for `max_n=1000`, `step=50` for Min-Conflicts, and `step=100` for Constraint Weighting, with `max_steps=100`):

    ```bash
    python MinConflictTest.py
    python ConstraintWeightingTest.py
    ```

    *(These scripts will print results to the console and display a final performance graph. You can adjust the parameters within their `if __name__ == "__main__":` blocks.)*

## Detailed Analysis and Results

For an in-depth understanding of the theoretical background, comprehensive experimental results, detailed performance tables, and a discussion of the conclusions drawn from this comparative study, please refer to the full report:

[Artificial_Intelligence_Project.pdf](Artificial_Intelligence_Project.pdf)

## Author

Federico Donati
