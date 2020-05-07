import numpy as np
import sys

def find_missing(input):
    missing_no = []
    for i in range(1,10):
        if i not in input:
            missing_no.append(i)
    return missing_no

class Sudoku:

    def __init__(self, file):
        puzzle = []
        with open(file) as f:
            for line in f:
                puzzle_row = line.replace('X', '0').split()
                puzzle.append(puzzle_row)
        self.grid = np.array(puzzle).astype(np.int)

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
        self.rows = [self.grid[x,:] for x in range(9)]
        self.cols = [self.grid[:,x] for x in range(9)]

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
                f'\n\nCorrect: {self.verify_grid()}, Filled: {self.filled}'

    def verify_grid(self):
        if 0 in self.grid:
            self.filled = False
            return False
        else:
            self.filled = True

        sums = self.grid.sum(axis = 0).tolist()
        sums.extend(self.grid.sum(axis = 1).tolist())
        sums.extend([np.sum(x) for x in self.regions])
        if not all(x == 45 for x in sums):
            return False
        else:
            return True

    def simple_missing_solve(self):

        any_mods = False
        for i in range(0,9):
            missing = find_missing(self.rows[i])
            if len(missing) == 1:
                np.place(self.rows[i], self.rows[i] == 0, missing[0])
            elif len(missing) > 1:
                print(f'Row {i+1} too complex')

            missing = find_missing(self.cols[i])
            if len(missing) == 1:
                np.place(self.cols[i], self.cols[i] == 0, missing[0])
            elif len(missing) > 1:
                print(f'Column {i+1} too complex')

            missing = find_missing(self.regions[i])
            if len(missing) == 1:
                np.place(self.regions[i], self.regions[i] == 0, missing[0])
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
    print(sud)
    sud.simple_missing_solve()
    print(sud)
