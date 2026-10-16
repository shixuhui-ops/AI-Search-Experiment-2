import heapq


def astar_path(start, goal, grid):
    rows = len(grid)
    cols = len(grid[0])

    def heuristic(position):
        row, col = position
        return abs(row - goal[0]) + abs(col - goal[1])

    def neighbors(position):
        row, col = position

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row = row + dr
            new_col = col + dc

            if 0 <= new_row < rows and 0 <= new_col < cols:
                if grid[new_row][new_col] != "X":
                    yield (new_row, new_col)

    if grid[start[0]][start[1]] == "X":
        return []

    if grid[goal[0]][goal[1]] == "X":
        return []

    open_list = []
    heapq.heappush(open_list, (heuristic(start), 0, start))

    g_cost = {start: 0}
    parent = {}

    while open_list:
        _, current_cost, current = heapq.heappop(open_list)

        if current != start and current_cost != g_cost.get(current):
            continue

        if current == goal:
            path = [current]

            while current != start:
                current = parent[current]
                path.append(current)

            path.reverse()
            return path

        for next_position in neighbors(current):
            new_cost = g_cost[current] + 1

            if new_cost < g_cost.get(next_position, float("inf")):
                g_cost[next_position] = new_cost
                parent[next_position] = current

                f_cost = new_cost + heuristic(next_position)
                heapq.heappush(
                    open_list,
                    (f_cost, new_cost, next_position)
                )

    return []

def weighted_astar_cost(start, goal, grid):
    rows = len(grid)
    cols = len(grid[0])

    def get_cost(position):
        row, col = position
        value = grid[row][col]

        if value == "X":
            return None

        if value == "E":
            return 0

        if value in ("S", "A", "B") or str(value).startswith("T"):
            return 1

        return int(value)

    def heuristic(position):
        row, col = position
        return abs(row - goal[0]) + abs(col - goal[1])

    def neighbors(position):
        row, col = position

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row = row + dr
            new_col = col + dc

            if 0 <= new_row < rows and 0 <= new_col < cols:
                next_position = (new_row, new_col)

                if get_cost(next_position) is not None:
                    yield next_position

    if get_cost(start) is None or get_cost(goal) is None:
        return -1

    open_list = []
    heapq.heappush(open_list, (heuristic(start), 0, start))

    cost_so_far = {start: 0}

    while open_list:
        _, current_cost, current = heapq.heappop(open_list)

        if current_cost != cost_so_far.get(current):
            continue

        if current == goal:
            return current_cost

        for next_position in neighbors(current):
            step_cost = get_cost(next_position)
            new_cost = current_cost + step_cost

            if new_cost < cost_so_far.get(next_position, float("inf")):
                cost_so_far[next_position] = new_cost

                f_cost = new_cost + heuristic(next_position)

                heapq.heappush(
                    open_list,
                    (f_cost, new_cost, next_position)
                )

    return -1

class TreeNode:
    def __init__(self, value=None, children=None):
        self.value = value
        self.children = children if children is not None else []


def minimax(node, maximizing_player=True):
    if not node.children:
        return node.value

    child_values = [
        minimax(child, not maximizing_player)
        for child in node.children
    ]

    if maximizing_player:
        return max(child_values)

    return min(child_values)


def alpha_beta(node, maximizing_player=True, alpha=float("-inf"),
               beta=float("inf")):
    if not node.children:
        return node.value

    if maximizing_player:
        best_value = float("-inf")

        for child in node.children:
            value = alpha_beta(
                child,
                False,
                alpha,
                beta
            )

            best_value = max(best_value, value)
            alpha = max(alpha, best_value)

            if alpha >= beta:
                break

        return best_value

    best_value = float("inf")

    for child in node.children:
        value = alpha_beta(
            child,
            True,
            alpha,
            beta
        )

        best_value = min(best_value, value)
        beta = min(beta, best_value)

        if alpha >= beta:
            break

    return best_value

def treasure_distances(grid, points):
    distance_matrix = []

    for start in points:
        row = []

        for goal in points:
            distance = weighted_astar_cost(start, goal, grid)
            row.append(distance)

        distance_matrix.append(row)

    return distance_matrix

def treasure_minimax(distances, target_names, target_values,
                     depth, start_a=0, start_b=1):
    targets = tuple(range(2, len(target_names)))

    def search(position_a, position_b, remaining,
               score_a, score_b, maximizing, current_depth):
        if current_depth == depth or not remaining:
            return score_a - score_b, None

        if maximizing:
            best_value = float("-inf")
            best_target = None

            for target in remaining:
                distance = distances[position_a][target]

                if distance < 0:
                    continue

                gain = target_values[target_names[target]] - distance
                next_remaining = tuple(
                    item for item in remaining if item != target
                )

                value, _ = search(
                    target,
                    position_b,
                    next_remaining,
                    score_a + gain,
                    score_b,
                    False,
                    current_depth + 1
                )

                if value > best_value:
                    best_value = value
                    best_target = target_names[target]

            return best_value, best_target

        best_value = float("inf")

        for target in remaining:
            distance = distances[position_b][target]

            if distance < 0:
                continue

            gain = target_values[target_names[target]] - distance
            next_remaining = tuple(
                item for item in remaining if item != target
            )

            value, _ = search(
                position_a,
                target,
                next_remaining,
                score_a,
                score_b + gain,
                True,
                current_depth + 1
            )

            if value < best_value:
                best_value = value

        return best_value, None

    value, target = search(
        start_a,
        start_b,
        targets,
        0,
        0,
        True,
        0
    )

    return {
        "best_target": target,
        "best_value": value
    }

def treasure_alpha_beta(distances, target_names, target_values,
                        depth, start_a=0, start_b=1):
    targets = tuple(range(2, len(target_names)))

    def search(position_a, position_b, remaining,
               score_a, score_b, maximizing,
               current_depth, alpha, beta):

        if current_depth == depth or not remaining:
            return score_a - score_b, None

        if maximizing:
            best_value = float("-inf")
            best_target = None

            for target in remaining:
                distance = distances[position_a][target]

                if distance < 0:
                    continue

                gain = target_values[target_names[target]] - distance

                next_remaining = tuple(
                    item for item in remaining if item != target
                )

                value, _ = search(
                    target,
                    position_b,
                    next_remaining,
                    score_a + gain,
                    score_b,
                    False,
                    current_depth + 1,
                    alpha,
                    beta
                )

                if value > best_value:
                    best_value = value
                    best_target = target_names[target]

                alpha = max(alpha, best_value)

                if alpha >= beta:
                    break

            return best_value, best_target

        best_value = float("inf")

        for target in remaining:
            distance = distances[position_b][target]

            if distance < 0:
                continue

            gain = target_values[target_names[target]] - distance

            next_remaining = tuple(
                item for item in remaining if item != target
            )

            value, _ = search(
                position_a,
                target,
                next_remaining,
                score_a,
                score_b + gain,
                True,
                current_depth + 1,
                alpha,
                beta
            )

            best_value = min(best_value, value)
            beta = min(beta, best_value)

            if alpha >= beta:
                break

        return best_value, None

    value, target = search(
        start_a,
        start_b,
        targets,
        0,
        0,
        True,
        0,
        float("-inf"),
        float("inf")
    )

    return {
        "best_target": target,
        "best_value": value
    }

def astar_path_stats(start, goal, grid, use_heuristic=True):
    rows = len(grid)
    cols = len(grid[0])

    def heuristic(position):
        if not use_heuristic:
            return 0

        return abs(position[0] - goal[0]) + abs(position[1] - goal[1])

    def neighbors(position):
        row, col = position

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row = row + dr
            new_col = col + dc

            if 0 <= new_row < rows and 0 <= new_col < cols:
                if grid[new_row][new_col] != "X":
                    yield (new_row, new_col)

    open_list = []
    heapq.heappush(open_list, (heuristic(start), 0, start))

    g_cost = {start: 0}
    parent = {}
    expanded_nodes = 0

    while open_list:
        _, current_cost, current = heapq.heappop(open_list)

        if current_cost != g_cost.get(current):
            continue

        expanded_nodes += 1

        if current == goal:
            path = [current]

            while current != start:
                current = parent[current]
                path.append(current)

            path.reverse()
            return path, expanded_nodes

        for next_position in neighbors(current):
            new_cost = current_cost + 1

            if new_cost < g_cost.get(next_position, float("inf")):
                g_cost[next_position] = new_cost
                parent[next_position] = current

                f_cost = new_cost + heuristic(next_position)

                heapq.heappush(
                    open_list,
                    (f_cost, new_cost, next_position)
                )

    return [], expanded_nodes

def minimax_stats(node, maximizing_player=True):
    visited_nodes = 1

    if not node.children:
        return node.value, visited_nodes

    values = []

    for child in node.children:
        value, child_count = minimax_stats(
            child,
            not maximizing_player
        )

        values.append(value)
        visited_nodes += child_count

    if maximizing_player:
        return max(values), visited_nodes

    return min(values), visited_nodes


def alpha_beta_stats(node, maximizing_player=True,
                     alpha=float("-inf"),
                     beta=float("inf")):
    visited_nodes = 1

    if not node.children:
        return node.value, visited_nodes

    if maximizing_player:
        best_value = float("-inf")

        for child in node.children:
            value, child_count = alpha_beta_stats(
                child,
                False,
                alpha,
                beta
            )

            visited_nodes += child_count
            best_value = max(best_value, value)
            alpha = max(alpha, best_value)

            if alpha >= beta:
                break

        return best_value, visited_nodes

    best_value = float("inf")

    for child in node.children:
        value, child_count = alpha_beta_stats(
            child,
            True,
            alpha,
            beta
        )

        visited_nodes += child_count
        best_value = min(best_value, value)
        beta = min(beta, best_value)

        if alpha >= beta:
            break

    return best_value, visited_nodes

if __name__ == "__main__":
    start = (0, 0)
    goal = (3, 4)

    grid = [
        ["S", ".", ".", "X", "."],
        [".", "X", ".", ".", "."],
        [".", "X", ".", "X", "."],
        [".", ".", ".", "X", "E"],
        ["X", "X", ".", ".", "."]
    ]

    result = astar_path(start, goal, grid)
    print(result)