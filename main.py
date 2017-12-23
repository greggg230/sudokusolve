import math

from itertools import combinations
from functools import reduce


ez_puzzle = [
    [9, 1, 5, None, None, 6, None, None, None],
    [None, None, 3, None, None, 1, None, None, 5],
    [2, None, None, None, 5, 3, 7, None, 6],
    [None, 6, None, 5, None, None, 4, None, 2],
    [None, None, None, 4, 8, 2, None, None, None],
    [4, None, 1, None, None, 7, None, 8, None],
    [8, None, 7, 2, 9, None, None, None, 1],
    [5, None, None, 1, None, None, 9, None, None],
    [None, None, None, 6, None, None, 8, 5, 7]
]

medium_puzzle = [
    [3, 8, 4, None, 1, None, 6, None, None],
    [None, None, None, None, 3, None, None, None, None],
    [9, 5, 7, None, None, None, None, None, 1],
    [None, None, None, 4, None, None, 1, 9, 6],
    [5, None, None, None, None, None, None, None, 3],
    [7, 4, 1, None, None, 6, None, None, None],
    [1, None, None, None, None, None, 2, 7, 9],
    [None, None, None, None, 7, None, None, None, None],
    [None, None, 3, None, 2, None, 5, 1, 8]
]

hard_puzzle = [
    [None, 5, None, None, 2, None, 8, None, None],
    [None, 1, 7, 8, 6, None, None, None, None],
    [4, None, None, 1, None, None, 7, None, None],
    [None, None, None, None, None, 4, None, None, 5],
    [None, 4, 9, None, None, None, 2, 7, None],
    [5, None, None, 2, None, None, None, None, None],
    [None, None, 5, None, None, 8, None, None, 3],
    [None, None, None, None, 4, 5, 9, 8, None],
    [None, None, 4, None, 9, None, None, 6, None]
]

evil_puzzle = [
    [None, None, None, None, 2, None, 1, 5, None],
    [9, None, None, 3, None, None, None, None, 8],
    [7, None, None, None, 4, None, 3, None, None],
    [None, None, None, None, None, None, 2, 7, 1],
    [5, None, None, None, None, None, None, None, 9],
    [2, 7, 1, None, None, None, None, None, None],
    [None, None, 5, None, 1, None, None, None, 7],
    [8, None, None, None, None, 5, None, None, 3],
    [None, 3, 4, None, 8, None, None, None, None]
]

puzzle_1 = [
    [None, None, 2, None, None, None, 6, None, None],
    [None, 4, None, 6, None, 3, None, 9, None],
    [5, None, None, None, 8, None, None, None, 7],
    [None, 5, None, 4, None, 1, None, 7, None],
    [None, None, 4, None, None, None, 2, None, None],
    [None, 9, None, 2, None, 8, None, 1, None],
    [4, None, None, None, 1, None, None, None, 8],
    [None, 6, None, 8, None, 4, None, 3, None],
    [None, None, 9, None, None, None, 4, None, None]
]

puzzle_2 = [
    [3, None, None, None, 6, None, None, None, 7],
    [None, None, None, 8, None, 1, None, None, None],
    [None, None, 2, None, 9, None, 5, None, None],
    [None, 1, None, None, None, None, None, 8, None],
    [8, None, 7, None, 1, None, 2, None, 6],
    [None, 3, None, None, None, None, None, 4, None],
    [None, None, 9, None, 5, None, 4, None, None],
    [None, None, None, 9, None, 2, None, None, None],
    [7, None, None, None, 8, None, None, None, 9]
]

puzzle_3 = [
    [9, None, None, None, None, None, 2, 3, None],
    [2, None, None, None, None, None, None, 1, 6],
    [1, None, None, 2, None, None, None, None, None],
    [6, None, None, None, None, 3, 1, 2, None],
    [None, None, None, 9, None, 1, None, None, None],
    [None, 1, None, 6, None, None, None, None, None],
    [None, None, None, None, None, 5, None, None, 2],
    [5, None, None, None, None, None, None, None, 1],
    [None, 6, None, None, None, None, None, None, 4]
]

hardest_puzzle = [
    [8, None, None, None, None, None, None, None, None],
    [None, None, 3, 6, None, None, None, None, None],
    [None, 7, None, None, 9, None, 2, None, None],
    [None, 5, None, None, None, 7, None, None, None],
    [None, None, None, None, 4, 5, 7, None, None],
    [None, None, None, 1, None, None, None, 3, None],
    [None, None, 1, None, None, None, None, 6, 8],
    [None, None, 8, 5, None, None, None, 1, None],
    [None, 9, None, None, None, None, 4, None, None]
]


def find_clusters(cells, min_size, max_size):
    clusters = []
    unknown_cells = filter(lambda x: len(x.possibilities) > 1, cells)
    for i in range(min_size, max_size + 1):
        for cell_set in combinations(unknown_cells, i):
            # Test if it's a cluster
            cell_values = set(
                reduce(lambda a, b: a.union(b),
                       [cell.possibilities for cell in cell_set])
            )
            if len(cell_values) == i:
                clusters.append(cell_set)
    return clusters


class BustedSudokuException(Exception):
    pass


class SudokuCell:
    def __init__(self, grid, x, y, value=None):
        self.value = value
        self.grid = grid
        self.x = x
        self.y = y
        self.group_num = (
            math.floor(float(y) / 3) * 3 + math.floor(float(x) / 3))
        if self.value is None:
            self.possibilities = set(range(1, 10))
        else:
            self.possibilities = {self.value}

    def __repr__(self):
        return "<Cell: ({0.x}, {0.y}) [{0.possibilities}]>".format(self)

    def remove_possibilities(self, to_remove, verbose=False):
        if len(self.possibilities.intersection(to_remove)) == 0:
            return
        self.possibilities -= to_remove
        if verbose:
            print("Removing {0} from {1}".format(to_remove, self))
        if len(self.possibilities) == 0:
            raise BustedSudokuException("Square with 0 possibilities")
        if len(self.possibilities) == 1:
            self.set_value(list(self.possibilities)[0], verbose=verbose)

    def set_value(self, new_value, verbose=False):
        self.value = new_value
        self.possibilities = {new_value}
        if verbose:
            print("Setting {0} to {1}".format(self, new_value))

    def update_possibilities(self):
        if self.value is not None:
            return
        initial_possibilities = len(self.possibilities)
        row_vals = self.grid.get_row_values(self.y, exclude=self)
        col_vals = self.grid.get_col_values(self.x, exclude=self)
        grp_vals = self.grid.get_grp_values(self.group_num, exclude=self)
        vals = reduce(lambda a, b: a.union(b), [row_vals, col_vals, grp_vals])
        self.remove_possibilities(vals)
        self.grid.validate()
        return len(self.possibilities) < initial_possibilities


class SudokuGrid:
    def __init__(self, values, solve_state):
        self.cells = []
        self.groups = []
        self.solve_state = solve_state
        for i in range(9):
            self.groups.append([])
        for y, row in enumerate(values):
            new_row = []
            for x, val in enumerate(row):
                new_cell = SudokuCell(self, x, y, val)
                new_row.append(new_cell)
                self.groups[new_cell.group_num].append(new_cell)
            self.cells.append(new_row)

    def display(self):
        row_count = 0
        for row in self.cells:
            if row_count % 3 == 0:
                print('-' * 13)
            col_count = 0
            for cell in row:
                if col_count % 3 == 0:
                    print("|", end='')
                if cell.value:
                    print(cell.value, end='')
                else:
                    print('_', end='')
                col_count += 1
            print("")
            row_count += 1

    def duplicate(self):
        values = []
        for y, row in enumerate(self.cells):
            new_row = []
            for x, cell in enumerate(row):
                new_row.append(cell.value)
            values.append(new_row)
        return SudokuGrid(values, self.solve_state)

    def get_col_cells(self, x):
        output = [row[x] for row in self.cells]
        return output

    def get_col_values(self, x, exclude=None):
        vals = set([])
        for cell in self.get_col_cells(x):
            if exclude is not None and cell == exclude:
                continue
            if cell.value:
                vals.add(cell.value)
        return vals

    def get_hash(self):
        toutput = []
        for row in self.cells:
            toutput.append(tuple([f.value for f in row]))
        return tuple(toutput).__hash__()

    def get_grp_cells(self, group_num):
        return self.groups[group_num]

    def get_grp_values(self, group_num, exclude=None):
        vals = set([])
        for cell in self.get_grp_cells(group_num):
            if exclude is not None and cell == exclude:
                continue
            if cell.value:
                vals.add(cell.value)
        return vals

    def get_row_cells(self, y):
        return self.cells[y]

    def get_row_values(self, y, exclude=None):
        vals = set([])
        for cell in self.get_row_cells(y):
            if exclude is not None and cell == exclude:
                continue
            if cell.value:
                vals.add(cell.value)
        return vals

    def is_solved(self):
        for row in self.cells:
            if not all(map(lambda x: x.value is not None, row)):
                return False
        return True

    def simplify(self, verbose=False):
        # Look for clusters among cols, rows, and groups
        handlers = (self.get_row_cells, self.get_grp_cells, self.get_col_cells)
        for handler in handlers:
            for v in range(9):
                clusters = find_clusters(handler(v), 2, 5)
                for cluster in clusters:
                    cluster_values = set(
                        reduce(lambda a, b: a.union(b),
                               [c.possibilities for c in cluster])
                    )
                    for cell in handler(v):
                        if cell not in cluster:
                            cell.remove_possibilities(
                                cluster_values, verbose=verbose)

    def validate(self):
        if self.get_hash() in self.solve_state.dead_hashes:
            raise BustedSudokuException("Found cached dead hash.")
        # Validate rows
        for row in self.cells:
            found_possibilities = set([])
            for cell in row:
                found_possibilities.update(cell.possibilities)
            if len(found_possibilities) != 9:
                raise BustedSudokuException("Missing possibility in row")
        # Validate columns.
        for i in range(9):
            found_possibilities = set([])
            for row in self.cells:
                found_possibilities.update(row[i].possibilities)
            if len(found_possibilities) != 9:
                raise BustedSudokuException("Missing possibility in col")
        # Validate groups
        for i in range(9):
            found_possibilities = set([])
            for cell in self.groups[i]:
                found_possibilities.update(cell.possibilities)
            if len(found_possibilities) != 9:
                raise BustedSudokuException("Missing possibility in grp")


class SimpleEliminationSolver:
    def __init__(self, grid):
        self.grid = grid

    def solve(self, verbose=False):
        for i in range(100):
            # Iterate through every cell and eliminate obvious
            # impossibilities
            changed = False
            for y, row in enumerate(self.grid.cells):
                for x, cell in enumerate(row):
                    # Skip solved squares
                    if cell.value is not None:
                        continue
                    if cell.update_possibilities():
                        changed = True
                    if self.grid.is_solved():
                        return
            self.grid.simplify(verbose=verbose)
            if not changed:
                break


class SolveState:
    def __init__(self):
        self.dead_hashes = set([])

    def add_hash(self, new_hash):
        self.dead_hashes.add(new_hash)


class EliminationBackTrackSolver(SimpleEliminationSolver):
    def __init__(self, grid, solve_state, max_depth=5, depth=0):
        self.grid = grid
        self.solve_state = solve_state
        self.depth = depth
        self.max_depth = max_depth

    def solve(self, verbose=False):
        super().solve()
        if self.grid.is_solved() or self.depth >= self.max_depth:
            return
        # Get the cell with the fewest possibilities and guess.
        for d in range(1, self.max_depth + 1):
            if self.depth == 0:
                print("Using depth: {0}".format(d))
            for i in range(2, 10):
                for row in self.grid.cells:
                    for guess_cell in row:
                        if len(guess_cell.possibilities) == i:
                            found = False
                            for guess in guess_cell.possibilities:
                                duplicate_grid = self.grid.duplicate()
                                new_target_cell = duplicate_grid.cells[
                                    guess_cell.y][guess_cell.x]
                                new_target_cell.value = guess
                                new_target_cell.possibilities = {guess}
                                if self.is_valid_grid(duplicate_grid):
                                    found = True
                                    break
                            if not found:
                                continue
                            new_solver = EliminationBackTrackSolver(
                                duplicate_grid,
                                self.solve_state,
                                max_depth=d,
                                depth=self.depth + 1)
                            try:
                                duplicate_grid.validate()
                                new_solver.solve(verbose=False)
                            except BustedSudokuException:
                                # We know that's not a valid guess, then.
                                self.solve_state.add_hash(
                                    duplicate_grid.get_hash())
                                guess_cell.remove_possibilities(
                                    {guess}, verbose=verbose)
                                return self.solve(verbose=verbose)
                            else:
                                if new_solver.grid.is_solved():
                                    print("Found solved grid!")
                                    self.grid = new_solver.grid
                                    return

    def is_valid_grid(self, grid):
        return grid.get_hash() not in self.solve_state.dead_hashes
