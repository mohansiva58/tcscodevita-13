import sys

# Increase recursion limit for safety, although not strictly needed for this iterative solution
sys.setrecursionlimit(2000)

class FoldedSheetSolver:
    
    def __init__(self, R, C, instructions):
        self.initial_R = R
        self.initial_C = C
        self.R = R
        self.C = C
        self.instructions = instructions
        # Sheet[r][c] holds a list of original cell numbers, from top (index 0) to bottom (last index)
        self.sheet = self._initialize_sheet()

    def _initialize_sheet(self):
        """Initializes the sheet with original cell numbers (1 to R*C)."""
        sheet = []
        for r in range(self.R):
            row = []
            for c in range(self.C):
                original_cell_number = self.initial_C * r + c + 1
                row.append([original_cell_number])
            sheet.append(row)
        return sheet

    def _fold_horizontal(self, k: int):
        """
        Folds the sheet horizontally along line h_k (between current row k and k+1).
        Bottom section moves over the Top section.
        k is 1-indexed.
        """
        r1 = k  # Number of rows in the top section (base)
        r2 = self.R - k  # Number of rows in the bottom section (folded part)
        
        # Determine the resulting number of rows
        new_R = max(r1, r2)
        new_sheet = [[[] for _ in range(self.C)] for _ in range(new_R)]
        
        # Case 1: Top section (r1) is the larger/equal base
        if r1 >= r2:
            # Copy top section (rows 0 to r1-1) to be the base (rows 0 to r1-1)
            for r in range(r1):
                for c in range(self.C):
                    new_sheet[r][c].extend(self.sheet[r][c])

            # Fold bottom section (rows R-1 down to R-r2) onto the base
            for r_fold in range(self.R - 1, self.R - r2 - 1, -1):
                # r_base is the row index in the new sheet where r_fold stacks
                # r_base decreases from r1 - 1
                r_base = r1 - 1 - (self.R - 1 - r_fold) 
                
                if r_base >= 0:
                    for c in range(self.C):
                        # Cells from the folded (bottom) section must be vertically mirrored
                        # by reversing their stack order, and then placed ON TOP of the base stack.
                        folded_stack = self.sheet[r_fold][c][::-1]
                        new_stack = folded_stack + new_sheet[r_base][c]
                        new_sheet[r_base][c] = new_stack

        # Case 2: Bottom section (r2) is the larger base
        else: # r2 > r1
            # Copy bottom section (rows r1 to R-1) to be the base (rows 0 to r2-1)
            for r in range(r2):
                for c in range(self.C):
                    new_sheet[r][c].extend(self.sheet[r1 + r][c])

            # Fold top section (rows r1-1 down to 0) onto the base
            for r_fold in range(r1 - 1, -1, -1):
                # r_base is the row index in the new sheet where r_fold stacks
                # r_base decreases from r2 - 1
                r_base = r2 - 1 - (r1 - 1 - r_fold) 

                if r_base < new_R:
                    for c in range(self.C):
                        # Cells from the folded (top) section must be vertically mirrored
                        # by reversing their stack order, and then placed ON TOP of the base stack.
                        folded_stack = self.sheet[r_fold][c][::-1]
                        new_stack = folded_stack + new_sheet[r_base][c]
                        new_sheet[r_base][c] = new_stack
        
        self.R = new_R
        self.sheet = new_sheet

    def _fold_vertical(self, k: int):
        """
        Folds the sheet vertically along line v_k (between current column k and k+1).
        Right section moves over the Left section.
        k is 1-indexed.
        """
        c1 = k  # Number of columns in the left section (base)
        c2 = self.C - k  # Number of columns in the right section (folded part)
        
        # Determine the resulting number of columns
        new_C = max(c1, c2)
        new_sheet = [[[] for _ in range(new_C)] for _ in range(self.R)]

        # Case 1: Left section (c1) is the larger/equal base
        if c1 >= c2:
            # Copy left section (cols 0 to c1-1) to be the base (cols 0 to c1-1)
            for r in range(self.R):
                for c in range(c1):
                    new_sheet[r][c].extend(self.sheet[r][c])

            # Fold right section (cols C-1 down to C-c2) onto the base
            for c_fold in range(self.C - 1, self.C - c2 - 1, -1):
                # c_base is the column index in the new sheet where c_fold stacks
                # c_base decreases from c1 - 1
                c_base = c1 - 1 - (self.C - 1 - c_fold)
                
                if c_base >= 0:
                    for r in range(self.R):
                        # Cells from the folded (right) section must be horizontally mirrored
                        # by reversing their stack order, and then placed ON TOP of the base stack.
                        folded_stack = self.sheet[r][c_fold][::-1]
                        new_stack = folded_stack + new_sheet[r][c_base]
                        new_sheet[r][c_base] = new_stack

        # Case 2: Right section (c2) is the larger base
        else: # c2 > c1
            # Copy right section (cols c1 to C-1) to be the base (cols 0 to c2-1)
            for r in range(self.R):
                for c in range(c2):
                    new_sheet[r][c].extend(self.sheet[r][c1 + c])

            # Fold left section (cols c1-1 down to 0) onto the base
            for c_fold in range(c1 - 1, -1, -1):
                # c_base is the column index in the new sheet where c_fold stacks
                # c_base decreases from c2 - 1
                c_base = c2 - 1 - (c1 - 1 - c_fold)

                if c_base < new_C:
                    for r in range(self.R):
                        # Cells from the folded (left) section must be horizontally mirrored
                        # by reversing their stack order, and then placed ON TOP of the base stack.
                        folded_stack = self.sheet[r][c_fold][::-1]
                        new_stack = folded_stack + new_sheet[r][c_base]
                        new_sheet[r][c_base] = new_stack

        self.C = new_C
        self.sheet = new_sheet


    def solve(self) -> str:
        """Applies all folding instructions sequentially and returns the top and bottom cell."""
        
        for instruction in self.instructions:
            try:
                type = instruction[0]
                k = int(instruction[1:])
            except (ValueError, IndexError):
                # Should not happen based on constraints, but handles malformed instruction
                continue 
                
            if type == 'h':
                if 1 <= k < self.R:
                    self._fold_horizontal(k)
            elif type == 'v':
                if 1 <= k < self.C:
                    self._fold_vertical(k)
        
        # After all folds, the sheet must be 1x1.
        if self.R == 1 and self.C == 1 and self.sheet[0][0]:
            top_cell = self.sheet[0][0][0]
            bottom_cell = self.sheet[0][0][-1]
            return f"{top_cell} {bottom_cell}"
        else:
            # Should not happen in a valid test case that completely folds the sheet
            return "Error: Final sheet not 1x1 or empty."

def run_solver():
    """Reads input from stdin and calls the solver."""
    try:
        # Read R and C
        line1 = sys.stdin.readline().strip()
        if not line1: return "Error: Missing R C input."
        R, C = map(int, line1.split())
        
        # Read instructions
        line2 = sys.stdin.readline().strip()
        if not line2: return "Error: Missing instructions."
        instructions = line2.split()
        
    except Exception as e:
        return f"Error reading input: {e}"

    solver = FoldedSheetSolver(R, C, instructions)
    return solver.solve()

# Execute the solver logic
if __name__ == "__main__":
    result = run_solver()
    print(result)