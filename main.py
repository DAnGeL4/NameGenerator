###START ImportBlock
##ident                                                                                              |
##systemImport
import typing
import functools
import subprocess
from contextlib import redirect_stdout

#import cython as cthn      #
#import numba               #not_working

#import pandas as pand      #
#import dask                #
#import pyspark             #not_working #not need yet

##customImport
from configs.CFGNames import GLOBAL_LOG_FILE
from configs.CFGNames import ERASE_NAME_BASE_INIT_FLAG
from configs.CFGNames import MAKE_PROFILING_FLAG
from configs.CFGNames import MAKE_UNITTESTS_FLAG 
from configs.CFGNames import USING_FILE_STORING_FLAG

from modules import nameGen
from modules import nameReader
from modules import nameAnalysis
from modules.diagnostics import Profiling

from database import dbtest

from tests import test_Common
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
        print("START...")
        logFilePath = GLOBAL_LOG_FILE
        
        with open(logFilePath, 'w') as f, redirect_stdout(f):
            print("---STARTED---\n")
            res = redirectedFunction(*args, **kwargs)
            print("\n---FINISHED---")
        
        print("...FINISH")

        return res

    return wrapper
###FINISH DecoratorBlock

###START FunctionalBlock
def eraseNamesBaseInitializeFile() -> typing.Text:
    '''
    Erases database of names and checksum. After this initializes default values.
    '''
    nameReader.FileWork.overwriteDataFile({})
    checkSumDB = nameReader.CheckSumWork.createCheckSumDB()
    checkSumDB[nameReader.CHECKSUM_DB_GLOBAL_FLAG] = False
    nameReader.CheckSumWork.writeCheckSumDB(checkSumDB)
    return "Main: DB erased"
    

def makeMainFunctionsList() -> typing.List[typing.Callable]:
    '''
    Makes runable functions list from main functions of all modules.
    '''
    functionsList = list([
        nameGen.main,
        nameReader.main,
        nameAnalysis.main,
    ])

    if MAKE_UNITTESTS_FLAG:
        functionsList.append(
            test_Common.main,
        )

    return functionsList


def runMainFunctionsList() -> typing.List[str]:
    '''
    Runs the list of main functions from other modules.
    Returns list of responds.
    '''
    responds = list()
    functionsList = makeMainFunctionsList()

    for function in functionsList:
        respond = function()
        responds.append(respond)

    return responds


def checkDependencies():
    '''
    Checking the dependencies and external ip for atlas mongodb.
    '''
    print("\n")

    setUpFile = "./bashscripts/setup.sh"
    returnValues = subprocess.check_output([setUpFile])
    returnValues = returnValues.decode('utf-8')

    answers = returnValues.split('\n')
    for answer in answers:
        print(answer)

    answerFlag = answers[-2].split(' ')[0]
    return answerFlag

###FINISH FunctionalBlock

###START MainBlock
@redirectOutput
def globalRun() -> typing.NoReturn:
    '''
    This is the base function.
    '''    
    if ERASE_NAME_BASE_INIT_FLAG:

        if not USING_FILE_STORING_FLAG:
            res = eraseNamesBaseInitializeFile()
            print(res)
        else:
            tools = dbtest.MongoDBWork()
            res = tools.eraseME_DB('mdbName')
            print(res)

    responds = runMainFunctionsList()
    for respond in responds:
        print(respond)

def main() -> typing.NoReturn:
    '''
    Main function.
    Uses profiling if #MAKE_PROFILING_FLAG is true.
    '''
    errors = list(["WARNING", "WRONG"])
    if checkDependencies() in errors:
        return

    if not USING_FILE_STORING_FLAG:
        tools = dbtest.ME_DBService()
        _ = tools.registerDataBases()

    if not MAKE_PROFILING_FLAG:
        globalRun()

    else:
        #!Not work yet. Too old version of graphviz(0.16) package
        #Hope updates soon :)
        Profiling.makeProfileNGraph('globalRun')


    ##TESTED_AREA_BEGIN
    print("\n#BEGIN TEST CODE...\n")
    
    dbtest.main()

    print("\n#...END TEST CODE")
    ##TESTED_AREA_END
    
    return


###FINISH Mainblock

###START RunBlock
main()
###FINISH RunBlock  