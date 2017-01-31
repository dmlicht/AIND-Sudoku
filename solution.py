from collections import defaultdict, namedtuple

from utils import *

assignments = []


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


TwinPair = namedtuple("Twin", "one two value unit")


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    len_2_values = {box: val for (box, val) in values.items() if len(val) == 2}
    for len_2_box, len_2_val in len_2_values.items():
        for unit in units[len_2_box]:
            twins = filter_for_twin(len_2_box, len_2_val, unit, values)
            if len(twins) == 1:
                twin = twins[0]
                print(unit, len_2_box, len_2_val, twin, values[twin])
                print([values[box] for box in unit])
                twin_peers = [peer for peer in unit if peer not in [len_2_box, twin]]
                for peer in twin_peers:
                    values[peer] = try_remove(values[peer], len_2_val)
                print([values[box] for box in unit])
    return values

def find_twins(values):
    """ Find all pairs of twins within units in values """
    found_twins = []
    len_2_values = {box: val for (box, val) in values.items() if len(val) == 2}
    for len_2_box, len_2_val in len_2_values.items():
        for unit in units[len_2_box]:
            twins = filter_for_twin(len_2_box, len_2_val, unit, values)
            if len(twins) == 1:
                twin = twins[0]
                found_twins.append(TwinPair(len_2_box, twin, len_2_val, unit))
    return found_twins


def filter_for_twin(box, val, unit, values):
    return [peer for peer in unit if box != peer and values[peer] == val]


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    single_values = {k: v for k, v in values.items() if len(v) == 1}

    for key, val in single_values.items():
        for peer in peers[key]:
            values[peer] = try_remove(values[peer], val)
    return values


def try_remove(source, sub):
    ## TODO: maybe I can just get rid of this.
    replaced = str(source)
    for digit in list(sub):
        print("trying to remove sub:", digit, "from source:", replaced)
        if digit in replaced:
            replaced = replaced.replace(digit, "")
            print(replaced)
    return replaced


def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    new_values = values.copy()

    for unit in unitlist:
        values_seen = value_appearence_dict(unit, values)
        values_seen_once = {val: boxes for val, boxes in values_seen.items() if len(boxes) == 1}
        updates = {boxes[0]: val for val, boxes in values_seen_once.items()}
        new_values.update(updates)

    return new_values


def value_appearence_dict(unit, values):
    """ Returns a dictionary mapping numbers to the list of boxes where they appear """

    values_seen = defaultdict(list)
    for box in unit:
        for num in list(values[box]):
            values_seen[num].append(box)
    return values_seen


def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    constraints = [eliminate, only_choice]
    stalled = False
    solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

    while not stalled:
        for constraint in constraints:
            values = constraint(values)

        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        solved_values_before = solved_values_after

        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """Using depth-first search and propagation, create a search tree and solve the sudoku."""

    values = reduce_puzzle(values)
    if not values:
        return False

    done = all(len(val) == 1 for val in values.values())
    if done:
        return values

    # Choose one of the unfilled squares with the fewest possibilities
    multi_option_boxes = {k: v for k, v in values.items() if len(v) > 1}
    sorted_boxes = sorted(multi_option_boxes.items(), key=lambda x: len(x[1]))

    (box, vals) = sorted_boxes[0]

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for val in vals:
        edited_dict = dict(values)

        edited_dict[box] = val

        search_result = search(edited_dict)
        if search_result:
            return search_result
    return False


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    return search(values)


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments

        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
