###START ImportBlock
##systemImport
import unittest
import os
import functools
import typing
import pickle

##customImport

###FINISH ImportBlock

###START GlobalConstantBlock
###FINISH GlobalConstantBlock

###START DecoratorBlock
###FINISH DecoratorBlock


###START FunctionalBlock
class FunctionalClass(unittest.TestCase):
    '''
    Add-in class, adding base functional for the test clases.
    '''
    TestConstruction = None
    TestFileDirectory = "tests/tmp/"
    TestFiles = dict()

    def descript(descriptedFunc: typing.Callable) -> typing.Callable:
        '''
        Descriptes a function in output.
        '''

        @functools.wraps(descriptedFunc)
        def wrapper(*args):
            self = args[0]
            print("* Description: \n|\t%s" % self.shortDescription())
            descriptedFunc(*args)

        return wrapper


    @classmethod
    def printSetUpClassMsg(cls) -> typing.NoReturn:
        '''Prints message for set up class.'''
        print("==============================")
        print("** SetUpClass: %s" % cls.__name__)
        print("==============================\n")


    @classmethod
    def printTearDownClassMsg(cls) -> typing.NoReturn:
        '''Prints message for tear down class.'''
        print("==============================")
        print("*** TearDownClass: %s" % cls.__name__)
        print("==============================\n")


    def printSetUpMethodMsg(self) -> typing.NoReturn:
        '''Prints message for set up method.'''
        print("-------------------------------")
        print("* Set up for:\n|\t" + str(self._testMethodName))


    def printTearDownMethodMsg(self) -> typing.NoReturn:
        '''Prints message for tear down method.'''
        print("* Tear down for:\n|\t" + str(self._testMethodName))
        print("-------------------------------\n")


    @classmethod
    def createTestFiles(cls):
        '''
        Creates test files from #TestFiles.
        '''
        for fileName, data in cls.TestFiles.items():
            fullPathTestFile = str(cls.TestFileDirectory + fileName)

            with open(fullPathTestFile, 'tw', encoding='utf-8') as test_file:
                test_file.write(str(data))
                test_file.close()


    @classmethod
    def removeTestFiles(cls):
        '''
        Remove test files from #TestFiles.
        '''

        for fileName in cls.TestFiles:
            fullPathTestFile = str(cls.TestFileDirectory + fileName)

            with open(fullPathTestFile, 'tw', encoding='utf-8') as test_file:
                try:
                    os.remove(fullPathTestFile)
                except:
                    print("* Error: \n | File %s doesn't exist." %
                          str(fullPathTestFile))
                          
    def deepCopy(self, data: typing.Dict[str, dict]) -> typing.Dict[str, dict]:
        '''
        Deep copy uses pickle module.
        '''
        _tmpDump = pickle.dumps(data, -1)
        data = pickle.loads(_tmpDump)
        return data

    def leaveKeys(self, allowedKeys: list, 
                    data: typing.Dict[str, dict]) -> typing.Dict[str, dict]:
        '''
        Leaves only allowed keys and delete other from #NamesAnalyticData.
        '''
        keys = list(data.keys())
        for key in keys:
            if key not in allowedKeys:
                del data[key]
        return data

    def deleteKeys(self, keys: list, 
                    data: typing.Dict[str, dict]) -> typing.Dict[str, dict]:
        '''
        Deletes keys from NamesAnalyticData by the #keys list.
        '''
        for key in keys:
            if key in data:
                del data[key]
        return data

###FINISH FunctionalBlock

###START MainBlock
def main() -> typing.NoReturn:
    pass
###FINISH Mainblock