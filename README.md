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
- Alpha-Beta 子节点访问顺序对比
- Minimax 记忆化搜索
- 距离矩阵对称性优化
- 无解情况和边界情况测试
- Python unittest 自动化测试
- GitHub Actions 自动测试和覆盖率统计

## 文件说明

    solution.py
        所有核心算法实现。

    run_experiment.py
        运行题目给定样例并输出全部实验结果。

    test_solution.py
        自动化测试文件，共 11 个测试用例。

    benchmark.py
        测量运行时间、搜索节点数量和 Alpha-Beta 访问顺序影响。

    make_report.py
        根据实验报告 Markdown 文件生成 PDF。

    make_pdf.py
        将实验报告 Markdown 转换为 PDF。

    verify.ps1
        一键执行语法检查、自动化测试和完整实验。

    requirements.txt
        项目依赖文件。

    实验报告.md
        实验报告源文件。

    实验报告.pdf
        最终实验报告，控制在 5 页以内。

    experiment_results.txt
        实验运行结果记录。

    实验二提交.zip
        最终提交压缩包。

    .github/workflows/tests.yml
        GitHub Actions 自动测试和覆盖率工作流。

## 环境要求

    Python 3.8 或更高版本
    reportlab
    pypdf
    coverage

安装全部依赖：

    python -m pip install -r requirements.txt

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

### 大规模博弈树

在深度为 4、每个节点有 3 个子节点的博弈树上：

    原始访问顺序：访问 73 个节点
    反转访问顺序：访问 45 个节点
    最优值：141

两种访问顺序得到相同的最优值，但反转顺序少访问 28 个节点，说明 Alpha-Beta 的剪枝效率与子节点访问顺序密切相关。

## 优化策略

### 1. 启发函数

普通迷宫使用曼哈顿距离作为启发函数：

    h(n) = |row - goal_row| + |col - goal_col|

四方向移动时，曼哈顿距离不会高估真实剩余步数，因此具有可采纳性。

### 2. 距离矩阵对称性

地图移动代价具有对称性，因此距离矩阵只计算上三角部分，再将结果镜像填充到下三角，避免重复执行 A*。

### 3. Minimax 记忆化

宝藏 Minimax 使用 `lru_cache` 缓存已经计算过的状态，避免重复计算相同的玩家位置、剩余宝藏、累计得分和当前回合。

### 4. Alpha-Beta 剪枝

Alpha-Beta 使用 `alpha` 和 `beta` 两个边界排除不可能影响最终结果的分支。

综合题的 `treasure_alpha_beta` 支持 `order_moves=True`。启用后，算法按照当前玩家获取宝藏的即时收益从高到低访问子节点，使较好的候选值更早更新 `alpha` 或 `beta`，从而增加剪枝机会。

| 深度 | 原始顺序 | 启发式排序 | 减少比例 |
|---|---:|---:|---:|
| H=2 | 13 | 11 | 15.4% |
| H=4 | 49 | 39 | 20.4% |

节点排序不改变最优结果：H=2 仍选择 T2、收益差为 -1；H=4 仍选择 T3、收益差为 3。

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

## 自动化测试

运行全部测试：

    python -m unittest test_solution.py -v

当前共有 11 个测试用例，覆盖：

- 迷宫 A* 路径搜索
- 迷宫无解情况
- 加权地形 A*
- 加权地图无解情况
- Minimax 与 Alpha-Beta 正确性
- 宝藏博弈 H=2、H=4 与节点排序
- 6×6 宝藏距离矩阵
- 宝藏全部不可达情况
- A* 启发函数性能统计
- 二叉树反转
- Alpha-Beta 访问顺序

预期结果：

    Ran 11 tests
    OK

## 测试覆盖率

执行：

    python -m coverage run -m unittest test_solution.py
    python -m coverage report -m

当前测试结果：

    solution.py 覆盖率为 91%
    项目整体覆盖率为 92%

剩余未覆盖部分主要是演示入口、异常分支和少量不影响核心算法正确性的代码。

## 运行时间基准测试

执行：

    python benchmark.py

基准测试包含：

- A* 使用 `h=0` 时的运行时间和节点数量
- A* 使用曼哈顿距离时的运行时间和节点数量
- Minimax 的运行时间和访问节点数
- Alpha-Beta 的运行时间和访问节点数
- 大规模博弈树的访问顺序对比

由于测试规模较小，运行时间会受到系统调度和计时精度影响，因此主要使用节点访问数量评价算法效率。

## 运行完整实验

执行：

    python run_experiment.py

保存实验结果：

    python run_experiment.py | Tee-Object experiment_results.txt

## 一键验证

执行：

    powershell -ExecutionPolicy Bypass -File .\verify.ps1

该脚本依次执行：

1. Python 文件语法检查
2. 11 个自动化测试
3. 完整实验运行
4. 输出验证通过提示

## 生成实验报告 PDF

执行：

    python make_pdf.py

检查 PDF 页数：

    python -c "from pypdf import PdfReader; print(len(PdfReader('实验报告.pdf').pages))"

实验报告控制在 5 页以内。

## 生成提交压缩包

    Compress-Archive -Path solution.py,run_experiment.py,test_solution.py,benchmark.py,make_report.py,make_pdf.py,verify.ps1,实验报告.md,实验报告.pdf,experiment_results.txt -DestinationPath 实验二提交.zip -Force

最终压缩包包括：

    solution.py
    run_experiment.py
    test_solution.py
    benchmark.py
    make_report.py
    make_pdf.py
    verify.ps1
    实验报告.md
    实验报告.pdf
    experiment_results.txt

## GitHub Actions

项目使用 GitHub Actions 自动执行：

- Python 语法检查
- 依赖安装
- 11 个单元测试
- coverage 覆盖率统计
- 覆盖率报告保存

工作流文件：

    .github/workflows/tests.yml

每次向 GitHub 推送代码或创建 Pull Request 时，工作流都会自动运行。

## 最终验证

    python -m py_compile solution.py
    python -m py_compile run_experiment.py
    python -m py_compile test_solution.py
    python -m py_compile benchmark.py
    python -m py_compile make_report.py
    python -m py_compile make_pdf.py

    python -m unittest test_solution.py -v

    python -m coverage run -m unittest test_solution.py
    python -m coverage report -m

    python run_experiment.py
    python benchmark.py
