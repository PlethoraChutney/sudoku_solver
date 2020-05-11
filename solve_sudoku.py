import sys
import math
from itertools import islice

grid_key = {
    (0,0): 'A', (0,1): 'B', (0,2): 'C',
    (1,0): 'D', (1,1): 'E', (1,2): 'F',
    (2,0): 'G', (2,1): 'H', (2,2): 'I'
}
cells = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']


def check_equal(iterator):
    if len(iterator) == 0:
        return False
    iterator = iter(iterator)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    return all(first == rest for rest in iterator)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Slot:
    def __init__(self, value, index):
        self.value = int(value)
        self.index = index
        self.row = index[0]
        self.col = index[1]
        self.cell = grid_key[(math.floor(index[0]/3), math.floor(index[1]/3))]
        self.modified = False
        self.impossibles = set()
        self.possibles = set()

    def update(self, value):
        self.modified = True
        self.value = value

    def colored_value(self):
        if self.modified:
            return f'{bcolors.OKGREEN}{str(self.value)}{bcolors.ENDC}'
        elif self.value == 0:
            return f'{bcolors.FAIL}X{bcolors.ENDC}'
        else:
            return str(self.value)

    def __repr__(self):
        return self.colored_value()

    def update_possibles(self):
        self.possibles = set()
        for i in range(1,10):
            if i not in self.impossibles:
                self.possibles.add(i)


class Sudoku:

    def make_row(self, input, row_num):
        row = []
        for i in range(len(input)):
            row.append(Slot(input[i], (row_num, i)))
        return row

    def pretty_grid(self):
        to_print = []
        for i in range(len(self.grid)):
            to_print.append(self.grid[i].colored_value())

            if (i+1) % 27 == 0 and i != 80:
                to_print.append('\n------+-------+-------\n')
            elif (i+1) % 9 == 0:
                to_print.append('\n')
            elif (i + 1) % 3 == 0:
                to_print.append(' | ')
            else:
                to_print.append(' ')
        return ''.join(to_print)

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
                if slot.cell == cells[i]:
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
            if slot.value == 0:
                for neighbor in self.grid:
                    if neighbor.row == slot.row and neighbor.value != 0:
                        slot.impossibles.add(neighbor.value)
                    if neighbor.col == slot.col and neighbor.value != 0:
                        slot.impossibles.add(neighbor.value)
                    if neighbor.cell == slot.cell and neighbor.value != 0:
                        slot.impossibles.add(neighbor.value)

                slot.update_possibles()
                if len(slot.possibles) == 1:
                    slot.update(list(slot.possibles)[0])
                    modified = True

        return modified

    def unique_candidate_solve(self):
        modified = False

        for i in range(9):
            cell_slots = []
            row_slots = []
            col_slots = []

            for slot in self.grid:
                if slot.cell == cells[i]:
                    cell_slots.append(slot)
                if slot.row == i:
                    row_slots.append(slot)
                if slot.col == i:
                    col_slots.append(slot)

            for j in range(1,10):
                for list in [cell_slots, row_slots, col_slots]:
                    if j not in [x.value for x in list]:
                        possibles_list = [x for x in list if j in x.possibles]
                        if len(possibles_list) == 1:
                            possibles_list[0].update(j)
                            modified = True

        return modified

    def block_interaction_solve(self):
        force_rows = {
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],
            7: [],
            8: [],
            9: []
        }
        for i in range(1,10):
            for cell in cells:
                cell_force_row = []
                for slot in self.grid:
                    if i in slot.possibles and slot.cell == cell:
                        cell_force_row.append(slot.row)
                if check_equal(cell_force_row):
                    force_rows[i].append(cell_force_row[0])
        print(force_rows)

    def trivial_loop(self):
        while not self.solved:
            modified = self.single_possibility_solve()
            self.verify_grid()
            if not modified:
                break
            else:
                print('TS algorithm loop...')
        if self.solved:
            print('Sudoku solved.')
            return(True)
        elif self.filled:
            print('Unrecoverable (misfilled)')
            return(False)
        else:
            print('No trivial solution.')
            return(False)

    def unique_candidate_loop(self):
        while not self.solved:
            modified = self.unique_candidate_solve()
            if modified:
                print('UC found position...')
            else:
                print('No unique candidate.')
            self.verify_grid()

            if not modified:
                break
            elif self.trivial_loop():
                break

        if self.solved:
            print('Sudoku solved.')
            return True
        else:
            print('Unsolvable by unique candidate.')
            return False

    def solve_sudoku(self):
        print('Attempting trivial solve...')
        if not self.trivial_loop():
            print('Attempting unique candidate solve...')
            if not self.unique_candidate_loop():
                print('Attempting block interaction solve...')
                self.block_interaction_solve()


if __name__ == '__main__':
    sud = Sudoku(sys.argv[1])
    print(sud)
    sud.solve_sudoku()
    print(sud)
