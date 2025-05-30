import random

def cross(A, B):
    return [a+b for a in A for b in B]

digits   = '123456789'
rows     = 'ABCDEFGHI'
cols     = digits
squares  = cross(rows, cols)
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
units = dict((s, [u for u in unitlist if s in u])
             for s in squares)
peers = dict((s, set(sum(units[s],[]))-set([s]))
             for s in squares)

def parse_grid(grid):
    values = dict((s, digits) for s in squares)
    for s,d in grid_values(grid).items():
        if d in digits and not assign(values, s, d):
            return False
    return values

def grid_values(grid):
    chars = [c for c in grid if c in digits or c in '0.']
    assert len(chars) == 81
    return dict(zip(squares, chars))

def assign(values, s, d):
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False

def eliminate(values, s, d):
    if d not in values[s]:
        return values
    values[s] = values[s].replace(d,'')
    if len(values[s]) == 0:
        return False
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False
        elif len(dplaces) == 1:
            if not assign(values, dplaces[0], d):
                return False
    return values

def solve(grid): return search(parse_grid(grid))

def replace_char_at_index(text, index, replacement):
  if 0 <= index < len(text):
    list_text = list(text)
    list_text[index] = replacement
    return "".join(list_text)
  else:
    return text

def has_unique_solution(grid):
    if not solve(grid):
        return False
    solutions = 0
    cells = list(grid)
    for index, cell in enumerate(cells):
        if cell == '0':
            for num in range(1, 10):
                grid = replace_char_at_index(grid, index, str(num))
                if solve(grid):
                    solutions += 1
    return solutions == 1

def search(values):
    if values is False:
        return False
    if all(len(values[s]) == 1 for s in squares):
        return values
    n,s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    return some(search(assign(values.copy(), s, d)) 
            for d in values[s])

def some(seq):
    for e in seq:
        if e: return e
    return False

def random_puzzle():
    values = dict((s, digits) for s in squares)
    for s in shuffled(squares):
        if not assign(values, s, random.choice(values[s])):
            break
        ds = [values[s] for s in squares if len(values[s]) == 1]
        if len(ds) == 30 and len(set(ds)) >= 8:
            grid = ''.join(values[s] if len(values[s])==1 else '0' for s in squares)
            if(has_unique_solution(grid)):
                return grid
    return random_puzzle()

def shuffled(seq):
    seq = list(seq)
    random.shuffle(seq)
    return seq

def generate_puzzle(difficulty):
    puzzle_cells = list(solve(random_puzzle()).values())
    cells_to_remove = get_removal_count(difficulty)
    cells = [i for i in range(81)]
    random.shuffle(cells)

    removed_count = 0
    for cell in cells:
        if removed_count >= cells_to_remove:
            break
        temp = puzzle_cells[cell]
        puzzle_cells[cell] = '0'
        grid = ''.join(puzzle_cells)
        if not has_unique_solution(grid):
            puzzle_cells[cell] = temp
        else:
            removed_count += 1
    grid = ''.join(puzzle_cells)
    return grid

def get_removal_count(difficulty):
  match difficulty:
      case 'easy':
          return random.randint(36, 46)
      case 'medium':
          return random.randint(51, 56)
      case 'hard':
          return random.randint(56, 61)
      case 'extreme':
          return random.randint(61, 64)