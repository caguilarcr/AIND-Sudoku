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
    naked_boxes = {}
    for box in values.keys():
        vals = values[box]
        if len(vals) == 2: # for naked_siblings we could use len(vals) > 1 and len(vals) < 8:
            naked_peers = set()
            for pb in peers[box]:
                if vals == values[pb]:
                    naked_peers.add(pb)
            if naked_peers:
                naked_boxes[box] = naked_peers

    # Eliminate the naked twins as possibilities for their peers
    for box, naked_peers in naked_boxes.items():
        for peer_box in naked_peers:
            # find common peers
            for box_to_update in set(peers[box]).intersection(peers[peer_box]):
                # delete twin values
                for digit in values[box]:
                    assign_value(values, box_to_update, values[box_to_update].replace(digit, ''))

    return values

def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s+t for s in a for t in b]

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string): A grid in string form.
    Return:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':
            print(line)
    return

def eliminate(values):
    for box in values.keys():
        # Get the values for all the key's peers
        vals = set(values[pb] for pb in peers[box] if len(values[pb]) == 1)
        assign_value(values, box, ''.join([c for c in values[box] if c not in vals]))
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    if isinstance(grid, str):
        grid = grid_values(grid)
    grid = reduce_puzzle(grid)
    if grid is False:
        return False ## Failed earlier
    if all(len(grid[s]) == 1 for s in boxes):
        return grid ## Solved!
    n,s = min((len(grid[s]), s) for s in boxes if len(grid[s]) > 1)
    for value in grid[s]:
        new_sudoku = grid.copy()
        new_sudoku[s] = value
        attempt = solve(new_sudoku)
        if attempt:
            return attempt

def search(values):
    pass

rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
rows_array = ('ABC', 'DEF', 'GHI')
columns_array = ('123', '456', '789')
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in rows_array for cs in columns_array]
diagonal_units = [
    [row + str(i+1) for i, row in enumerate(rows)],
    [row + str(9-i) for i, row in enumerate(rows)]
]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], []))-set([s])) for s in boxes)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(grid_values(diag_sudoku_grid)))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
