import sys
import math

grid_key = {
    (0,0): 'A', (0,1): 'B', (0,2): 'C',
    (1,0): 'D', (1,1): 'E', (1,2): 'F',
    (2,0): 'G', (2,1): 'H', (2,2): 'I'
}

class Slot:
    def __init__(self, value, index):
        self.value = int(value)
        self.index = index
        self.row = index[0]
        self.col = index[1]
        self.cell = grid_key[(math.floor(index[0]/3), math.floor(index[1]/3))]

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
        self.grid = []
        with open(file) as f:
            i = 0
            for line in f:
                puzzle_row = list(line.replace('X', '0').strip())
                self.grid.extend(self.make_row(puzzle_row, i))
                i += 1

        self.solved = self.verify_grid()

    def pretty_grid(self):
        string_grid = [str(x.value) for x in self.grid]
        string_grid = ''.join(string_grid)

        pretty_grid = [
            ''.join(string_grid[0:9]),
            ''.join(string_grid[9:18]),
            ''.join(string_grid[18:27]),
            ''.join(string_grid[27:36]),
            ''.join(string_grid[36:45]),
            ''.join(string_grid[45:54]),
            ''.join(string_grid[54:63]),
            ''.join(string_grid[63:72]),
            ''.join(string_grid[72:81])
        ]

        print_grid = []
        for i in range(0, 9):
            pretty_grid_row = [str(x).replace('0', 'X') for x in pretty_grid[i]]
            pretty_grid_row.insert(6, '|')
            pretty_grid_row.insert(3, '|')
            pretty_grid_row = ' '.join(pretty_grid_row)
            print_grid.append(pretty_grid_row)

            if i == 2 or i == 5:
                print_grid.append('------+-------+-------')

        print_grid = '\n'.join(print_grid)
        return print_grid

    def verify_grid(self):
        if all(slot.value != 0 for slot in self.grid):
            self.filled = True
        else:
            self.filled = False
            return False

        sums = []
        for i in range(9):
            row_sum = 0
            col_sum = 0
            cell_sum = 0

            for slot in self.grid:
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

    def single_possibility_solve(self):
        modified = False

        for slot in self.grid:
            slot.update_possibles(self.grid)
            if len(slot.possibles) == 1:
                slot.value = slot.possibles[0]
                modified = True

        return modified

    # def unique_candidate_solve(self):
    #     modified = False
#
        # for i in range(9):
        #

    def solve_sudoku(self):
        print('Attempting trivial solve...')
        while not self.solved:
            modified = self.single_possibility_solve()
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
            print('Unsolvable by trivial solve.')


if __name__ == '__main__':
    sud = Sudoku(sys.argv[1])
    print(sud)
