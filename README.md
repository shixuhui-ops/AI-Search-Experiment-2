# 实验二：搜索算法

GitHub 仓库：

https://github.com/shixuhui-ops/AI-Search-Experiment-2

## 项目简介

本项目实现了《当代人工智能实验课》实验二要求的搜索算法，包括：

- 迷宫环境中的 A* 最短路径搜索
- 加权地形环境中的 A* 最小代价搜索
- Minimax 极大极小搜索
- Alpha-Beta 剪枝
- 竞争环境下的宝藏分配博弈
- A* 启发函数性能对比
- Minimax 与 Alpha-Beta 节点访问数量对比
- 无解情况和边界情况测试
- Python unittest 自动化测试

## 文件说明

    solution.py
        所有核心算法实现。

    run_experiment.py
        运行实验样例并输出全部实验结果。

    test_solution.py
        自动化测试文件。

    make_report.py
        根据实验报告 Markdown 文件生成 PDF。

    实验报告.md
        实验报告源文件。

    实验报告.pdf
        最终实验报告，控制在 5 页以内。

    experiment_results.txt
        实验运行结果记录。

    make_pdf.py
        PDF 报告生成脚本。

    实验二提交.zip
        最终提交压缩包。

## 环境要求

    Python 3.8 或更高版本
    reportlab
    pypdf

安装 PDF 生成依赖：

    python -m pip install reportlab pypdf

## 题目一：迷宫 A*

函数：

    astar_path(start, goal, grid)

参数：

- `start`：起点坐标，格式为 `(row, col)`
- `goal`：终点坐标，格式为 `(row, col)`
- `grid`：二维网格
- `X`：不可通行障碍物
- `.`、`S`、`E`：可通行位置

返回值：

    List[Tuple[int, int]]

如果存在路径，返回从起点到终点的坐标序列；如果无解，返回空列表 `[]`。

示例：

    grid = [
        ["S", ".", ".", "X", "."],
        [".", "X", ".", ".", "."],
        [".", "X", ".", "X", "."],
        [".", ".", ".", "X", "E"],
        ["X", "X", ".", ".", "."],
    ]

    path = astar_path((0, 0), (3, 4), grid)
    print(path)

输出：

    [(0, 0), (0, 1), (0, 2), (1, 2),
     (1, 3), (1, 4), (2, 4), (3, 4)]

## 题目二：加权地形 A*

函数：

    weighted_astar_cost(start, goal, grid)

地图中的数字代表进入对应地形的代价。

- `1`：平原
- `3`、`6`、`8`、`9`：不同代价的地形
- `X`：障碍物
- `S`：起点
- `E`：终点，进入终点的代价为 0

返回从起点到终点的最小总代价。无解时返回 `-1`。

    cost = weighted_astar_cost((0, 0), (4, 4), weighted_grid)
    print(cost)

输出：

    7

## 题目三：Minimax 与 Alpha-Beta

树节点定义：

    class TreeNode:
        def __init__(self, value=None, children=None):
            self.value = value
            self.children = children if children is not None else []

Minimax 函数：

    minimax(root)

Alpha-Beta 函数：

    alpha_beta(root)

两种算法均从 MAX 根节点开始，之后交替进行 MAX 和 MIN 操作。

在相同测试树上：

    Minimax 结果：5
    Alpha-Beta 结果：5

Alpha-Beta 的结果与 Minimax 相同，但可以跳过不可能影响最终结果的分支。

## 题目四：宝藏分配博弈

综合题使用 A* 预先计算 A、B 和各个宝藏之间的最小移动代价，形成距离矩阵。

点的顺序为：

    [A, B, T1, T2, T3, T4]

距离矩阵为：

    [0, 12, 10, 4, 8, 8]
    [12, 0, 8, 8, 4, 10]
    [10, 8, 0, 6, 6, 12]
    [4, 8, 6, 0, 6, 6]
    [8, 4, 6, 6, 0, 6]
    [8, 10, 12, 6, 6, 0]

宝藏价值：

    values = {
        "T1": 9,
        "T2": 7,
        "T3": 8,
        "T4": 7,
    }

收益计算方式：

    Gain = 宝藏价值 - 移动代价
    U = Score_A - Score_B

A 玩家选择使 `U` 最大的策略，B 玩家选择使 `U` 最小的策略。

搜索结果：

    H=2：
    最优首步为 T2
    最优收益差为 -1

    H=4：
    最优首步为 T3
    最优收益差为 3

Minimax 和 Alpha-Beta 得到相同结果。

## 性能分析

### A* 启发函数对比

在相同迷宫上测试：

    h=0：扩展 16 个节点
    曼哈顿距离：扩展 14 个节点

节点数减少：

    2 个

减少比例：

    12.5%

说明合理的启发函数可以在保证最优性的同时减少搜索范围。

### Alpha-Beta 剪枝对比

在相同博弈树上测试：

    Minimax：访问 15 个节点
    Alpha-Beta：访问 14 个节点

Alpha-Beta 减少访问：

    1 个节点

在更深、更宽的博弈树中，Alpha-Beta 剪枝的效果会更加明显。

## 边界情况

迷宫无解时：

    astar_path(start, goal, grid)

返回：

    []

加权地图无解时：

    weighted_astar_cost(start, goal, grid)

返回：

    -1

程序能够正确处理无解地图，不会进入死循环，也不会返回非法路径。

## 运行实验

执行完整实验：

    python run_experiment.py

保存实验结果：

    python run_experiment.py | Tee-Object experiment_results.txt

## 自动化测试

运行全部测试：

    python -m unittest test_solution.py -v

当前测试覆盖：

- 迷宫 A* 路径搜索
- 迷宫无解情况
- 加权地形 A*
- Minimax
- Alpha-Beta
- 宝藏博弈

预期结果：

    Ran 5 tests
    OK

## 生成实验报告 PDF

执行：

    python make_pdf.py

检查 PDF 页数：

    python -c "from pypdf import PdfReader; print(len(PdfReader('实验报告.pdf').pages))"

实验报告控制在 5 页以内。

## 生成提交压缩包

    Compress-Archive -Path solution.py,run_experiment.py,test_solution.py,make_report.py,实验报告.md,实验报告.pdf,experiment_results.txt -DestinationPath 实验二提交.zip -Force

最终压缩包包括：

    solution.py
    run_experiment.py
    test_solution.py
    make_report.py
    实验报告.md
    实验报告.pdf
    experiment_results.txt

## 最终验证

    python -m py_compile solution.py run_experiment.py test_solution.py
    python -m unittest test_solution.py -v
    python run_experiment.py

## 当前验证结果

自动化测试共 6 个，全部通过。

A* 使用曼哈顿启发函数后，扩展节点数从 16 个减少为 14 个。

在大规模博弈树上，Alpha-Beta 通过优化访问顺序将访问节点数从 73 个减少为 45 个。

宝藏 Minimax 使用记忆化搜索，减少了重复状态的计算。

距离矩阵计算利用无向地图的对称性，只计算上三角部分，再镜像填充下三角。
