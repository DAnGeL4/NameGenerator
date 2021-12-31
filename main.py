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
class MainService():
    '''
    Contains a tools for main function.
    '''
    def eraseMongoDBs(self) -> typ.NoReturn:
        '''
        Erases target mongo databases by aliases.
        '''
        mdbNAliases = ME_SETTINGS.MDB_n_Aliases
        
        mdbAliases = list([
            mdbNAliases['mdbName']['alias'],
            mdbNAliases['mdbAnalytic']['alias']
        ])

        for mdbAlias in mdbAliases:
            res = nameReader.NamesTools.eraseNamesBase(mdb=mdbAlias)
            print(res)

    def makeMainFunctionsList(self) -> typ.List[typ.Callable]:
        '''
        Makes runable functions list from main functions of all modules.
        '''
        functionsList = list([
            nameReader.main,
            nameAnalysis.main,
            nameGen.main,
        ])

        return functionsList

    def runMainFunctionsList(self) -> typ.List[str]:
        '''
        Runs the list of main functions from other modules.
        Returns list of responds.
        '''
        responds = list()
        functionsList = self.makeMainFunctionsList()

        for function in functionsList:
            respond = function()
            responds.append(respond)

        return responds

    @redirectOutput
    def runUnittests(self) -> typ.NoReturn:
        '''
        Runs the module with unittests.
        '''
        if MAKE_UNITTESTS_FLAG:
            res = test_Common.main()
            print(res)

    @redirectOutput
    def globalRun(self) -> typ.NoReturn:
        '''
        This is the base function.
        '''    
        if ERASE_NAME_BASE_INIT_FLAG:
            if USING_FILE_STORING_FLAG:
                res = nameReader.NamesTools.eraseNamesBase()
                print(res)
            else:
                self.eraseMongoDBs()

        responds = self.runMainFunctionsList()
        for respond in responds:
            print(respond)
###FINISH FunctionalBlock

###START MainBlock
def main() -> typ.NoReturn:
    '''
    Main function.
    Uses profiling if #MAKE_PROFILING_FLAG is true.
    '''
    tools = None
    service = MainService()

    errors = list(["WARNING", "WRONG"])
    if checkDependencies() in errors:
        return

    if not USING_FILE_STORING_FLAG:
        tools = dbTools.MongoDBTools()
        _ = tools.registerDataBases()

    if not MAKE_PROFILING_FLAG:
        service.globalRun()

    else:
        #!Not work yet. Too old version of graphviz(0.16) package
        #Hope updates soon :)
        Profiling.makeProfileNGraph('MainService().globalRun')

    if tools:
        tools.unregisterDataBases()

    service.runUnittests()


    ##TESTED_AREA_BEGIN
    print("\n#BEGIN TEST CODE...\n")

    #from modules import tst
    #tst.main()

    print("\n#...END TEST CODE")
    ##TESTED_AREA_END
    return


###FINISH Mainblock

###START RunBlock
main()
###FINISH RunBlock  