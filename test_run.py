import unittest

from Tests.testUI import TestMainWaysCheck, TestWithoutBD

# run selected tests
suite = unittest.TestSuite()
suite.addTest(TestMainWaysCheck("testOTPExpress"))
runner = unittest.TextTestRunner()
runner.run(suite)

# if __name__ == '__main__':  # uncomment to run all tests
#     unittest.main()
