###START ImportBlock
##systemImport
import ast
import os
import hashlib
import copy
import functools
import typing
from typing import Union
from pathlib import Path as PathType
from contextlib import redirect_stdout

##customImport
from configs.CFGNames import DB_NAMES_DIRECTORY
from configs.CFGNames import NAMES_BASE_INITIALIZE_FILE, CHECK_SUM_FILE
from configs.CFGNames import DB_NAMES_FILENAME_FLAG, CHECKSUM_DB_GLOBAL_FLAG
from configs.CFGNames import LOCAL_NAMES_LOG_FILE
from configs.CFGNames import USING_FILE_STORING_FLAG
from templates.templateAnalysis import TEMPLATE_LOCAL_RACE, TEMPLATE_GLOBAL_RACE

from database.dbtest import ME_DBService

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
        logFilePath = LOCAL_NAMES_LOG_FILE
        
        with open(logFilePath, 'w') as f, redirect_stdout(f):
            print("---NAMEREADER-STARTED---\n")
            res = redirectedFunction(*args, **kwargs)
            print("\n---NAMEREADER-FINISHED---")

        return res

    return wrapper
###FINISH DecoratorBlock


###START FunctionalBlock
class FileWork:
    '''
    Class #FileWork groups methods to works with files (find, sort, read, write, owerwrite etc.). 
    
    For work with class don't need class instance.
    '''

    @staticmethod
    def readFile(fileName: Union[str, PathType]) -> Union[list, None]:
        '''
        Reads data from the file (#fileName) and formats the data 
        into a list of lines.
        '''

        try:
            with open(fileName, 'r') as fileObject:
                listOfLines = [str(name).strip('\n') for name in fileObject]

            return listOfLines

        except:
            return None

    @staticmethod
    def readDataFile(
            fileName: Union[str, PathType] = NAMES_BASE_INITIALIZE_FILE
    ) -> dict:
        '''
        Reads data (dictionary type) from the datafile (#fileName).
        Default #fileName - NAMES_BASE_INITIALIZE_FILE
        '''

        try:
            data = open(fileName).read()

            if data:
                data = ast.literal_eval(data)

            return dict(data)

        except:
            return dict({})

    @staticmethod
    def overwriteDataFile(
            data: dict,
            fileName: Union[str, PathType] = NAMES_BASE_INITIALIZE_FILE
    ) -> bool:
        '''
        Erase and owerwrite new data (dictionary type) in datafile(#fileName). 
        Default #fileName - NAMES_BASE_INITIALIZE_FILE
        '''

        #Case of incorrect data
        if data is None or type(data) is not dict:
            return False

        try:
            with open(fileName, 'w') as dataFile:
                dataFile.write(str(data))

            return True

        except:
            return False

    @staticmethod
    def getFileNameFromPath(
            path: Union[str, PathType]) -> Union[str, PathType]:
        '''
        Extracts file name from full path.
        '''

        fileName = path.split("/")[-1]
        #last one is the file name  ^

        return fileName

    @staticmethod
    def findDBNamesFiles(**kwargs) -> typing.List[PathType]:
        '''
        Finds all files, excluding folders, in directory (default directory is #DB_NAMES_DIRECTORY).

        !!!This method is potentially vulnerable.
        '''
        directory = DB_NAMES_DIRECTORY

        #begin_test_case_block
        if 'directory' in kwargs:
            directory = kwargs['directory']
        #end_test_case_block

        dbDirFiles = [
            os.path.join(directory, fileName)
            for fileName in os.listdir(directory)
        ]

        dbDirFiles = [
            fileName for fileName in dbDirFiles if os.path.isfile(fileName)
        ]

        return dbDirFiles

    @classmethod
    def findValidDBNamesFiles(cls, **kwargs) -> typing.List[PathType]:
        '''
        Checks for a flag in the file names from list. Return list of files path's with a flag.
        
        Flag it's #DB_NAMES_FILENAME_FLAG. Default directory is #DB_NAMES_DIRECTORY.
        '''

        validFiles = []
        dbDirFiles = cls.findDBNamesFiles(**kwargs)

        for fullPath in dbDirFiles:
            fileName = cls.getFileNameFromPath(fullPath)
            tmp_FileWords = fileName.split("_")
            tmp_FileNameFlag = tmp_FileWords[0]

            if tmp_FileNameFlag == DB_NAMES_FILENAME_FLAG:
                validFiles.append(fullPath)

        return validFiles


class CheckSumWork:
    '''
    Class CheckSumWork contains methods to works wits checksum (calculate, check, createDB, write). Checksum based on md5 hash.
    '''

    @staticmethod
    def calculateCheckSum(
            fullPath: Union[str, PathType] = None,
            data: Union[str, typing.ByteString] = None) -> typing.Hashable:
        '''
        Calculates md5 hash of file or data.
        '''

        checkSum = ''

        if fullPath:
            data = open(fullPath, 'rb').read()

        if data:
            data = data.strip()
            if hasattr(data, 'encode'):
                data = data.encode()

            checkSum = hashlib.md5(data).hexdigest()

        return checkSum

    @staticmethod
    def getOldCheckSumDB(checkSumDBFile: Union[str, PathType], **kwargs
                         ) -> typing.Dict[str, Union[typing.Hashable, bool]]:
        '''
        Gets checksum database from file if #USING_FILE_STORING_FLAG true,
        else gets from mongoDB.
        '''

        #begin_test_case_block
        usingFileStoringFlag = USING_FILE_STORING_FLAG
        if 'usingFileStoringFlag' in kwargs:
            usingFileStoringFlag = kwargs['usingFileStoringFlag']
        #end_test_case_block

        oldCheckSumDB = None
        if usingFileStoringFlag:
            oldCheckSumDB = FileWork.readDataFile(checkSumDBFile)
        else:
            tool = ME_DBService()
            oldCheckSumDB = tool.readChecksumDB_ME()
        
        if not oldCheckSumDB:
            oldCheckSumDB = {}
        
        return oldCheckSumDB

    @classmethod
    def createFileCheckSum(cls, fullPath: Union[str, PathType]
                           ) -> typing.Tuple[PathType, typing.Hashable]:
        '''
        Creates check sum for the file from path.
        '''

        checkSum = cls.calculateCheckSum(fullPath)
        fileName = FileWork.getFileNameFromPath(fullPath)

        return fileName, checkSum

    @classmethod
    def createCheckSumDB(cls, checkSumDBFile: Union[str, PathType] = CHECK_SUM_FILE,
                         **kwargs
                         ) -> typing.Dict[str, Union[typing.Hashable, bool]]:
        '''
        Creates a checksum DB from #DBNames files.
        '''
        checkSumDB = cls.getOldCheckSumDB(checkSumDBFile, **kwargs)
        dbNamesFiles = FileWork.findValidDBNamesFiles(**kwargs)

        for fullPath in dbNamesFiles:
            fileName, checkSum = cls.createFileCheckSum(fullPath)
            checkSumDB[fileName] = checkSum

        checkSumDB[CHECKSUM_DB_GLOBAL_FLAG] = True

        return checkSumDB

    @classmethod
    def writeCheckSumDB(cls,
            checkSumDB: typing.Dict[str, typing.Hashable] = None,
            checkSumDBFile: Union[str, PathType] = CHECK_SUM_FILE,
            **kwargs) -> bool:
        '''
        Writes a checksum DB in specified file.
        '''

        #begin_test_case_block
        usingFileStoringFlag = USING_FILE_STORING_FLAG
        if 'usingFileStoringFlag' in kwargs:
            usingFileStoringFlag = kwargs['usingFileStoringFlag']

        if 'checkSumDBFile' in kwargs:
            checkSumDBFile = kwargs.pop('checkSumDBFile')
        #end_test_case_block

        if not checkSumDB:
            checkSumDB = cls.createCheckSumDB(checkSumDBFile, **kwargs)

        if usingFileStoringFlag:
            answer: bool = FileWork.overwriteDataFile(checkSumDB, checkSumDBFile)
        else:
            tool = ME_DBService()
            answer: bool = tool.writeChecksumDB_ME(checkSumDB)

        return answer

    @classmethod
    def checkValidHash(cls, fileNamePath: Union[str, PathType] = None,
                       **kwargs) -> bool:
        '''
        Compares DB of all files checksums from file and recently calculated. If #fileNamePath defined then include file name in check sum database and compare.
        '''
        checkSumDBFile = CHECK_SUM_FILE

        #begin_test_case_block
        if 'checkSumDBFile' in kwargs:
            checkSumDBFile = kwargs.pop('checkSumDBFile')
        #end_test_case_block
        
        oldCheckSumDB = cls.getOldCheckSumDB(checkSumDBFile, **kwargs)
        curCheckSumDB = cls.createCheckSumDB(checkSumDBFile, **kwargs)

        if fileNamePath:
            fileName, checkSum = cls.createFileCheckSum(fileNamePath)
            curCheckSumDB[fileName] = checkSum

        return oldCheckSumDB == curCheckSumDB


class WithNamesWork:
    '''
    Class #WithNamesWork contains methods to prepare #DBNames files (files with lists of names) to paste in DB. 
    '''

    @staticmethod
    def prepareLocalRaceTemplate(raceName: str) -> typing.Dict:
        '''
        Prepares a local race template replacing #tmp_race to #raceName.
        '''

        tmp_Race = copy.deepcopy(TEMPLATE_LOCAL_RACE)
        tmp_Race[raceName] = tmp_Race.pop('tmp_Race')

        return dict(tmp_Race)

    @staticmethod
    def makeRaceList(races: typing.List[dict]) -> typing.List:
        '''
        Makes a list of race names.
        '''

        raceList = list()

        for race in races:
            key = list(race.keys())[0]  #only first key
            raceList.append(key)

        return list(raceList)

    @staticmethod
    def getRaceAndKeyFormFileNamePath(
            fullPath: Union[str, PathType]) -> typing.Tuple[str, str]:
        '''
        Gets the name of the race and the name of the key from the file name in the full path and returns it.
        '''

        fileName = FileWork.getFileNameFromPath(fullPath)

        tmp_NameWords = fileName.split("_")
        raceName = tmp_NameWords[1]  #e.g. Elf, Ork, e.t.c
        keyName = tmp_NameWords[2]  #e.g. Male, Female e.t.c

        return raceName, keyName

    @classmethod
    def prepareGlobalRaceTemplate(cls, dataBaseOfNames: typing.Dict[str, dict],
                                  raceName: str) -> typing.Dict[str, dict]:
        '''
        Prepares a global race template. Inserts #TEMPLATE_GLOBAL_RACE if database of names is empty.
        '''

        if dataBaseOfNames is None:
            dataBaseOfNames = FileWork.readDataFile()

        if len(dataBaseOfNames.keys()) == 0:
            dataBaseOfNames = copy.deepcopy(TEMPLATE_GLOBAL_RACE)

        raceList = cls.makeRaceList(dataBaseOfNames["Races"])
        if raceName not in raceList:
            tmp_emptyRace = dict({raceName: {}})
            dataBaseOfNames["Races"].append(tmp_emptyRace)

        return dict(dataBaseOfNames)

    @classmethod
    def insertNames(cls, keyName: str, raceNameDict: typing.Dict[str, dict],
                    listOfNames: list) -> str:
        '''
        Selected insert of key in dictionary.

        #keyName have value "Male", "Female" or "Surnames"
        '''

        state = "Done"

        #Case of first initialize
        if not raceNameDict:
            tmpRace = cls.prepareLocalRaceTemplate('tmp')
            raceNameDict.update(tmpRace['tmp'])

        if keyName in raceNameDict:
            raceNameDict[keyName] = list(listOfNames)

        elif keyName in raceNameDict["Genders"]:
            raceNameDict["Genders"][keyName]["Names"] = list(listOfNames)

        else:
            state = "Failure"

        return state

    @classmethod
    def formatNames(cls,
            fullPath: Union[str, PathType],
            dataBaseOfNames: typing.Dict[str, dict]) -> typing.Dict[str, dict]:
        '''
        Creates and formats the database of data to be inserted into the DB file.
        '''

        listOfNames = FileWork.readFile(fullPath)
        raceName, keyName = cls.getRaceAndKeyFormFileNamePath(
            fullPath)
        dataBaseOfNames = cls.prepareGlobalRaceTemplate(
            dataBaseOfNames, raceName)

        for race in dataBaseOfNames["Races"]:
            if raceName in list(race.keys()):
                cls.insertNames(keyName, race[raceName], listOfNames)

        return dict(dataBaseOfNames)

    @classmethod
    def createNamesDB(cls, **kwargs):
        '''
        Formates DB of names, writes to file and updates a checksum DB.
        '''
        dataBaseOfNames = None
        initializeFile = NAMES_BASE_INITIALIZE_FILE

        if CheckSumWork.checkValidHash(**kwargs):
            return "\nNamesDB: Canceled", "INF: Checksum exists"

        #begin_test_case_block
        usingFileStoringFlag = USING_FILE_STORING_FLAG
        if 'usingFileStoringFlag' in kwargs:
            usingFileStoringFlag = kwargs['usingFileStoringFlag']

        if 'initializeFile' in kwargs:
            initializeFile = kwargs['initializeFile']

        if 'dataBaseOfNames' in kwargs:
            dataBaseOfNames = kwargs.pop('dataBaseOfNames')
        #end_test_case_block

        dbNamesFiles = FileWork.findValidDBNamesFiles(**kwargs)

        for fullPath in dbNamesFiles:
            dataBaseOfNames = cls.formatNames(
                fullPath, dataBaseOfNames)

        answers = 'Empty answer.'
        if usingFileStoringFlag:
            answ = FileWork.overwriteDataFile(dataBaseOfNames, initializeFile)
            if not answ:
                answers = "ERR: Can't write data to file."
                return "\nNamesDB: Failed", answers
            answers = "INF: db file created, mongodb skipped."
            
        else:
            tool = ME_DBService()
            answers = tool.insertNames(dataBaseOfNames)
            
        
        #FileWork.overwriteDataFile(dataBaseOfNames, initializeFile)
        #CheckSumWork.writeCheckSumDB(**kwargs)

        return "\nNamesDB: Created", answers

###FINISH FunctionalBlock


###START MainBlock
@redirectOutput
def printResponds(responds):
    '''
    Function for printing responds in log file.
    '''
    if responds is list:
        for res in responds:
            print(res)
    else:
        print(responds)

def main():
    globRresp, locResp = WithNamesWork.createNamesDB()
    printResponds(locResp)
    
    return globRresp
###FINISH Mainblock
