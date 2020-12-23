import sys
import copy
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def get_input_data_as_list(file_name):
    """ 
    Reads in data from the given file and returns them as list
        with one entry per line and whitespaced trimmed 
    """
    with open(file_name) as input_file:
        #data_list = list(input_file.readlines())
        #data_list = list(map(list, input_file.readlines()))
        data_list = input_file.readlines()
        data_list = [str.strip(line) for line in data_list]
        data_list = [list(line) for line in data_list]
    return data_list

def increase_pane(pane):
    for row in pane:
        row.append('.')
        row.reverse()
        row.append('.')
        row.reverse()
    pane.append(['.'] * len(pane[0]))
    pane.reverse()
    pane.append(['.'] * len(pane[0]))
    pane.reverse()
    pass

def fill_dimension(pocket_dimension):
    for pane in pocket_dimension:
        increase_pane(pane)
    pocket_dimension.append([['.'] * len(pocket_dimension[0]) for x in range(len(pocket_dimension[0]))])
    pocket_dimension.reverse()
    pocket_dimension.append([['.'] * len(pocket_dimension[0]) for x in range(len(pocket_dimension[0]))])
    pocket_dimension.reverse()
    return pocket_dimension

def activate_cube(pane, row_idx, column_idx, pane_idx):
    active = get_all_dimension_active_neighbors(pane, row_idx, column_idx, pane_idx)
    #print(row_idx, column_idx, active)
    if active == 3:
        return True
    else:
        return False

def inactivate_cube(pane, row_idx, column_idx, pane_idx):
    active = get_all_dimension_active_neighbors(pane, row_idx, column_idx, pane_idx) - 1
    #print(row_idx, column_idx, active)
    if active < 2 or active > 3:
        return True
    else:
        return False

def get_pane_active_cubes(pane, row_idx, column_idx):
    active_cubes = [cube for row in pane[row_idx-1:row_idx+2] for cube in row[column_idx-1:column_idx+2] if cube == '#']
    return len(active_cubes)

def get_all_dimension_active_neighbors(pocket_dimension, row_idx, column_idx, pane_idx):
    active = 0
    for pane in pocket_dimension[pane_idx-1:pane_idx+2]:
        active += get_pane_active_cubes(pane, row_idx, column_idx)
    return active

def print_pane(pane):
    print()
    for row in pane:
        print("".join(row))
    print()

def print_pocket_dimension(pocket_dimension):
    for pane_idx, pane in enumerate(pocket_dimension):
        print(f"Z={pane_idx}")
        print_pane(pane)

def activate_cubes(pocket_dimension_in):
    pocket_dimension_copy = copy.deepcopy(pocket_dimension_in)
    for pane_idx, pane in enumerate(pocket_dimension_in[1:-1],1):
        for row_idx,row in enumerate(pane[1:-1],1):
            for column_idx,cube in enumerate(row[1:-1],1):
                if cube == '.':
                    if activate_cube(pocket_dimension_in, row_idx, column_idx, pane_idx):
                        pocket_dimension_copy[pane_idx][row_idx][column_idx] = '#'
                elif cube == '#':
                    if inactivate_cube(pocket_dimension_in, row_idx, column_idx, pane_idx):
                        pocket_dimension_copy[pane_idx][row_idx][column_idx] = '.'
                        pass
    return pocket_dimension_copy

def count_active(pocket_dimension):
    cubes = [cube for pane in pocket_dimension for row in pane for cube in row if cube == '#'].count('#')
    return cubes

def find_seats(pane):
    seated_old = -1
    seated_new = -2
    while seated_old != seated_new:
        cls()
        seated_old = seated_new
        pane = activate_cubes(pane)
        seated_new = count_active(pane)
        print_pane(pane)
    return seated_new

def test_activation(pocket_dimension, max_rounds):
    for round in range(0, max_rounds):
        cls()
        print(f"Round {round}")
        #print_pocket_dimension(pocket_dimension)
        fill_dimension(pocket_dimension)
        #print_pocket_dimension(pocket_dimension)
        pocket_dimension = activate_cubes(pocket_dimension)
        #seated_new = count_active(pane)
        print_pocket_dimension(pocket_dimension)
        input("Press Enter to continue ... ")
        #if seated_old == seated_new:
        #    break
    return count_active(pocket_dimension)

def build_pocket_dimension(pane):
    pocket_dimension = []
    pocket_dimension.append([['.'] * len(pane) for x in range(len(pane))])
    pocket_dimension.append(pane)
    pocket_dimension.append([['.'] * len(pane) for x in range(len(pane))])
    return pocket_dimension

pane = get_input_data_as_list(sys.argv[1])
increase_pane(pane)

pocket_dimension = build_pocket_dimension(pane)

print_pocket_dimension(pocket_dimension)

#print(pocket_dimension)

input("Press Enter to continue ... ")


#print(f"Occupied seats 1st star when stable: {find_seats(get_pane_active_cubes, 4, pane)}")
print(f"Occupied seats 1st star when stable: {test_activation(pocket_dimension, 6)}")


