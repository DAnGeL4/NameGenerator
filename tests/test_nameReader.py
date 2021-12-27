###START ImportBlock
##systemImport
import os
import typing as typ

##customImport
from tests.test_Service import FunctionalClass
from modules.nameReader import FileTools, ChecksumTools, NamesTools

###FINISH ImportBlock

###START GlobalConstantBlock
###FINISH GlobalConstantBlock

###START DecoratorBlock
###FINISH DecoratorBlock


###START FunctionalBlock
class FileTools_Test(FunctionalClass):
    '''
    Testing next methods of class #FileTools:
    readFile;
    readDataFile;
    overwriteDataFile;
    getFileNameFromPath;
    findDBNamesFiles;
    findValidDBNamesFiles.
    '''

    ##BEGIN ConstantBlock
    TestFiles = {
        'DBNames_Test_Data': dict({
            'test_key': 'test_data'
        }),
        'TMP_Test_Data': dict({
            'test_key': 'test_data'
        })
    }
    ##END ConstantBlock

    ##BEGIN PrepareBlock
    @classmethod
    def setUpClass(cls) -> typ.NoReturn:
        '''Set up for class.'''

        cls.printSetUpClassMsg()
        cls.createTestFiles()

    @classmethod
    def tearDownClass(cls) -> typ.NoReturn:
        '''Tear down for class.'''

        cls.removeTestFiles()
        cls.printTearDownClassMsg()

    def setUp(self) -> typ.NoReturn:
        '''Set up for test.'''

        self.printSetUpMethodMsg()

    def tearDown(self) -> typ.NoReturn:
        '''Tear down for test.'''

        self.printTearDownMethodMsg()

    ##END PrepareBlock

    @FunctionalClass.descript
    def test_readFile_checkingReadedData_expectedListOfLines(
            self) -> typ.NoReturn:
        '''
        Testing read data from file.
        '''

        #Must be list of lines without last symbol in each line
        res = FileTools.readFile(
            str(self.TestFileDirectory + 'DBNames_Test_Data'))
        self.assertEqual(res, ["{'test_key': 'test_data'}"])

    @FunctionalClass.descript
    def test_readDataFile_checkingReadedData_expectedDictData(
            self) -> typ.NoReturn:
        '''
        Testing read dictionary data from file.
        '''

        res = FileTools.readDataFile(
            str(self.TestFileDirectory + 'DBNames_Test_Data'))
        self.assertDictEqual(res, {'test_key': 'test_data'})

    @FunctionalClass.descript
    def test_overwriteDataFile_checkingReturn_expectedTrue(
            self) -> typ.NoReturn:
        '''
        Testing writing to file method.
        '''

        res = FileTools.overwriteDataFile(
            self.TestFiles['DBNames_Test_Data'],
            fileName=str(self.TestFileDirectory + 'DBNames_Test_Data'))

        self.assertTrue(res)

    @FunctionalClass.descript
    def test_overwriteDataFile_checkingWritedData_expectedEqualData(
            self) -> typ.NoReturn:
        '''
        Testing data written to a file.
        '''

        FileTools.overwriteDataFile(
            dict({
                'test_key': 'test_data'
            }),
            fileName=str(self.TestFileDirectory + 'DBNames_Test_Data'))

        res: dict = FileTools.readDataFile(
            str(self.TestFileDirectory + 'DBNames_Test_Data'))
        self.assertDictEqual(res, {'test_key': 'test_data'})

    @FunctionalClass.descript
    def test_getFileNameFromPath_splitPath_expectedFileName(
            self) -> typ.NoReturn:
        '''
        Testing getting filename from full path.
        '''

        res = FileTools.getFileNameFromPath("tests/tmp/DBNames_Test_Data")
        self.assertEqual(res, "DBNames_Test_Data")

    @FunctionalClass.descript
    def test_findDBNamesFiles_findAllFilesInDirectory_expectedListOfAllFiles(
            self) -> typ.NoReturn:
        '''
        Testing the method of finding files in a folder.
        '''

        res = FileTools.findDBNamesFiles(directory="tests/tmp/")
        #sort the list of files alphabetically
        res = sorted(res, key=lambda x: os.path.splitext(x)[0])

        self.assertListEqual(
            res, ['tests/tmp/.gitkeep', "tests/tmp/DBNames_Test_Data", 
                    "tests/tmp/TMP_Test_Data"])

    @FunctionalClass.descript
    def test_findValidDBNamesFiles_findFilesWithDBNames_expectedListOfDBNamesFiles(
            self) -> typ.NoReturn:
        '''
        Testing the method of finding valid (with flag DB_NAMES_FILENAME_FLAG = "DBNames") files in a folder.
        '''

        res = FileTools.findValidDBNamesFiles(directory="tests/tmp/")
        self.assertListEqual(res, ["tests/tmp/DBNames_Test_Data"])


class ChecksumTools_Test(FunctionalClass):
    '''
    Testing next methods of class #ChecksumTools:
    calculateCheckSum;
    
    getOldCheckSumDB;
    setGlobalChecksumFlag;

    createFileCheckSum;
    createCheckSumDB;
    writeCheckSumDB;
    checkValidHash.
    '''

    ##BEGIN ConstantBlock
    TestFiles = {
        'CheckSumDB.cfg': dict({}),
        'DBNames_Test_Data': dict({
            'test_key': 'test_data'
        }),
        'TMP_Test_Data': dict({
            'test_key': 'test_data'
        })
    }
    ##END ConstantBlock

    ##BEGIN PrepareBlock
    @classmethod
    def setUpClass(cls) -> typ.NoReturn:
        '''Set up for class.'''

        cls.printSetUpClassMsg()
        cls.createTestFiles()

    @classmethod
    def tearDownClass(cls) -> typ.NoReturn:
        '''Tear down for class.'''

        cls.removeTestFiles()
        cls.printTearDownClassMsg()

    def setUp(self) -> typ.NoReturn:
        '''Set up for test.'''

        self.printSetUpMethodMsg()

    def tearDown(self) -> typ.NoReturn:
        '''Tear down for test.'''

        self.printTearDownMethodMsg()

    ##END PrepareBlock

    @FunctionalClass.descript
    def test_calculateCheckSum_calcDataMD5_expectedMD5Hash(
            self) -> typ.NoReturn:
        '''
        Testing the method for calculating md5 hash from data.
        '''

        res: typ.Hashable = ChecksumTools.calculateCheckSum(
            data="Some testing data")
        self.assertEqual(res, 'b5ec912b4a44962563c97b37817757af')

    @FunctionalClass.descript
    def test_calculateCheckSum_calcFileMD5_expectedMD5Hash(
            self) -> typ.NoReturn:
        '''
        Testing the method for calculating md5 hash for data from file.
        '''

        res: typ.Hashable = ChecksumTools.calculateCheckSum(
            str(self.TestFileDirectory + 'TMP_Test_Data'))
        self.assertEqual(res, 'f8ecbed43362ae6ecf00726de6ae17ea')

    @FunctionalClass.descript
    def test_createFileCheckSum_makeMD5ForFile_expectedFilenameAndMD5(
            self) -> typ.NoReturn:
        '''
        Testing the method for preparing file checksum to write in database.
        '''

        res: typ.Tuple = ChecksumTools.createFileCheckSum(
            str(self.TestFileDirectory + 'TMP_Test_Data'))
        self.assertTupleEqual(
            res, tuple(('TMP_Test_Data', 'f8ecbed43362ae6ecf00726de6ae17ea')))

    @FunctionalClass.descript
    def test_createCheckSumDB_makeDictDataOfDirectoryFiles_expectedDictData(
            self) -> typ.NoReturn:
        '''
        Testing the method of creates database (dict) for DB_NAMES_FILENAME_FLAG files in directory.
        '''

        res: typ.Dict = ChecksumTools.createCheckSumDB(
            checkSumDBFile=str(self.TestFileDirectory + 'CheckSumDB.cfg'),
            directory="tests/tmp/",
            usingFileStoringFlag=True)
        self.assertDictEqual(
            res,
            dict({
                'DBNames_Test_Data': 'f8ecbed43362ae6ecf00726de6ae17ea',
                'globalExist': True
            }))

    @FunctionalClass.descript
    def test_writeCheckSumDB_writeChecksumDataToFile_expectedTrueAnsw(
            self) -> typ.NoReturn:
        '''
        Testing the answer of the method of writes database (dict) to database file.
        '''

        checkSumData: dict = dict({
            'DBNames_Test_Data':
            'f8ecbed43362ae6ecf00726de6ae17ea',
            'globalExist':
            True
        })

        res: bool = ChecksumTools.writeCheckSumDB(
            checkSumData,
            checkSumDBFile=str(self.TestFileDirectory + 'CheckSumDB.cfg'),
            usingFileStoringFlag=True)
        self.assertTrue(res)

    @FunctionalClass.descript
    def test_writeCheckSumDB_checkingWritedData_expectedEqualData(
            self) -> typ.NoReturn:
        '''
        Testing the data written to a checksum database file.
        '''

        #Write expected data to database file
        checkSumData: dict = dict({
            'DBNames_Test_Data':
            'f8ecbed43362ae6ecf00726de6ae17ea',
            'globalExist':
            True
        })
        ChecksumTools.writeCheckSumDB(
            checkSumData,
            checkSumDBFile=str(self.TestFileDirectory + 'CheckSumDB.cfg'),
            usingFileStoringFlag=True)

        res: dict = FileTools.readDataFile(
            str(self.TestFileDirectory + 'CheckSumDB.cfg'))
        self.assertDictEqual(
            res,
            dict({
                'DBNames_Test_Data': 'f8ecbed43362ae6ecf00726de6ae17ea',
                'globalExist': True
            }))

    @FunctionalClass.descript
    def test_checkValidHash_compareCurrentHashWithOld_expectedTrue(
            self) -> typ.NoReturn:
        '''
        Testing the method comparing checksum from file and recently calculated.
        '''

        #Write expected data to database file
        checkSumData: dict = dict({
            'DBNames_Test_Data':
            'f8ecbed43362ae6ecf00726de6ae17ea',
            'globalExist':
            True
        })
        ChecksumTools.writeCheckSumDB(
            checkSumData,
            checkSumDBFile=str(self.TestFileDirectory + 'CheckSumDB.cfg'),
            usingFileStoringFlag=True)

        #Comparing checksum value of #DBNames_Test_Data file with value from database
        res: bool = ChecksumTools.checkValidHash(
            fileNamePath=str(self.TestFileDirectory + 'DBNames_Test_Data'),
            checkSumDBFile=str(self.TestFileDirectory + 'CheckSumDB.cfg'),
            directory="tests/tmp/",
            usingFileStoringFlag=True)
        self.assertTrue(res)


class NamesTools_Test(FunctionalClass):
    '''
    Testing next methods of class #NamesTools:

    eraseNamesBase;
    
    prepareLocalRaceTemplate;
    makeRaceList;
    getRaceAndKeyFromFileNamePath;
    prepareGlobalRaceTemplate;
    insertNames;
    getRaceAndKeyFormFileName;
    formatNames;
    createNamesDB.
    '''

    ##BEGIN ConstantBlock
    TestFiles = {
        'CheckSumDB.cfg':
        dict({
            'DBNames_testRace_Surnames': 'f979b7abfe5c503d10c2945d1212842e',
            'GLOB_EXIST': True
        }),
        'DBNames_testRace_Surnames':
        'testName1\ntestName2\ntestName3\n',
        'InitializeFile.cfg':
        dict({})
    }
    ##END ConstantBlock

    ##BEGIN PrepareBlock
    @classmethod
    def setUpClass(cls) -> typ.NoReturn:
        '''Set up for class.'''

        cls.printSetUpClassMsg()
        cls.createTestFiles()

    @classmethod
    def tearDownClass(cls) -> typ.NoReturn:
        '''Tear down for class.'''

        cls.removeTestFiles()
        cls.printTearDownClassMsg()

    def setUp(self) -> typ.NoReturn:
        '''Set up for test.'''

        self.printSetUpMethodMsg()

    def tearDown(self) -> typ.NoReturn:
        '''Tear down for test.'''

        self.printTearDownMethodMsg()

    ##END PrepareBlock

    @FunctionalClass.descript
    def test_prepareLocalRaceTemplate_insertRaceInTemplate_expectedPreparingTemplate(
            self) -> typ.NoReturn:
        '''
        Testing the method of inserts the race key into template.
        '''

        res: typ.Dict = NamesTools.prepareLocalRaceTemplate('testedRace')
        self.assertDictEqual(
            res, {
                "testedRace": {
                    "Genders": {
                        "Female": {
                            "Names": [],
                        },
                        "Male": {
                            "Names": []
                        }
                    },
                    "Surnames": []
                }
            })

    @FunctionalClass.descript
    def test_makeRaceList_gettingRaceKeyFromDict_expectedListOfRaces(
            self) -> typ.NoReturn:
        '''
        Testing the method of getting a list race names from dictionary database.
        '''

        res: typ.List = NamesTools.makeRaceList(
            list([{
                'testedRace1': {}
            }, {
                'testedRace2': {}
            }]))
        self.assertListEqual(res, list(['testedRace1', 'testedRace2']))

    @FunctionalClass.descript
    def test_prepareGlobalRaceTemplate_preparingDataWithTemplates_expectedPreparedData(
            self) -> typ.NoReturn:
        '''
        Testing the method of preparing the global race template.
        '''

        res: dict = NamesTools.prepareGlobalRaceTemplate({}, "testedRace")
        self.assertDictEqual(res, {"Races": [{"testedRace": {}}]})

    @FunctionalClass.descript
    def test_insertNames_insertingFemale_expectedCorrectReturnsValue(
            self) -> str:
        '''
        Testing the method of inserting list of names in race data dictionary by a key.

        Testing case: 
        1. inserting in 'Female' key 
        2. returned value.
        '''

        raceNameDict = {
            'Genders': {
                'Female': {
                    'Names': []
                },
                'Male': {
                    'Names': []
                }
            },
            'Surnames': []
        }

        res: str = NamesTools.insertNames("Female", raceNameDict,
                                             ['tmp_1', 'tmp_2', 'tmp_3'])
        self.assertEqual(res, 'Done')

    @FunctionalClass.descript
    def test_insertNames_insertingMaleWithEmptyRaceDict_expectedPreparedAndFilledData(
            self) -> str:
        '''
        Testing the method of inserting list of names in race data dictionary by a key.

        Testing case: 
        1. inserting in 'Male' key 
        2. preapering empty dictionary.
        '''

        raceNameDict = {}

        res: str = NamesTools.insertNames("Male", raceNameDict,
                                             ['tmp_1', 'tmp_2', 'tmp_3'])
        self.assertDictEqual(
            raceNameDict, {
                'Genders': {
                    'Female': {
                        'Names': []
                    },
                    'Male': {
                        'Names': ['tmp_1', 'tmp_2', 'tmp_3']
                    }
                },
                'Surnames': []
            })

    @FunctionalClass.descript
    def test_insertNames_insertingSurnames_expectedFilledData(self) -> str:
        '''
        Testing the method of inserting list of names in race data dictionary by a key.

        Testing case: 
        1. inserting in 'Surnames' key 
        2. inserting in prepared dictionary.
        '''

        raceNameDict = {
            'Genders': {
                'Female': {
                    'Names': []
                },
                'Male': {
                    'Names': []
                }
            },
            'Surnames': []
        }

        res: str = NamesTools.insertNames("Surnames", raceNameDict,
                                             ['tmp_1', 'tmp_2', 'tmp_3'])
        self.assertDictEqual(
            raceNameDict, {
                'Genders': {
                    'Female': {
                        'Names': []
                    },
                    'Male': {
                        'Names': []
                    }
                },
                'Surnames': ['tmp_1', 'tmp_2', 'tmp_3']
            })

    @FunctionalClass.descript
    def test_getRaceAndKeyFromFileName_gettingsKeysFromFilename_expectedCorrectKeys(
            self) -> typ.NoReturn:
        '''
        Testing the method of gettings race key and gender/surname key from full path of file.
        '''

        res: typ.Tuple[str,
                          str] = NamesTools.getRaceAndKeyFromFileNamePath(
                              "./DBTest/DBNames_TestRace_TestGender")
        self.assertTupleEqual(res, ('TestRace', 'TestGender'))

    @FunctionalClass.descript
    def test_formatNames_preparingDataForEmptyDatabaseVar_expectedPreparedAndFilledData(
            self) -> typ.NoReturn:
        '''
        Testing the method of creates and formats the data for database.

        Initial database variable is empty.
        '''
        res: typ.Dict[str, dict] = NamesTools.formatNames(
            str(self.TestFileDirectory + 'DBNames_testRace_Surnames'), {})
        self.assertDictEqual(
            res, {
                'Races': [{
                    'testRace': {
                        'Genders': {
                            'Female': {
                                'Names': []
                            },
                            'Male': {
                                'Names': []
                            }
                        },
                        'Surnames': ['testName1', 'testName2', 'testName3']
                    }
                }]
            })

    @FunctionalClass.descript
    def test_formatNames_preparingDataForFilledDatabaseVar_expectedPreparedAndFilledData(
            self) -> typ.NoReturn:
        '''
        Testing the method of creates and formats the data for database.

        Initial database variable is filled according to the template with the changed race key.
        '''
        res: typ.Dict[str, dict] = NamesTools.formatNames(
            str(self.TestFileDirectory + 'DBNames_testRace_Surnames'), {
                'Races': [{
                    'testRace': {
                        'Genders': {
                            'Female': {
                                'Names': []
                            },
                            'Male': {
                                'Names': []
                            }
                        },
                        'Surnames': []
                    }
                }]
            })
        self.assertDictEqual(
            res, {
                'Races': [{
                    'testRace': {
                        'Genders': {
                            'Female': {
                                'Names': []
                            },
                            'Male': {
                                'Names': []
                            }
                        },
                        'Surnames': ['testName1', 'testName2', 'testName3']
                    }
                }]
            })

    @FunctionalClass.descript
    def test_createNamesDB_creatingDatabase_expectedCorrectResponse(
            self) -> typ.NoReturn:
        '''
        Testing the method creating Database of names and writing in DB file with verification of checksum.

        Testing a correct responce.
        '''

        res: str = NamesTools.createNamesDB(
            checkSumDBFile=str(self.TestFileDirectory + 'CheckSumDB.cfg'),
            initializeFile=str(self.TestFileDirectory + 'InitializeFile.cfg'),
            directory="tests/tmp/",
            dataBaseOfNames={},
            usingFileStoringFlag=True)
        self.assertEqual(res, ('\nNamesDB: Created', 
                                'INF: db file created, mongodb skipped.'))

    @FunctionalClass.descript
    def test_createNamesDB_creatingDatabase_expectedCorrectWritedData(
            self) -> typ.NoReturn:
        '''
        Testing the method creating Database of names and writing in DB file with verification of checksum.

        Testing a correct writed data in DB file.
        '''

        res: str = NamesTools.createNamesDB(
            checkSumDBFile=str(self.TestFileDirectory + 'CheckSumDB.cfg'),
            initializeFile=str(self.TestFileDirectory + 'InitializeFile.cfg'),
            directory="tests/tmp/",
            dataBaseOfNames={},
            usingFileStoringFlag=True)

        data: typ.Dict[str, dict] = FileTools.readDataFile(
            str(self.TestFileDirectory + 'InitializeFile.cfg'))

        self.assertDictEqual(
            data, {
                "Races": [{
                    "testRace": {
                        "Genders": {
                            "Female": {
                                "Names": []
                            },
                            "Male": {
                                "Names": []
                            }
                        },
                        "Surnames": ['testName1', 'testName2', 'testName3']
                    }
                }]
            })


###FINISH FunctionalBlock

###START MainBlock
def main() -> typ.NoReturn:
    pass
###FINISH Mainblock
