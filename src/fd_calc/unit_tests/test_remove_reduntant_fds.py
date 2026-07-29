import unittest

from fd_calc import FDCalc, FD

class TestRemoveRedundantFDs(unittest.TestCase):
    def setUp(self):
        self.fdCalc = FDCalc()

    
    def test_remove_basic(self):
        test_fds = [FD(("a"), ("b"), False), FD(("a", "c"), ("b"), False)]
        expected = [FD(("a"), ("b"), False)]
        self.fdCalc.result = test_fds
        self.fdCalc.remove_redundant_fds()
        for fd in self.fdCalc.result:
            for fd2 in expected:
                if fd.left_side == fd2.left_side:
                    #print(fd.left_side, fd2.left_side)
                    self.assertCountEqual(fd.right_side, fd2.right_side)
    
    def test_remove_basic_2(self):
        test_fds = [FD(("a"), ("b"), False), FD(("c"), ("d"), False), FD(("a", "c"), ("d", "b"), False)]
        expected = [FD(("a"), ("b"), False), FD(("c"), ("d"), False)]
        self.fdCalc.result = test_fds
        self.fdCalc.remove_redundant_fds()
        for fd in self.fdCalc.result:
            for fd2 in expected:
                if fd.left_side == fd2.left_side:
                    #print(fd.left_side, fd2.left_side)
                    self.assertCountEqual(fd.right_side, fd2.right_side)

if __name__ == '__main__':
    unittest.main()