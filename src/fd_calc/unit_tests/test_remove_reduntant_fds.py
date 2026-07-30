import unittest

from fd_calc import FDCalc, FD

class TestRemoveRedundantFDs(unittest.TestCase):
    def setUp(self):
        self.fdCalc = FDCalc()

    
    def test_remove_basic(self):
        print("test_remove_basic")
        test_fds = [FD(("a"), ("b"), False), FD(("a", "c"), ("b"), False)]
        expected = [FD(("a"), ("b"), False)]
        self.fdCalc.result = test_fds
        self.fdCalc.remove_redundant_fds()
        for fd in self.fdCalc.result:
            found = False
            for fd2 in expected:
                if fd.left_side == fd2.left_side and fd.right_side == fd2.right_side:
                    #print(fd.left_side, fd2.left_side)
                    found = True
                    break
            if not found:
                raise Exception(f"Couldnt find {fd.to_string()}")

        for fd in expected:
            found = False
            for fd2 in self.fdCalc.result:
                if fd.left_side == fd2.left_side and fd.right_side == fd2.right_side:
                    #print(fd.left_side, fd2.left_side)
                    found = True
                    break
            if not found:
                raise Exception(f"Couldnt find {fd.to_string()}")
    
    def test_remove_basic_2(self):
        print("test_remove_basic_2")
        test_fds = [FD(("a"), ("b"), False), FD(("c"), ("d"), False), FD(("a", "c"), ("d", "b"), False)]
        expected = [FD(("a"), ("b"), False), FD(("c"), ("d"), False)]
        self.fdCalc.result = test_fds
        self.fdCalc.remove_redundant_fds()
        for fd in self.fdCalc.result:
            found = False
            for fd2 in expected:
                if fd.left_side == fd2.left_side and fd.right_side == fd2.right_side:
                    #print(fd.left_side, fd2.left_side)
                    found = True
                    break
            if not found:
                raise Exception(f"Couldnt find {fd.to_string()}")

        for fd in expected:
            found = False
            for fd2 in self.fdCalc.result:
                if fd.left_side == fd2.left_side and fd.right_side == fd2.right_side:
                    #print(fd.left_side, fd2.left_side)
                    found = True
                    break
            if not found:
                raise Exception(f"Couldnt find {fd.to_string()}")

    def test_remove_basic_3(self):
        print("test_remove_basic_3")
        test_fds = [FD(("a"), ("b", "c"), False), FD(("d"), ("b"), False), FD(("a", "d"), ("b", "c"), False)]
        expected = [FD(("a"), ("b", "c"), False), FD(("d"), ("b"), False), FD(("a", "d"), ("b", "c"), False)]
        self.fdCalc.result = test_fds
        self.fdCalc.remove_redundant_fds()
        for fd in self.fdCalc.result:
            found = False
            for fd2 in expected:
                if fd.left_side == fd2.left_side and fd.right_side == fd2.right_side:
                        #print(fd.left_side, fd2.left_side)
                    found = True
                    break
            if not found:
                raise Exception(f"Couldnt find {fd.to_string()}")

        for fd in expected:
            found = False
            for fd2 in self.fdCalc.result:
                if fd.left_side == fd2.left_side and fd.right_side == fd2.right_side:
                    #print(fd.left_side, fd2.left_side)
                    found = True
                    break
            if not found:
                raise Exception(f"Couldnt find {fd.to_string()}")

if __name__ == '__main__':
    unittest.main()