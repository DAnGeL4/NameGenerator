###START ImportBlock
##systemImport
import os
import typing as typ
import functools
import cProfile
import pydot
import time
import subprocess

##customImport
from configs.CFGNames import GLOBAL_PROFILE_FILE, GLOBAL_PROFILE_DOT_FILE 
from configs.CFGNames import GLOBAL_GRAPH_FILE, MAKE_UNITTESTS_FLAG
###FINISH ImportBlock

###START GlobalConstantBlock

#####START TemplateBlock
#####FINISH TemplateBlock

###FINISH GlobalConstantBlock

###START DecoratorBlock
def timeMe(method: typ.Callable) -> typ.Callable:
    '''Counts run time.'''
    @functools.wraps(method)
    def wrapper(*args, **kw):
        #startTime = int(round(time.time() * 1000))
        startTime = time.time() * 1000
        result = method(*args, **kw)
        #endTime = int(round(time.time() * 1000))
        endTime = time.time() * 1000

        print(endTime - startTime,'ms')
        return result

    return wrapper
###FINISH DecoratorBlock

###START FunctionalBlock
class Timer:   
    '''Counts run time with operator "with".'''

    def __init__(self, message: str = '') -> typ.NoReturn:
        self.message = message

    def _printTime(self) -> typ.NoReturn:
        print(self.message)
        print('Run time %s ms.' % self.interval)

    def __enter__(self) -> object:
        #self.startTime = int(round(time.time() * 1000))
        self.startTime = time.time() * 1000
        return self

    def __exit__(self, *args) -> typ.NoReturn:
        #self.endTime = int(round(time.time() * 1000))
        self.endTime = time.time() * 1000
        self.interval = self.endTime - self.startTime

        self._printTime()


class Profiling:    
    '''Diagnostics with profiling.'''

    @staticmethod
    def getFileName(globalFileName: str) -> str:
        '''
        Makes correct file name if tests run.
        '''
        if MAKE_UNITTESTS_FLAG:
            fullFileName = str(globalFileName)
            testsFlag = '-test'

            fileName = fullFileName.split('.')[0]
            fileExtension = fullFileName.split('.')[1]

            fileName = str(fileName) + str(testsFlag)
            fullFileName = str(fileName) + str(fileExtension)

            return fullFileName

        else:
            return globalFileName

    @classmethod
    def makeProfileNGraph(cls, generalFunction: str) -> typ.NoReturn:
        '''
        Makes profiling and create call tree graph (with other data).
        '''
        profileFile = cls.getFileName(GLOBAL_PROFILE_FILE)
        profileDotFile = cls.getFileName(GLOBAL_PROFILE_DOT_FILE)
        graphFile = cls.getFileName(GLOBAL_GRAPH_FILE)

        cProfile.run(''+ generalFunction +'()', profileFile)
        os.system('gprof2dot -f pstats ' + profileFile + 
                                    ' > ' + profileDotFile)

        (graph,) = pydot.graph_from_dot_file(profileDotFile)
        graph.write_png(graphFile)


def checkDependencies() -> typ.NoReturn:
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
###FINISH Mainblock