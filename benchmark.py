import time
from math import factorial

from solution import (
    astar_path_stats,
    TreeNode,
    minimax_stats,
    alpha_beta_stats,
    reverse_tree,
    treasure_alpha_beta,
    treasure_minimax,
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


max1 = TreeNode(children=[
    TreeNode(value=3),
    TreeNode(value=5),
])

max2 = TreeNode(children=[
    TreeNode(value=6),
    TreeNode(value=9),
])

max3 = TreeNode(children=[
    TreeNode(value=1),
    TreeNode(value=2),
])

min1 = TreeNode(children=[
    max1,
    max2,
])

min2 = TreeNode(children=[
    max2,
    max3,
])

root = TreeNode(children=[
    min1,
    min2,
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


def build_tree(depth, base_value=0):
    if depth == 0:
        return TreeNode(value=base_value)

    children = []

    for index in range(3):
        child = build_tree(
            depth - 1,
            base_value * 3 + index
        )
        children.append(child)

    return TreeNode(children=children)


large_tree = build_tree(4, 1)

normal_value, normal_nodes = alpha_beta_stats(large_tree)

reversed_large_tree = reverse_tree(large_tree)
reversed_value, reversed_nodes = alpha_beta_stats(
    reversed_large_tree
)

print("大规模博弈树：")
print("原顺序:", {
    "value": normal_value,
    "visited_nodes": normal_nodes,
})

print("反转顺序:", {
    "value": reversed_value,
    "visited_nodes": reversed_nodes,
})

print(
    "访问节点差异:",
    reversed_nodes - normal_nodes
)

print()
print("综合题 Alpha-Beta 节点排序：")

treasure_distance_matrix = [
    [0, 12, 10, 4, 8, 8],
    [12, 0, 8, 8, 4, 10],
    [10, 8, 0, 6, 6, 12],
    [4, 8, 6, 0, 6, 6],
    [8, 4, 6, 6, 0, 6],
    [8, 10, 12, 6, 6, 0],
]

treasure_names = ["A", "B", "T1", "T2", "T3", "T4"]

treasure_values = {
    "T1": 9,
    "T2": 7,
    "T3": 8,
    "T4": 7,
}

for search_depth in (2, 4):
    original = treasure_alpha_beta(
        treasure_distance_matrix,
        treasure_names,
        treasure_values,
        search_depth,
        return_stats=True,
    )

    ordered = treasure_alpha_beta(
        treasure_distance_matrix,
        treasure_names,
        treasure_values,
        search_depth,
        return_stats=True,
        order_moves=True,
    )

    print(f"H={search_depth} 原始顺序:", original)
    print(f"H={search_depth} 启发式排序:", ordered)

print()
print("Minimax 记忆化对照：")

symmetric_size = 8
symmetric_distances = [
    [0] * symmetric_size
    for _ in range(symmetric_size)
]
symmetric_names = [
    "A",
    "B",
    "T1",
    "T2",
    "T3",
    "T4",
    "T5",
    "T6",
]
symmetric_values = {
    name: 1
    for name in symmetric_names[2:]
}

uncached_states = sum(
    factorial(6) // factorial(6 - depth)
    for depth in range(7)
)

cached_result = treasure_minimax(
    symmetric_distances,
    symmetric_names,
    symmetric_values,
    6,
    return_stats=True,
)

reduction = (
    (uncached_states - cached_result["expanded_states"])
    / uncached_states
    * 100
)

print("无缓存理论节点数:", uncached_states)
print("缓存展开状态数:", cached_result["expanded_states"])
print("缓存命中次数:", cached_result["cache_hits"])
print(f"状态减少比例: {reduction:.1f}%")