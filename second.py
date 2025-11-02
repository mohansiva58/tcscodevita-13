import collections
import sys

def solve_ladder_problem():
    # Read M and N from the first line of standard input
    try:
        # Increase recursion limit for potential deep calls, though BFS limits depth
        sys.setrecursionlimit(2000) 
        
        # Read M and N
        line = sys.stdin.readline().strip()
        if not line:
            # Handle empty input gracefully
            return "Impossible"
        
        M, N = map(int, line.split())
        
        # Read the grid
        grid = []
        for _ in range(M):
            grid.append(sys.stdin.readline().strip().split())
            
    except Exception:
        # Handle formatting errors or EOF
        return "Impossible"


    # --- 1. Preprocessing: Find start, end, and ladder length ---
    
    start_coords = []
    end_coords = []
    
    for r in range(M):
        for c in range(N):
            if grid[r][c] == 'l':
                start_coords.append((r, c))
            elif grid[r][c] == 'L':
                end_coords.append((r, c))

    if not start_coords or not end_coords:
        return "Impossible"

    L = len(start_coords) # Ladder length (2 <= L <= 6)
    
    # Determine initial state (r, c, orientation)
    # The start (r, c) is always the top-left-most cell.
    start_r, start_c = min(r for r, c in start_coords), min(c for r, c in start_coords)
    
    # Orientation: 0 for Horizontal, 1 for Vertical
    if L > 1 and start_coords[0][0] == start_coords[1][0]:
        start_orientation = 0 # Horizontal (same row)
    else:
        start_orientation = 1 # Vertical (same column)
        
    start_state = (start_r, start_c, start_orientation)
    
    
    # --- 2. Helper Functions for Checks ---

    def is_valid_cell(r, c):
        """Checks if a single cell is within bounds and not a Block ('B')."""
        return 0 <= r < M and 0 <= c < N and grid[r][c] != 'B'

    def is_valid_position(r, c, orientation, length):
        """Checks if the entire ladder position is valid."""
        if orientation == 0:  # Horizontal (occupies (r, c) to (r, c + L - 1))
            if c + length > N: return False
            for col in range(c, c + length):
                if not is_valid_cell(r, col):
                    return False
        else:  # Vertical (occupies (r, c) to (r + L - 1, c))
            if r + length > M: return False
            for row in range(r, r + length):
                if not is_valid_cell(row, c):
                    return False
        return True

    def is_rotatable(r, c, length):
        """
        Checks if the L x L square area required for rotation is clear.
        The L x L square starts at (r, c).
        """
        if r + length > M or c + length > N:
            return False # Square extends beyond bounds
            
        for row in range(r, r + length):
            for col in range(c, c + length):
                if not is_valid_cell(row, col):
                    return False
        return True

    def is_goal_state(r, c, orientation, length):
        """Checks if the current position matches the destination ('L') configuration."""
        
        # The goal state must occupy exactly the destination cells.
        current_occupied_cells = set()
        
        if orientation == 0:
            for col in range(c, c + length):
                current_occupied_cells.add((r, col))
        else:
            for row in range(r, r + length):
                current_occupied_cells.add((row, c))

        # Check if the set of occupied cells is exactly the set of 'L' cells
        return current_occupied_cells == set(end_coords)


    # --- 3. BFS Implementation ---

    queue = collections.deque([(start_state, 0)]) # (state, steps)
    visited = {start_state} # Store only the (r, c, orientation) tuple

    # Directions: (dr, dc) for Up, Down, Left, Right
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)] 

    while queue:
        (r, c, o), steps = queue.popleft()

        # Check for goal state
        if is_goal_state(r, c, o, L):
            return steps

        # A. Attempt Movement (4 directions)
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            new_state = (nr, nc, o)
            
            if new_state not in visited and is_valid_position(nr, nc, o, L):
                visited.add(new_state)
                queue.append((new_state, steps + 1))

        # B. Attempt Rotation
        
        # Rotation is only possible if the L x L square starting at (r, c) is clear.
        if is_rotatable(r, c, L):
            # Calculate new orientation and state
            new_o = 1 - o # Flip orientation
            new_state = (r, c, new_o)
            
            # The rotation is only valid if the new position itself is valid
            # (Which is implicitly true if the L x L box check passed, 
            # but we keep the explicit check for robustness, although it's redundant here 
            # as the rotation check is stronger than the simple position check)
            if new_state not in visited:
                visited.add(new_state)
                queue.append((new_state, steps + 1))

    # If the queue empties without reaching the goal
    return "Impossible"

if __name__ == '__main__':
    result = solve_ladder_problem()
    print(result)
