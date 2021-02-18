def go_to_next_coordinates(coord, vertical_step, horizontal_step):
    coord['y'] += vertical_step
    coord['x'] += horizontal_step
    return coord


def get_normal_vertical_position(segment_length, x_coord):
    if segment_length - 1 > x_coord or x_coord == 0 or segment_length == 0:
        return x_coord
    else:
        return x_coord % segment_length


# coordinates are x, y, where y is number of segment starting from 0
def read_location_sign(map, y_position, x_position):
    segment = map[y_position]
    return segment[x_position]


def calculate_number_of_trees(tree_map, vertical_step, horizontal_step):
    segment_length = len(tree_map[0])
    coordinates = dict(x=0, y=0)
    tree_sing = '#'
    tree_counter = 0

    while len(tree_map) > coordinates['y']:
        cursor_position = get_normal_vertical_position(segment_length, coordinates['x'])
        position_sign = read_location_sign(map=tree_map, y_position=coordinates['y'], x_position=cursor_position)

        tree_counter = tree_counter + 1 if position_sign == tree_sing else tree_counter

        coordinates = go_to_next_coordinates(coordinates, vertical_step, horizontal_step)

    print(tree_counter)
    return tree_counter


with open('input.txt') as file:
    tree_map = [row.replace('\n', '') for row in file.readlines()]
    trees_counts = []

    for h_step, v_step in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
        trees_counts.append(calculate_number_of_trees(tree_map, vertical_step=v_step, horizontal_step=h_step))

    total_sum = 1

    for trees_count in trees_counts:
        total_sum = total_sum * trees_count

    print(total_sum)