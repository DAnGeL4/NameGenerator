###START ImportBlock
##ident                                                                                              |
##systemImport
import typing as typ
import functools
from contextlib import redirect_stdout

#import cython as cthn      #

#import pandas as pand      #
#import dask                #

##customImport
from configs.CFGNames import GLOBAL_LOG_FILE
from configs.CFGNames import ERASE_NAME_BASE_INIT_FLAG
from configs.CFGNames import MAKE_PROFILING_FLAG
from configs.CFGNames import MAKE_UNITTESTS_FLAG 
from configs.CFGNames import USING_FILE_STORING_FLAG
from configs.CFGNames import ME_SETTINGS

from modules import nameGen
from modules import nameReader
from modules import nameAnalysis
from modules import dbTools

from tests import test_Common

from diagnostic.modules.diagnostics import Profiling, checkDependencies
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
def makeMainFunctionsList() -> typ.List[typ.Callable]:
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

def runMainFunctionsList() -> typ.List[str]:
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

@redirectOutput
def globalRun() -> typ.NoReturn:
    '''
    This is the base function.
    '''    
    if ERASE_NAME_BASE_INIT_FLAG:
        mdbNAliases = ME_SETTINGS.MDB_n_Aliases
        
        mdbAliases = list([
            mdbNAliases['mdbName']['alias'],
            mdbNAliases['mdbAnalytic']['alias']
        ])

        for mdbAlias in mdbAliases:
            res = nameReader.NamesTools.eraseNamesBase(mdb=mdbAlias)
            print(res)

    responds = runMainFunctionsList()
    for respond in responds:
        print(respond)
###FINISH FunctionalBlock

###START MainBlock
def main() -> typ.NoReturn:
    '''
    Main function.
    Uses profiling if #MAKE_PROFILING_FLAG is true.
    '''
    errors = list(["WARNING", "WRONG"])
    if checkDependencies() in errors:
        return

    if not USING_FILE_STORING_FLAG:
        tools = dbTools.MongoDBTools()
        _ = tools.registerDataBases()

    if not MAKE_PROFILING_FLAG:
        globalRun()

    else:
        #!Not work yet. Too old version of graphviz(0.16) package
        #Hope updates soon :)
        Profiling.makeProfileNGraph('globalRun')


    ##TESTED_AREA_BEGIN
    print("\n#BEGIN TEST CODE...\n")
    
    dbTools.main()

    print("\n#...END TEST CODE")
    ##TESTED_AREA_END
    
    return


###FINISH Mainblock

###START RunBlock
main()
###FINISH RunBlock  