from collections import defaultdict

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


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers


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
    if sub in source:
        return source.replace(sub, "")
    else:
        return source


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

    # TODO: Implement only choice strategy here
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
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."

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
