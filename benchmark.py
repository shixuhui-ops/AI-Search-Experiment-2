import time

from solution import (
    astar_path_stats,
    TreeNode,
    minimax_stats,
    alpha_beta_stats,
)


maze = [
    ["S", ".", ".", "X", "."],
    [".", "X", ".", ".", "."],
    [".", "X", ".", "X", "."],
    [".", ".", ".", "X", "E"],
    ["X", "X", ".", ".", "."],
]


def measure_astar(use_heuristic):
    start_time = time.perf_counter()

    path, expanded_nodes = astar_path_stats(
        (0, 0),
        (3, 4),
        maze,
        use_heuristic,
    )

    elapsed = time.perf_counter() - start_time

    return {
        "path_length": len(path),
        "expanded_nodes": expanded_nodes,
        "time_ms": elapsed * 1000,
    }


left = TreeNode(children=[
    TreeNode(value=3),
    TreeNode(value=5),
])

right = TreeNode(children=[
    TreeNode(value=6),
    TreeNode(value=9),
])

root = TreeNode(children=[
    TreeNode(children=[left, right]),
    TreeNode(children=[
        TreeNode(value=1),
        TreeNode(value=2),
    ]),
])


def measure_tree(search_function):
    start_time = time.perf_counter()
    value, visited_nodes = search_function(root)
    elapsed = time.perf_counter() - start_time

    return {
        "value": value,
        "visited_nodes": visited_nodes,
        "time_ms": elapsed * 1000,
    }


print("A*，h=0：")
print(measure_astar(False))

print("A*，曼哈顿启发式：")
print(measure_astar(True))

print("Minimax：")
print(measure_tree(minimax_stats))

print("Alpha-Beta：")
print(measure_tree(alpha_beta_stats))