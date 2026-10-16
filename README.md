# 实验二：搜索算法

`solution.py` 提供四组可直接调用的函数：

- `astar_path(start, goal, grid)`：四连通迷宫最短路径，无解返回 `[]`。
- `weighted_astar_cost(start, goal, grid)`：按进入目标格子的代价计算最小总成本；进入 `E` 为 0，无解返回 `-1`。
- `minimax(root)` 与 `alpha_beta(root)`：从 MAX 根节点开始、子节点从左到右访问。
- `treasure_distances(...)` 和 `treasure_game(...)`：综合题的距离矩阵与深度限制博弈搜索。

运行 `python solution.py` 可快速验证迷宫和博弈树样例。综合题中距离矩阵的点顺序约定为 `[A, B, T1, T2, ...]`，`values` 使用宝藏名称到分值的映射。

实现只依赖 Python 标准库。A* 的优先级为 `f=g+h`；加权地图使用最小正地形代价乘曼哈顿距离作为可采纳启发函数。Alpha-Beta 保持与 Minimax 相同的左到右访问顺序，便于统计剪枝效果。
