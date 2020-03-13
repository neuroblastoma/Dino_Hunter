import unittest
# import TestFIFO
# import TestStack
# import TestUtilities
import TestEntities

def suite():
    """
        Create a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestEntities.TestEntity))
    test_suite.addTest(unittest.makeSuite(TestEntities.TestEnemy))
    test_suite.addTest(unittest.makeSuite(TestEntities.TestTRex))
    return test_suite


mySuite = suite()

runner = unittest.TextTestRunner()
runner.run(mySuite)
