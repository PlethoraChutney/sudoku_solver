import sys
import math

grid_key = {
    (0,0): 'A', (0,1): 'B', (0,2): 'C',
    (1,0): 'D', (1,1): 'E', (1,2): 'F',
    (2,0): 'G', (2,1): 'H', (2,2): 'I'
}
cells = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
horiz_cells = {
    'A': ['B'],
    'B': ['A', 'C'],
    'C': ['B'],
    'D': ['E'],
    'E': ['D', 'F'],
    'F': ['E'],
    'G': ['H'],
    'H': ['G', 'I'],
    'I': ['H']
}
vert_cells = {
    'A': ['D'],
    'B': ['E'],
    'C': ['F'],
    'D': ['A', 'G'],
    'E': ['B', 'H'],
    'F': ['C', 'I'],
    'G': ['D'],
    'H': ['E'],
    'I': ['F']
}


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
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


class Slot:
    def __init__(self, value, index):
        self.value = int(value)
        self.index = index
        self.row = index[0]
        self.col = index[1]
        self.cell = grid_key[(math.floor(index[0]/3), math.floor(index[1]/3))]
        self.modified = False
        # use sets, not lists, because we don't want duplicates (length has meaning)
        self.impossibles = set()
        self.possibles = set()

        if self.value != 0:
            self.possibles.add(self.value)
            self.impossibles.update([x for x in range(1,10) if x != self.value])

    def update(self, value):
        # using update() sets a color for ones the algorithm solves
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
        # easier to define impossibles and deduce possibles than maintain two sets
        self.possibles = set()
        if self.value != 0:
            self.possibles = set([self.value])
            self.impossibles = set([x for x in range(10) if x != self.value])
        else:
            for i in range(1,10):
                if i not in self.impossibles:
                    self.possibles.add(i)

    def solve(self):
        if len(self.possibles) == 1 and self.value == 0:
            self.update(list(self.possibles)[0])
            return True
        else:
            return False


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

            # dumb hardcoding, would be better to do this modular for arbitrary
            # sudokus haha
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
        # it's technically possible to make 45 from numbers other than the correct
        # 1--9, but that would be obvious
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

    def trivial_solve(self):
        # check if a given slot has only have one valid value
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
                if slot.solve():
                    modified = True

        return modified

    def unique_candidate_solve(self):
        # checks if a subset only have one valid slot for a specific value
        modified = False

        # gather a list of cells, rows, and columns
        for i in range(9):
            cell_slots = []
            row_slots = []
            col_slots = []

            for slot in self.grid:
                slot.update_possibles()
                if slot.cell == cells[i]:
                    cell_slots.append(slot)
                if slot.row == i:
                    row_slots.append(slot)
                if slot.col == i:
                    col_slots.append(slot)

            # iterating over every possible value
            for value in range(1,10):
                # check each subset for that value
                for list in [cell_slots, row_slots, col_slots]:
                    # if it's not there, find which slots could hold it
                    if value not in [x.value for x in list]:
                        possibles_list = [x for x in list if value in x.possibles]
                        # if there's only one, that's where it goes
                        if len(possibles_list) == 1:
                            possibles_list[0].update(value)
                            possibles_list[0].update_possibles()
                            modified = True

            for slot in self.grid:
                slot.update_possibles()
                if slot.solve():
                    modified = True

        return modified

    def block_interaction_solve(self):
        # check if one block forces a number to be in a specific row/col in that block
        # which would make it an illegal row/col for adjacent blocks in that direction
        modified = False

        # find cells with a "forced" row or column,in which all possible slots for
        # a value are in the same row or column
        for cell in cells:
            for value in range(1,10):
                cell_force_row = []
                cell_force_col = []
                for slot in self.grid:
                    if value in slot.possibles and slot.cell == cell:
                        cell_force_row.append(slot.row)
                        cell_force_col.append(slot.col)

                # if the cell has a forced row
                if check_equal(cell_force_row):
                    # for every slot in the grid which is in that row, not currently
                    # filled, and is in a horizontally-adjacent cell
                    for slot in self.grid:
                        if slot.row == cell_force_row[0] and slot.value == 0\
                                and slot.cell in horiz_cells[cell]:
                            # that value is impossible
                            slot.impossibles.add(value)
                # same for columns
                if check_equal(cell_force_col):
                    for slot in self.grid:
                        if slot.row == cell_force_row[0] and slot.value == 0\
                                and slot.cell in vert_cells[cell]:
                            slot.impossibles.add(value)

        for slot in self.grid:
            slot.update_possibles()
            if slot.solve():
                modified = True

        return modified

    def trivial_loop(self):
        modified = False
        while not self.solved:
            single_loop_modified = self.trivial_solve()
            if not modified:
                modified = single_loop_modified
            self.verify_grid()
            if not modified:
                print('No trivials found.')
                return modified
            else:
                print('Trivials found.')
                break
        if not self.solved and self.filled:
            print('Unrecoverable (misfilled)')
            sys.exit(1)
        else:
            return modified

    def unique_candidate_loop(self):
        while not self.solved:
            modified = self.unique_candidate_solve()
            self.verify_grid()

            if not modified:
                print('No unique candidate.')
                break
            else:
                print('UCs found, attempting TS...')
                if not self.trivial_loop():
                    break

        if self.solved:
            return modified

    def block_interaction_loop(self):
        while not self.solved:
            modified = self.block_interaction_solve()
            self.verify_grid()

            if not modified:
                print('No useful block interactions.')
                break
            else:
                print('BIs found, attempting UC...')
                if not self.unique_candidate_loop():
                    break

        if self.solved:
            return modified

    def solve_sudoku(self):
        modified = False
        while not self.solved:
            modified = False
            print('Beginning full loop')
            print('Attempting trivial solve...')
            if self.trivial_loop():
                modified = True
            if not self.solved:
                print('Attempting unique candidate solve...')
                if self.unique_candidate_loop():
                    modified = True
            if not self.solved:
                print('Attempting block interaction solve...')
                if self.block_interaction_loop():
                    modified = True
            if not modified:
                print('Not modified since last full loop. Giving up.')
                break
        if self.solved:
            print('Sudoku solved.')


if __name__ == '__main__':
    sud = Sudoku(sys.argv[1])
    print(sud)
    sud.solve_sudoku()
    print(sud)
