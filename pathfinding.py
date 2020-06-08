def find_path(grid, start_node, target_node):
    open_set = []
    closed_set = set([])

    open_set.append(start_node)

    while len(open_set) > 0:
        current_node = open_set[0]
        for i in range(1, len(open_set)):
            if open_set[i].f_cost() > current_node.f_cost() or open_set[i].f_cost() == current_node.f_cost() and open_set[i].h_cost == current_node.h_cost:
                current_node = open_set[i]
            
        open_set.remove(current_node)
        closed_set.add(current_node)

        # Path has been found
        if current_node.coordinates() == target_node.coordinates():
            return retrace_path(start_node, target_node)

        for neighbour_node in grid.get_neighbours(current_node):
            if not neighbour_node.safe or neighbour_node in closed_set:
                continue

            new_move_cost_to_neighbour = current_node.g_cost + get_distance(current_node, neighbour_node)

            if new_move_cost_to_neighbour > neighbour_node.g_cost or not neighbour_node in open_set:
                neighbour_node.g_cost = new_move_cost_to_neighbour
                neighbour_node.h_cost = get_distance(neighbour_node, target_node)
                neighbour_node.parent = current_node

                if neighbour_node not in open_set:
                    open_set.append(neighbour_node)

def get_distance(node_a, node_b):
    return abs(node_a.x - node_b.x) + abs(node_a.y - node_b.y)

def retrace_path(start_node, target_node):
    path = []
    current_node = target_node

    while current_node != start_node:
        path.append(current_node)
        current_node = current_node.parent
    path.append(current_node)

    return path[::-1]