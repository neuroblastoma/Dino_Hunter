import unittest
import TestEntities

def suite():
    """
        Create a test suite.
    """
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestEntities.TestEntity))
    test_suite.addTest(unittest.makeSuite(TestEntities.TestEnemy))
    test_suite.addTest(unittest.makeSuite(TestEntities.TestTRex))
    test_suite.addTest(unittest.makeSuite(TestEntities.TestRaptor))
    test_suite.addTest(unittest.makeSuite(TestEntities.TestPtero))
    test_suite.addTest(unittest.makeSuite(TestEntities.TestPlayer))
    return test_suite


mySuite = suite()

runner = unittest.TextTestRunner()
runner.run(mySuite)
