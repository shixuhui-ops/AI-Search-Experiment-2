import unittest

from solution import (
    astar_path,
    astar_path_stats,
    minimax_stats,
    alpha_beta_stats,
    weighted_astar_cost,
    reverse_tree,
    compare_alpha_beta_order,
    TreeNode,
    minimax,
    alpha_beta,
    treasure_minimax,
    treasure_alpha_beta,
    treasure_distances,
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
        minimax_result_h4 = treasure_minimax(
            distances,
            names,
            values,
            4,
        )

        alpha_beta_result_h4 = treasure_alpha_beta(
            distances,
            names,
            values,
            4,
        )

        self.assertEqual(
            minimax_result_h4,
            {"best_target": "T3", "best_value": 3},
        )

        self.assertEqual(
            alpha_beta_result_h4,
            {"best_target": "T3", "best_value": 3},
        )
        minimax_h4_stats = treasure_minimax(
            distances,
            names,
            values,
            4,
            return_stats=True,
        )

        alpha_beta_h4_stats = treasure_alpha_beta(
            distances,
            names,
            values,
            4,
            return_stats=True,
        )

        self.assertEqual(
            minimax_h4_stats["expanded_states"],
            65,
        )

        self.assertEqual(
            alpha_beta_h4_stats["expanded_states"],
            49,
        )

        self.assertLess(
            alpha_beta_h4_stats["expanded_states"],
            minimax_h4_stats["expanded_states"],
        )
        ordered_alpha_beta_h4 = treasure_alpha_beta(
            distances,
            names,
            values,
            4,
            return_stats=True,
            order_moves=True,
        )

        self.assertEqual(
            ordered_alpha_beta_h4["best_target"],
            "T3",
        )

        self.assertEqual(
            ordered_alpha_beta_h4["best_value"],
            3,
        )

        self.assertEqual(
            ordered_alpha_beta_h4["expanded_states"],
            39,
        )

        self.assertLess(
            ordered_alpha_beta_h4["expanded_states"],
            alpha_beta_h4_stats["expanded_states"],
        )

    def test_treasure_distance_matrix(self):
        grid = [
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

        expected = [
            [0, 12, 10, 4, 8, 8],
            [12, 0, 8, 8, 4, 10],
            [10, 8, 0, 6, 6, 12],
            [4, 8, 6, 0, 6, 6],
            [8, 4, 6, 6, 0, 6],
            [8, 10, 12, 6, 6, 0],
        ]

        self.assertEqual(
            treasure_distances(grid, points),
            expected,
        )
    def test_unreachable_treasure(self):
        distances = [
            [0, 0, -1],
            [0, 0, -1],
            [-1, -1, 0],
        ]

        names = ["A", "B", "T1"]
        values = {"T1": 9}

        expected = {
            "best_target": None,
            "best_value": 0,
        }

        self.assertEqual(
            treasure_minimax(
                distances,
                names,
                values,
                1,
            ),
            expected,
        )

        self.assertEqual(
            treasure_alpha_beta(
                distances,
                names,
                values,
                1,
            ),
            expected,
        )

    def test_search_statistics(self):
        grid = [
            ["S", ".", ".", "X", "."],
            [".", "X", ".", ".", "."],
            [".", "X", ".", "X", "."],
            [".", ".", ".", "X", "E"],
            ["X", "X", ".", ".", "."],
        ]

        path_without_heuristic, nodes_without_heuristic = (
            astar_path_stats(
                (0, 0),
                (3, 4),
                grid,
                False,
            )
        )

        path_with_heuristic, nodes_with_heuristic = (
            astar_path_stats(
                (0, 0),
                (3, 4),
                grid,
                True,
            )
        )

        self.assertEqual(
            path_without_heuristic,
            path_with_heuristic,
        )

        self.assertLessEqual(
            nodes_with_heuristic,
            nodes_without_heuristic,
        )

    def test_weighted_astar_no_solution(self):
        grid = [
            ["S", "X", 1],
            [1, "X", "E"],
        ]

        self.assertEqual(
            weighted_astar_cost((0, 0), (1, 2), grid),
            -1,
        )

    def test_reverse_tree(self):
        root = TreeNode(children=[
            TreeNode(value=1),
            TreeNode(value=2),
        ])

        reversed_root = reverse_tree(root)

        self.assertEqual(
            reversed_root.children[0].value,
            2,
        )

        self.assertEqual(
            reversed_root.children[1].value,
            1,
        )

    def test_alpha_beta_order_comparison(self):
        root = TreeNode(children=[
            TreeNode(children=[
                TreeNode(value=3),
                TreeNode(value=5),
            ]),
            TreeNode(children=[
                TreeNode(value=1),
                TreeNode(value=2),
            ]),
        ])

        result = compare_alpha_beta_order(root)

        self.assertEqual(
            result["normal_order"]["value"],
            result["reversed_order"]["value"],
        )

if __name__ == "__main__":
    unittest.main()