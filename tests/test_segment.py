import unittest
import main
import helper

class TestSegment(unittest.TestCase):
    def test_segmentMoving(self):
        # Initialize game state
        game_state = main.GameState(600, 600)
        
        # Deep copy grid positions of all segments before movement
        before_positions = [(seg.gridX, seg.gridY) for seg in game_state.snake]
        directions = [(seg.direction.x, seg.direction.y) for seg in game_state.snake]

        # Move the snake
        main.moveBodySegments(game_state)

        # After movement, each segment should have moved 1 unit in its direction
        for i, seg in enumerate(game_state.snake):
            expected_x = before_positions[i][0] + directions[i][0]
            expected_y = before_positions[i][1] + directions[i][1]
            self.assertEqual((seg.gridX, seg.gridY), (expected_x, expected_y), 
                             msg=f"Segment {i} did not move correctly.")

if __name__ == "__main__":
    unittest.main()
