import snakemethods
import helper
import unittest

class TestSnakeMethodsFunctions(unittest.TestCase):
    def test_nextBestMove(self):
        # TEST 1
        board1 = [[0, 0, 0, 0, 0, 0],
                 [0, 2, 0, 0, 3, 0],
                 [0, 1, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0]]

        board1_1 = [[0, 0, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0, 0],
                 [0, 2, 0, 0, 3, 0]]

        board1_2 = [[3, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0],
                    [2, 1, 1, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0]]
        
        board1_3 = [[0, 0, 0, 0, 0],
                    [0, 0, 3, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 1, 1, 1, 2],
                    [0, 0, 0, 0, 0]]

        board2 = [[0, 0, 0, 0, 0, 0],
                 [0, 1, 0, 0, 3, 0],
                 [0, 1, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0, 0],
                 [0, 1, 2, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0]]
        
        board3 = [[0, 0, 1, 0, 0, 0],
                 [0, 2, 1, 0, 3, 0],
                 [0, 1, 1, 0, 0, 0],
                 [0, 1, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0]]

        board4 = [[0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0],
                 [3, 0, 0, 0, 0, 0],
                 [0, 0, 0, 1, 1, 2]]

        board5 = [[0, 0, 0, 2, 0, 0],
                 [0, 0, 0, 1, 0, 0],
                 [0, 0, 0, 1, 0, 0],
                 [0, 0, 0, 1, 0, 0],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 3, 0, 0]]

        board6 = [[2, 1, 1, 0, 0, 0],
                 [1, 1, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 3, 0],
                 [0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0]]
        
        board7 = [[0, 3, 0, 0],
                  [0, 0, 0, 0],
                  [0, 2, 0, 0],
                  [0, 1, 0, 0]]
        

        # BAD BOARDS -----------------
        board20 = [[
            [1, 0, 1],
            [2, 3, 0],
            [1, 0, 1]
        ]]

        board21 = [[
            [1, 0, 0],
            [1, 2, 0],
            [0, 0, 0]
        ]]
        

        test_cases = [
            ("Simple right path", board1, helper.vector(1, 0)),
            ("Simple against bottom wall", board1_1, helper.vector(1, 0)),
            ("Simple against left wall", board1_2, helper.vector(0, 1)),
            ("Against right wall", board1_3, helper.vector(0, 1)),
            ("Open Space, two possible options", board2, [helper.vector(1, 0), helper.vector(0, 1)]),
            ("Tail blocking path", board3, helper.vector(-1, 0)),
            ("In corner", board4, helper.vector(0, 1)),
            ("apple behind tail", board5, [helper.vector(1, 0), helper.vector(-1, 0)]),
            ("guaranteed death", board6, [helper.vector(0, 1), helper.vector(0, -1), helper.vector(1, 0), helper.vector(-1, 0)]),
            ("Simple up path, 2-long snake", board7, (0, 1)),
            ("discombobulated snake", board20, None),
            ("no apple", board21, None)
        ]

        for label, board, expectedValue in test_cases:
            with self.subTest(label=label):
                if isinstance(expectedValue, list):
                    self.assertIn(snakemethods.nextBestMove(board), expectedValue)
                else:
                    self.assertEqual(snakemethods.nextBestMove(board), expectedValue)
        
        
if __name__ == "__main__":
    unittest.main()