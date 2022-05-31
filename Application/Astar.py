import math

'''heuristic functions'''
def heuristic_function(endpoint,neighbour, heuristic):
    x1, y1 = endpoint.get_pos()
    x2, y2 = neighbour.get_pos()
    
    if heuristic == None: # by default h will always be 0
        return 0

    elif heuristic.lower() == "euclidean":
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        return math.sqrt(dx * dx + dy * dy)
    
    elif heuristic.lower() == "chebyshev":
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        return max(dx, dy)
        
    elif heuristic.lower() == "octile":
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)       
        return max(dx, dy) + math.sqrt(min(dx, dy))
        
    elif heuristic.lower() == "manhattan":
        return abs(x1 - x2) + abs(y1 - y2)
    
    elif heuristic.lower() == "minkowski":
        p = 2
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)         
        return (dx ** p + dy ** p) ** (1/p)

def find_lowest_f_score_node(f_scores, open_set):
    lowest_cell = None
    lowest_f_score = 0
    for cell in open_set:
        current_f_score = f_scores[cell]
        if lowest_cell == None or current_f_score < lowest_f_score:
            lowest_cell = cell
            lowest_f_score = current_f_score
    return lowest_cell

def reconstruct_path(came_from, f_scores, current_cell):
    tmp_cell = current_cell
    total_path = [tmp_cell]
    total_cost = 0
    while tmp_cell in came_from.keys():
        tmp_cell = came_from[tmp_cell]
        total_cost += f_scores[tmp_cell]
        total_path.append(tmp_cell)
    total_path.reverse()
    return total_path, total_cost

def A_Star(map, startpoint, heuristic):
    # The set of discovered nodes that may need to be (re-)expanded.
    # Initially, only the start node is known.
    open_set = set([startpoint])

    # Stores the cell immediately preceding the given cell
    came_from = {}

    # Stores the cost of the cheapest path from start to the given cell
    g_score = {}
    g_score[startpoint] = 0

    # Stores the f-score for the given cell
    f_score = {}
    f_score[startpoint] = heuristic_function(startpoint, startpoint, heuristic)
    total_iterations = 0
    while len(open_set) > 0:
        # This operation can occur in O(Log(N)) time if openSet is a min-heap or a priority queue
        current = find_lowest_f_score_node(f_score, open_set)
        if current == map.endpoint:
            path, total_cost = reconstruct_path(came_from, f_score, current)
            return path, total_cost, total_iterations

        open_set.remove(current)
        for neighbor in map.find_neighbors_in_radius(current):
            # d(current,neighbor) is the weight of the edge from current to neighbor
            # tentative_gScore is the distance from start to the neighbor through current
            weight = map.get_weight(neighbor)
            tentative_gScore = g_score[current] + weight
            if not neighbor in g_score.keys():
                # This path to neighbor is better than any previous one. Record it!
                came_from[neighbor] = current
                g_score[neighbor] = tentative_gScore
                f_score[neighbor] = tentative_gScore + heuristic_function(map.endpoint, neighbor, heuristic)
                if neighbor not in open_set:
                    open_set.add(neighbor)
        total_iterations += 1
    # Open set is empty but goal was never reached
    return [],0,0
