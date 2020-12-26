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

def increase_2d_pane(pane):
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

def increase_3d_dimension(pocket_dimension):
    for pane in pocket_dimension:
        increase_2d_pane(pane)
    pocket_dimension.reverse()
    pocket_dimension.append([['.'] * len(pocket_dimension[0]) for x in range(len(pocket_dimension[0]))])
    pocket_dimension.reverse()
    pocket_dimension.append([['.'] * len(pocket_dimension[0]) for x in range(len(pocket_dimension[0]))])
    #print_3d_dimension(pocket_dimension)
    return pocket_dimension

def increase_4d_dimension(hyper_dimension):
    for pocket_dimension in hyper_dimension:
        increase_3d_dimension(pocket_dimension)
    hyper_dimension.reverse()
    hyper_dimension.append([[['.'] * len(hyper_dimension[0][0]) for x in range(len(hyper_dimension[0][0]))] for y in range(len(hyper_dimension[0]))])
    hyper_dimension.reverse()
    hyper_dimension.append([[['.'] * len(hyper_dimension[0][0]) for x in range(len(hyper_dimension[0][0]))] for y in range(len(hyper_dimension[0]))])
    return hyper_dimension

def build_3d_pocket_dimension(pane):
    pocket_dimension = [pane]
    increase_3d_dimension(pocket_dimension)
    return pocket_dimension

def build_4d_hyper_dimension(pane):
    hyper_dimension = [[pane]]
    increase_4d_dimension(hyper_dimension)
    return hyper_dimension

def activate_3d_system_cube(pane, row_idx, column_idx, pane_idx):
    active = get_3d_dimension_active_neighbors(pane, row_idx, column_idx, pane_idx)
    #print(row_idx, column_idx, active)
    if active == 3:
        return True
    else:
        return False

def inactivate_3d_system_cube(pane, row_idx, column_idx, pane_idx):
    active = get_3d_dimension_active_neighbors(pane, row_idx, column_idx, pane_idx) - 1
    #print(row_idx, column_idx, active)
    if active < 2 or active > 3:
        return True
    else:
        return False

def activate_4d_system_cube(hyper_dimension, dim_idx, row_idx, column_idx, pane_idx):
    active = get_4d_dimension_active_neighbors(hyper_dimension, dim_idx, row_idx, column_idx, pane_idx)
    #print(dim_idx, row_idx, column_idx, active)
    if active == 3:
        return True
    else:
        return False

def inactivate_4d_system_cube(hyper_dimension, dim_idx, row_idx, column_idx, pane_idx):
    active = get_4d_dimension_active_neighbors(hyper_dimension, dim_idx, row_idx, column_idx, pane_idx) - 1
    #print(dim_idx, row_idx, column_idx, active)
    if active < 2 or active > 3:
        return True
    else:
        return False

def get_2d_pane_active_neighbors(pane, row_idx, column_idx):
    active = len([cube for row in pane[row_idx-1:row_idx+2] for cube in row[column_idx-1:column_idx+2] if cube == '#'])
    return active

def get_3d_dimension_active_neighbors(pocket_dimension, row_idx, column_idx, pane_idx):
    active = 0
    for pane in pocket_dimension[pane_idx-1:pane_idx+2]:
        active += get_2d_pane_active_neighbors(pane, row_idx, column_idx)
    return active

def get_4d_dimension_active_neighbors(hyper_dimension, dim_idx, row_idx, column_idx, pane_idx):
    active = 0
    for pocket_dimension in hyper_dimension[dim_idx-1:dim_idx+2]:
        active += get_3d_dimension_active_neighbors(pocket_dimension, row_idx, column_idx, pane_idx)
    return active

def print_2d_pane(pane):
    print()
    for row in pane:
        print("".join(row))
    print()

def print_3d_dimension(pocket_dimension):
    for pane_idx, pane in enumerate(pocket_dimension):
        print(f"Z={pane_idx}")
        print_2d_pane(pane)

def print_4d_dimension(hyper_dimension):
    for dimension_id, pocket_dimension in enumerate(hyper_dimension):
        print(f"W={dimension_id}")
        print_3d_dimension(pocket_dimension)

def activate_3d_system_cubes(pocket_dimension_in):
    pocket_dimension_copy = copy.deepcopy(pocket_dimension_in)
    for pane_idx, pane in enumerate(pocket_dimension_in[1:-1],1):
        for row_idx,row in enumerate(pane[1:-1],1):
            for column_idx,cube in enumerate(row[1:-1],1):
                if cube == '.':
                    if activate_3d_system_cube(pocket_dimension_in, row_idx, column_idx, pane_idx):
                        pocket_dimension_copy[pane_idx][row_idx][column_idx] = '#'
                elif cube == '#':
                    if inactivate_3d_system_cube(pocket_dimension_in, row_idx, column_idx, pane_idx):
                        pocket_dimension_copy[pane_idx][row_idx][column_idx] = '.'
    return pocket_dimension_copy

def activate_4d_system_cubes(hyper_dimension_in):
    hyper_dimension_copy = copy.deepcopy(hyper_dimension_in)
    for dim_idx, pocket_dimension in enumerate(hyper_dimension_in[1:-1],1):
        for pane_idx, pane in enumerate(pocket_dimension[1:-1],1):
            for row_idx, row in enumerate(pane[1:-1],1):
                for column_idx, cube in enumerate(row[1:-1],1):
                    if cube == '.':
                        if activate_4d_system_cube(hyper_dimension_in, dim_idx, row_idx, column_idx, pane_idx):
                            hyper_dimension_copy[dim_idx][pane_idx][row_idx][column_idx] = '#'
                    elif cube == '#':
                        if inactivate_4d_system_cube(hyper_dimension_in, dim_idx, row_idx, column_idx, pane_idx):
                            hyper_dimension_copy[dim_idx][pane_idx][row_idx][column_idx] = '.'
    return hyper_dimension_copy

def count_2d_active(pane):
    cubes = [cube for row in pane for cube in row if cube == '#'].count('#')
    return cubes

def count_3d_active(pocket_dimension):
    cubes = sum([count_2d_active(pane) for pane in pocket_dimension])
    return cubes

def count_4d_active(hyper_dimension):
    cubes = sum([count_3d_active(pocket_dimension) for pocket_dimension in hyper_dimension])
    return cubes

def activate_3d_system(pocket_dimension, max_rounds):
    for round in range(0, max_rounds):
        print(f"Round {round}")
        increase_3d_dimension(pocket_dimension)
        pocket_dimension = activate_3d_system_cubes(pocket_dimension)
    return count_3d_active(pocket_dimension)

def activate_4d_system(hyper_dimension, max_rounds):
    for round in range(0, max_rounds):
        print(f"Round {round}")
        increase_4d_dimension(hyper_dimension)
        hyper_dimension = activate_4d_system_cubes(hyper_dimension)
    return count_4d_active(hyper_dimension)

def test_activation_3d_system(pocket_dimension, max_rounds):
    for round in range(0, max_rounds):
        cls()
        print(f"Round {round}")
        increase_3d_dimension(pocket_dimension)
        pocket_dimension = activate_3d_system_cubes(pocket_dimension)
        print_3d_dimension(pocket_dimension)
        input("Press Enter to continue ... ")
    return count_3d_active(pocket_dimension)

def test_activation_4d_system(hyper_dimension, max_rounds):
    for round in range(0, max_rounds):
        cls()
        print(f"Round {round}")
        increase_4d_dimension(hyper_dimension)
        hyper_dimension = activate_4d_system_cubes(hyper_dimension)
        print_4d_dimension(hyper_dimension)
        input("Press Enter to continue ... ")
    #return count_3d_active(hyper_dimension)

pane = get_input_data_as_list(sys.argv[1])

pocket_dimension = build_3d_pocket_dimension(pane)

print_3d_dimension(pocket_dimension)

#print(pocket_dimension)

#input("Press Enter to continue ... ")


print(f"Active 3d system cubes: {activate_3d_system(pocket_dimension, 6)}")

pane = get_input_data_as_list(sys.argv[1])
hyper_dimension = build_4d_hyper_dimension(pane)
print_4d_dimension(hyper_dimension)

print(f"Active 4d system cubes: {activate_4d_system(hyper_dimension, 6)}")

