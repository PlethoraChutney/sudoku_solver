import numpy as np


class Sudoku:

    def read_grid(self, file):
        puzzle = []
        with open(file) as f:
            for line in f:
                puzzle.append(line.split())
        self.grid = np.array(puzzle)

    def pretty_grid(self):
        pretty_grid = []
        for i in range(0, 9):
            pretty_grid_row = [str(x) for x in self.grid[i].tolist()]
            pretty_grid_row.insert(6, '|')
            pretty_grid_row.insert(3, '|')
            pretty_grid_row = ' '.join(pretty_grid_row)
            pretty_grid.append(pretty_grid_row)

            if i == 2 or i == 5:
                pretty_grid.append('------+-------+-------')

        pretty_grid = '\n'.join(pretty_grid)
        return pretty_grid

    def __repr__(self):
        return self.pretty_grid()


if __name__ == '__main__':
    sud = Sudoku()
    sud.read_grid('sudoku_solved.txt')
    print(sud)
