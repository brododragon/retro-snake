import unittest
import helper

class TestHelperFunctions(unittest.TestCase):
    def test_gridToPixels(self):
        self.assertEqual(helper.gridToPixels(2, 50), 100)
        self.assertEqual(helper.gridToPixels(0, 5), 0)
    
    def test_pixelsToGrid(self):
        self.assertEqual(helper.pixelsToGrid(150, 50), 3)
        self.assertEqual(helper.pixelsToGrid(0, 50), 0)

    def test_gridToPixelsVec(self):
        self.assertEqual(helper.gridToPixelsVec(2, 3, 50), [100, 150])
        self.assertEqual(helper.gridToPixelsVec((2, 3), 50), [100, 150])

    def test_pixelsToGridVec(self):
        self.assertEqual(helper.pixelsToGridVec(100, 150, 50), [2, 3])
        self.assertEqual(helper.pixelsToGridVec((100, 150), 50), [2, 3])

    def test_areOppDirection(self):
        self.assertTrue(helper.areOppDirection(0, 2))
        self.assertFalse(helper.areOppDirection(-1, 3))

if __name__ == '__main__':
    unittest.main()