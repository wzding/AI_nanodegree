assignments = []

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

rows = 'ABCDEFGHI'
cols = '123456789'
# create a variable to store diagonal unit
diag = [ [rows[i]+cols[i] for i in range(len(rows))],\
[rows[i]+cols[len(rows)-1-i] for i in range(len(rows))] ]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

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
    # dict_unit's key is a unit and its values is a string of two numbers
    # {'B4': '46', 'B5': '46', 'C2': '68'}
    dict_unit = dict( (key, values[key] ) for key in values if len(values[key])\
     == 2)
    # dict_value's key is a string of two numbers and its values is a list of
    # possible units, such as {'46': ['B4', 'B5'], '68': ['C2']}
    dict_value = dict( (i,[j for j in dict_unit if dict_unit[j] ==i]) \
    for i in set(dict_unit.values()))

    for v in dict_value:  # v is a string of two numbers
        length = len(dict_value[v])
        if length > 1: # there are two units have exactly same two values
            i = 0 ; j = i+1
            while i < length and j < length:
                curr = dict_value[v][i]  # curr and nxt are unit
                while j < length:
                    nxt = dict_value[v][j]
                    peer_list = [unitlist[i] for i in range(len(unitlist)) if \
                    curr in unitlist[i] and nxt in unitlist[i]]
                    # check whether curr and nxt are peers
                    if len(peer_list)>0:
                        for k in range(len(peer_list)):
                            # temp is a row or column or box of curr and nxt but
                            # does not contain these two units
                            temp = [ele for ele in peer_list[k] \
                            if ele != curr and ele != nxt]
                            # go through each unit in temp
                            for p in temp:
                                # go through each value in v
                                for v1 in v:
                                    if v1 in values[p]:
                                        values[p] = values[p].replace(v1, "")
                    j += 1
                i += 1; j = i+1
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
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
        if r in 'CF': print(line)
    return

def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    for v in values:
        if len(values[v]) == 1:
            temp = values[v]
            for p in peers[v]:
                if temp in values[p] :
                    values[p] = values[p].replace(temp, "")

    # diagonal line
    for d_list in diag:
        for d in d_list:
            if len(values[d]) == 1:
                temp = values[d]
                for g in d_list:
                    if g != d and temp in values[g]:
                        values[g] = values[g].replace(temp, "")

    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    # go through all units on diagnal lines
    for d_list in diag:
        for digit in '123456789':
            dplaces = [box for box in d_list if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    # go through all other pairs
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False

    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    value = reduce_puzzle(values)
    if not value:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    temp = {}
    for v in values:
        if len(values[v]) > 1:
            temp[v] = len(values[v])
    min_len = min(temp.values())
    min_unit = [k for k in temp.keys() if temp[k] == min_len][0]
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[min_unit]:
        new_sudoku = values.copy()
        new_sudoku[min_unit] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

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
