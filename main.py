import math


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

    def update_possibilities(self):
        if self.value is not None:
            return
        initial_possibilities = len(self.possibilities)
        self.possibilities -= self.grid.get_row_values(
            self.y, exclude=self)
        self.possibilities -= self.grid.get_col_values(
            self.x, exclude=self)
        self.possibilities -= self.grid.get_grp_values(
            self.group_num, exclude=self)
        if len(self.possibilities) == 0:
            raise BustedSudokuException("Square with 0 possibilities")
        if len(self.possibilities) == 1:
            self.value = list(self.possibilities)[0]
        self.grid.validate()
        return len(self.possibilities) < initial_possibilities


class SudokuGrid:
    def __init__(self, values):
        self.cells = []
        self.groups = []
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
                if cell.value is None:
                    print('_', end='')
                else:
                    print(cell.value, end='')
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
        return SudokuGrid(values)

    def get_col_values(self, x, exclude=None):
        vals = set([])
        for row in self.cells:
            target_cell = row[x]
            if exclude is not None and target_cell == exclude:
                continue
            if target_cell.value:
                vals.add(target_cell.value)
        return vals

    def get_grp_values(self, group_num, exclude=None):
        vals = set([])
        for cell in self.groups[group_num]:
            if exclude is not None and cell == exclude:
                continue
            if cell.value:
                vals.add(cell.value)
        return vals

    def get_row_values(self, y, exclude=None):
        vals = set([])
        for cell in self.cells[y]:
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

    def validate(self):
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

    def solve(self):
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
            if not changed:
                break
        print("Iterations to maximally simplify: {0}".format(i))


class EliminationBackTrackSolver(SimpleEliminationSolver):
    def __init__(self, grid, depth=0):
        self.grid = grid
        self.depth = depth

    def solve(self):
        super().solve()
        if self.grid.is_solved() or self.depth >= 2:
            return
        # Get the cell with the fewest possibilities and guess.
        for _ in range(10):
            # self.grid.display()
            guess_cell = None
            for i in range(2, 6):
                for row in self.grid.cells:
                    for guess_cell in row:
                        if len(guess_cell.possibilities) == i:
                            guess = list(guess_cell.possibilities)[0]
                            duplicate_grid = self.grid.duplicate()
                            new_target_cell = duplicate_grid.cells[
                                guess_cell.y][guess_cell.x]
                            new_target_cell.value = guess
                            new_target_cell.possibilities = {guess}
                            new_solver = EliminationBackTrackSolver(
                                duplicate_grid, self.depth + 1)
                            try:
                                duplicate_grid.validate()
                                new_solver.solve()
                            except BustedSudokuException as e:
                                print(e)
                                # We know that's not a valid guess, then.
                                guess_cell.possibilities.remove(guess)
                            else:
                                if new_solver.grid.is_solved():
                                    self.grid = new_solver.grid
                                    return
