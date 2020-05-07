import numpy as np
import sys


class Sudoku:

    def __init__(self, file):
        puzzle = []
        with open(file) as f:
            for line in f:
                puzzle_row = line.replace('X', '0').split()
                puzzle.append(puzzle_row)
        self.grid = np.array(puzzle).astype(np.int)

        self.regions = []
        self.regions.append(self.grid[0:3, 0:3])
        self.regions.append(self.grid[0:3, 3:6])
        self.regions.append(self.grid[0:3, 6:9])
        self.regions.append(self.grid[3:6, 0:3])
        self.regions.append(self.grid[3:6, 3:6])
        self.regions.append(self.grid[3:6, 6:9])
        self.regions.append(self.grid[6:9, 0:3])
        self.regions.append(self.grid[6:9, 3:6])
        self.regions.append(self.grid[6:9, 6:9])

        self.verify_grid()

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

    def __repr__(self):
        return '\n' + self.pretty_grid() +\
                f'\n\nFilled: {self.filled}, Correct: {self.verify_grid()}'

    def verify_grid(self):
        if 0 in self.grid:
            return False
            self.filled = False
        else:
            self.filled = True

        sums = self.grid.sum(axis = 0).tolist()
        sums.extend(self.grid.sum(axis = 1).tolist())
        sums.extend([np.sum(x) for x in self.regions])
        if not all(x == 45 for x in sums):
            return False
        else:
            return True


if __name__ == '__main__':
    sud = Sudoku(sys.argv[1])
    print(sud)
