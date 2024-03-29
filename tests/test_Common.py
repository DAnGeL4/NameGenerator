###START ImportBlock
import unittest
import typing as typ
import functools
from contextlib import redirect_stdout

from configs.CFGNames import GLOBAL_TEST_LOG_FILE

from tests import test_nameReader
from tests import test_nameReader_MongoDB
from tests import test_nameAnalysis
from tests import test_nameAnalysis_MongoDB 
from tests import test_dbTools_MongoDB
from tests import test_nameGen
from tests import test_nameGen_MongoDB
###FINISH ImportBlock

###START GlobalConstantBlock
###FINISH GlobalConstantBlock

###START DecoratorBlock

def redirectOutput(redirectedFunction: typ.Callable) -> typ.Callable:
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
    tests = testLoad.loadTestsFromModule(test_nameReader_MongoDB)
    suites.addTests(tests)
    
    tests = testLoad.loadTestsFromModule(test_nameAnalysis)
    suites.addTests(tests)
    tests = testLoad.loadTestsFromModule(test_nameAnalysis_MongoDB)
    suites.addTests(tests)
    
    tests = testLoad.loadTestsFromModule(test_dbTools_MongoDB)
    suites.addTests(tests)
    
    tests = testLoad.loadTestsFromModule(test_nameGen)
    suites.addTests(tests)
    tests = testLoad.loadTestsFromModule(test_nameGen_MongoDB)
    suites.addTests(tests)
    
    return suites
###FINISH FunctionalBlock

###START MainBlock
@redirectOutput
def main() -> str:
    runner = unittest.TextTestRunner()
    testSuites = createTestSuites()
    
    runner.run(testSuites)

    return "Tests Module: Done"
###FINISH Mainblock