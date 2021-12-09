###START ImportBlock
import unittest
import typing
import sys
import functools
from contextlib import redirect_stdout

from configs.CFGNames import GLOBAL_TEST_LOG_FILE

from tests import test_nameReader
from tests import test_nameAnalysis
###FINISH ImportBlock

###START GlobalConstantBlock
###FINISH GlobalConstantBlock

###START DecoratorBlock

def redirectOutput(redirectedFunction: typing.Callable) -> typing.Callable:
    '''
    Redirects output to log file for #redirectedFunction. After returns stdout back.
    '''
    @functools.wraps(redirectedFunction)
    def wrapper(*args, **kwargs):
        logFilePath = GLOBAL_TEST_LOG_FILE
        
        with open(logFilePath, 'w') as f, redirect_stdout(f):
            print("---TEST-STARTED---\n")
            res = redirectedFunction(*args, **kwargs)
            print("\n---TEST-FINISHED---")

        return res

    return wrapper
    
###FINISH DecoratorBlock

###START FunctionalBlock
def createTestSuites() -> unittest.suite.TestSuite:
    '''
    Makes and returns TestSuite object.
    '''    

    testLoad = unittest.TestLoader()
    suites = unittest.TestSuite()

    tests = testLoad.loadTestsFromModule(test_nameReader)
    suites.addTests(tests)
    
    tests = testLoad.loadTestsFromModule(test_nameAnalysis)
    suites.addTests(tests)
    
    return suites
###FINISH FunctionalBlock

###START MainBlock
@redirectOutput
def main() -> str:
    runner = unittest.TextTestRunner()
    testSuites = createTestSuites()
    
    runner.run(testSuites)

    return "\nTests Module: Done"
###FINISH Mainblock