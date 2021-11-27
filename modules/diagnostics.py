###START ImportBlock
##systemImport
import os
import typing
import functools
import cProfile
import pydot
import time

##customImport
from configs.CFGNames import GLOBAL_PROFILE_FILE, GLOBAL_PROFILE_DOT_FILE 
from configs.CFGNames import GLOBAL_GRAPH_FILE
###FINISH ImportBlock

###START GlobalConstantBlock

#####START TemplateBlock
#####FINISH TemplateBlock

###FINISH GlobalConstantBlock

###START DecoratorBlock
def timeMe(method: typing.Callable) -> typing.Callable:
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

    def __init__(self, message: str = '') -> typing.NoReturn:
        self.message = message

    def _printTime(self) -> typing.NoReturn:
        print(self.message)
        print('Run time %s ms.' % self.interval)

    def __enter__(self) -> object:
        #self.startTime = int(round(time.time() * 1000))
        self.startTime = time.time() * 1000
        return self

    def __exit__(self, *args) -> typing.NoReturn:
        #self.endTime = int(round(time.time() * 1000))
        self.endTime = time.time() * 1000
        self.interval = self.endTime - self.startTime

        self._printTime()


class Profiling:    
    '''Diagnostics with profiling.'''

    @staticmethod
    def makeProfileNGraph(generalFunction: str) -> typing.NoReturn:
        '''
        Makes profiling and create call tree graph (with other data).
        '''

        cProfile.run(''+ generalFunction +'()', GLOBAL_PROFILE_FILE)
        os.system('gprof2dot -f pstats ' + GLOBAL_PROFILE_FILE + 
                                    ' > ' + GLOBAL_PROFILE_DOT_FILE)

        (graph,) = pydot.graph_from_dot_file(GLOBAL_PROFILE_DOT_FILE)
        graph.write_png(GLOBAL_GRAPH_FILE)
###FINISH FunctionalBlock

###START MainBlock
###FINISH Mainblock