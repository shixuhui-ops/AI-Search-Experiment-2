from solution import (
    astar_path,
    astar_path_stats,
    weighted_astar_cost,
    TreeNode,
    minimax,
    alpha_beta,
    treasure_distances,
    treasure_minimax,
    treasure_alpha_beta,
)


maze = [
    ["S", ".", ".", "X", "."],
    [".", "X", ".", ".", "."],
    [".", "X", ".", "X", "."],
    [".", ".", ".", "X", "E"],
    ["X", "X", ".", ".", "."],
]

weighted_grid = [
    ["S", 1, 1, 8, 1],
    [1, 8, 3, 1, 1],
    [1, 8, 1, 8, 1],
    [1, 1, 1, 8, 1],
    [8, 8, 1, 1, "E"],
]

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

min1 = TreeNode(children=[max1, max2])
min2 = TreeNode(children=[max2, max3])
root = TreeNode(children=[min1, min2])

treasure_grid = [
    ["A", 1, 1, "X", 2, 1, "T1"],
    [1, "X", 6, "X", 1, "X", 1],
    [1, 1, "T2", 1, 1, 1, 1],
    ["X", 1, "X", 8, "X", 1, "X"],
    [1, 1, 1, 1, "T3", 1, 1],
    [1, "X", 9, "X", 1, "X", 1],
    ["T4", 1, 1, "X", 1, 1, "B"],
]

points = [
    (0, 0),
    (6, 6),
    (0, 6),
    (2, 2),
    (4, 4),
    (6, 0),
]

names = ["A", "B", "T1", "T2", "T3", "T4"]

values = {
    "T1": 9,
    "T2": 7,
    "T3": 8,
    "T4": 7,
}


print("题目一：迷宫 A*")
print(astar_path((0, 0), (3, 4), maze))
print(
    "h=0 节点数:",
    astar_path_stats((0, 0), (3, 4), maze, False)[1]
)

print(
    "曼哈顿启发式节点数:",
    astar_path_stats((0, 0), (3, 4), maze, True)[1]
)

print()
print("题目二：加权地形 A*")
print(weighted_astar_cost((0, 0), (4, 4), weighted_grid))

print()
print("题目三：Minimax 与 Alpha-Beta")
print("Minimax:", minimax(root))
print("Alpha-Beta:", alpha_beta(root))

print()
print("题目四：距离矩阵")
distances = treasure_distances(treasure_grid, points)

for row in distances:
    print(row)

print()
print("题目四：博弈结果")
print("Minimax H=2:", treasure_minimax(
    distances, names, values, 2
))
print("Minimax H=4:", treasure_minimax(
    distances, names, values, 4
))
print("Alpha-Beta H=2:", treasure_alpha_beta(
    distances, names, values, 2
))
print("Alpha-Beta H=4:", treasure_alpha_beta(
    distances, names, values, 4
))