import sys
import numpy as np
import math

class Slot:
    def __init__(self, value, index):
        self.value = int(value)
        self.index = index
        self.row = index[0]
        self.col = index[1]
        self.cell = (math.floor(index[0]/3), math.floor(index[1]/3))

    def __repr__(self):
        return str(self.value)

    def update_possibles(self, grid):
        row_imposs = []
        col_imposs = []
        cell_imposs = []
        impossibles = []
        self.possibles = []

        if self.value == 0:
            for slot in grid:
                if slot.row == self.row & slot.value != 0:
                    row_imposs.append(slot.value)
                if slot.col == self.col & slot.value != 0:
                    col_imposs.append(slot.value)
                if slot.cell == self.cell and slot.value != 0:
                    cell_imposs.append(slot.value)
            impossibles.extend(row_imposs)
            impossibles.extend(col_imposs)
            impossibles.extend(cell_imposs)
            impossibles = set(impossibles)
            for i in range(1,10):
                if i not in impossibles:
                    self.possibles.append(i)


class Sudoku:

    def make_row(self, input, row_num):
        row = []
        for i in range(len(input)):
            row.append(Slot(input[i], (i,row_num)))
        return row

    def __repr__(self):
        return '\n' + self.pretty_grid() +\
                f'\n\nCorrect: {self.solved}, Filled: {self.filled}'

    def __init__(self, file):
        puzzle = []
        with open(file) as f:
            i = 0
            for line in f:
                puzzle_row = list(line.replace('X', '0').strip())
                puzzle.append(self.make_row(puzzle_row, i))
                i += 1
        self.grid = np.array(puzzle)

        self.regions = []
        self.letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        self.regions.append(self.grid[0:3, 0:3])
        self.regions.append(self.grid[0:3, 3:6])
        self.regions.append(self.grid[0:3, 6:9])
        self.regions.append(self.grid[3:6, 0:3])
        self.regions.append(self.grid[3:6, 3:6])
        self.regions.append(self.grid[3:6, 6:9])
        self.regions.append(self.grid[6:9, 0:3])
        self.regions.append(self.grid[6:9, 3:6])
        self.regions.append(self.grid[6:9, 6:9])
        self.cells = []
        for i in range(3):
            for j in range(3):
                self.cells.append((i,j))
        self.rows = [self.grid[x,:] for x in range(9)]
        self.cols = [self.grid[:,x] for x in range(9)]

        self.solved = self.verify_grid()

    def pretty_grid(self):
        pretty_grid = []
        for i in range(0, 9):
            pretty_grid_row = [str(x).replace('0', 'X') for x in self.grid[i].tolist()]
            pretty_grid_row.insert(6, '|')
            pretty_grid_row.insert(3, '|')
            pretty_grid_row = ' '.join(pretty_grid_row)
            pretty_grid.append(pretty_grid_row)

            if i == 2 or i == 5:
                pretty_grid.append('------+-------+-------')

        pretty_grid = '\n'.join(pretty_grid)
        return pretty_grid

    def verify_grid(self):
        flat_grid = self.grid.flatten()

        if not all(value != 0 for value in flat_grid):
            self.filled = False
            return False
        else:
            self.filled = True

        sums = []
        for i in range(9):
            row_sum = 0
            col_sum = 0
            cell_sum = 0

            for slot in flat_grid:
                if slot.row == i:
                    row_sum += slot.value
                if slot.col == i:
                    col_sum += slot.value
                if slot.cell == self.cells[i]:
                    cell_sum += slot.value
            sums.extend([row_sum, col_sum, cell_sum])
        if all(sum == 45 for sum in sums):
            self.solved = True
        else:
            self.solved = False

        return self.solved

    def new_simple_solve(self):
        flat_grid = self.grid.flatten()

        modified = False

        for slot in flat_grid:
            slot.update_possibles(flat_grid)
            if len(slot.possibles) == 1:
                slot.value = slot.possibles[0]
                modified = True

        if self.verify_grid():
            return True
        elif modified:
            self.new_simple_solve()
        else:
            return False





    def simple_missing_solve(self):

        any_mods = False
        for i in range(0,9):
            missing = find_missing(self.rows[i])
            if len(missing) == 1:
                np.place(self.rows[i], self.rows[i] == 0, missing[0])
                any_mods = True
            elif len(missing) > 1:
                print(f'Row {i+1} too complex')

            missing = find_missing(self.cols[i])
            if len(missing) == 1:
                np.place(self.cols[i], self.cols[i] == 0, missing[0])
                any_mods = True
            elif len(missing) > 1:
                print(f'Column {i+1} too complex')

            missing = find_missing(self.regions[i])
            if len(missing) == 1:
                np.place(self.regions[i], self.regions[i] == 0, missing[0])
                any_mods = True
            elif len(missing) > 1:
                print(f'Region {self.letters[i]} too complex')

        if self.verify_grid():
            return True
        elif any_mods:
            print('Modifications made, repeating simple solve')
            self.simple_missing_solve()
        else:
            return any_mods


if __name__ == '__main__':
    sud = Sudoku(sys.argv[1])
    sud.new_simple_solve()
    print(sud)
