import unittest

from solution import (
    astar_path,
    weighted_astar_cost,
    TreeNode,
    minimax,
    alpha_beta,
    treasure_minimax,
    treasure_alpha_beta,
)


class TestSearchAlgorithms(unittest.TestCase):

    def test_astar_path(self):
        grid = [
            ["S", ".", ".", "X", "."],
            [".", "X", ".", ".", "."],
            [".", "X", ".", "X", "."],
            [".", ".", ".", "X", "E"],
            ["X", "X", ".", ".", "."],
        ]

        path = astar_path((0, 0), (3, 4), grid)

        self.assertEqual(path[0], (0, 0))
        self.assertEqual(path[-1], (3, 4))
        self.assertEqual(len(path), 8)

    def test_astar_no_solution(self):
        grid = [
            ["S", "X", "E"],
            ["X", "X", "X"],
            [".", ".", "."],
        ]

        self.assertEqual(
            astar_path((0, 0), (0, 2), grid),
            []
        )

    def test_weighted_astar(self):
        grid = [
            ["S", 1, 1, 8, 1],
            [1, 8, 3, 1, 1],
            [1, 8, 1, 8, 1],
            [1, 1, 1, 8, 1],
            [8, 8, 1, 1, "E"],
        ]

        self.assertEqual(
            weighted_astar_cost((0, 0), (4, 4), grid),
            7
        )

    def test_minimax_and_alpha_beta(self):
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

        self.assertEqual(minimax(root), 5)
        self.assertEqual(alpha_beta(root), 5)

    def test_treasure_game(self):
        distances = [
            [0, 12, 10, 4, 8, 8],
            [12, 0, 8, 8, 4, 10],
            [10, 8, 0, 6, 6, 12],
            [4, 8, 6, 0, 6, 6],
            [8, 4, 6, 6, 0, 6],
            [8, 10, 12, 6, 6, 0],
        ]

        names = ["A", "B", "T1", "T2", "T3", "T4"]

        values = {
            "T1": 9,
            "T2": 7,
            "T3": 8,
            "T4": 7,
        }

        minimax_result = treasure_minimax(
            distances,
            names,
            values,
            2,
        )

        alpha_beta_result = treasure_alpha_beta(
            distances,
            names,
            values,
            2,
        )

        self.assertEqual(
            minimax_result,
            {"best_target": "T2", "best_value": -1},
        )

        self.assertEqual(
            alpha_beta_result,
            {"best_target": "T2", "best_value": -1},
        )


if __name__ == "__main__":
    unittest.main()