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
        self.impossibles = []
        self.possibles = []

        if self.value == 0:
            for slot in grid:
                if slot.row == self.row and slot.value != 0:
                    row_imposs.append(slot.value)
                if slot.col == self.col and slot.value != 0:
                    col_imposs.append(slot.value)
                if slot.cell == self.cell and slot.value != 0:
                    cell_imposs.append(slot.value)
            self.impossibles.extend(row_imposs)
            self.impossibles.extend(col_imposs)
            self.impossibles.extend(cell_imposs)
            self.impossibles = set(self.impossibles)
            for i in range(1,10):
                if i not in self.impossibles:
                    self.possibles.append(i)


class Sudoku:

    def make_row(self, input, row_num):
        row = []
        for i in range(len(input)):
            row.append(Slot(input[i], (row_num, i)))
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

        if all(slot.value != 0 for slot in flat_grid):
            self.filled = True
        else:
            self.filled = False
            return False

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

    def simple_solve(self):
        flat_grid = self.grid.flatten()

        modified = False

        for slot in flat_grid:
            slot.update_possibles(flat_grid)
            if len(slot.possibles) == 1:
                slot.value = slot.possibles[0]
                modified = True

        return modified

    def solve_sudoku(self):
        print('Attempting simple solve...')
        while not self.solved:
            modified = self.simple_solve()
            self.verify_grid()
            if not modified:
                break
            else:
                print('Algorithm loop...')
        if self.solved:
            print('Sudoku solved.')
        elif self.filled:
            print('Unrecoverable (misfilled)')
            sys.exit(0)
        else:
            print('Unsolvable by simple solve.')


if __name__ == '__main__':
    sud = Sudoku(sys.argv[1])
    print(sud)
    sud.solve_sudoku()
    print(sud)
