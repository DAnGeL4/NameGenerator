###START ImportBlock
##systemImport
import typing as typ
import mongoengine as medb

##customImport
from configs.CFGNames import ME_SETTINGS
from configs.CFGNames import CHECKSUM_DB_GLOBAL_FLAG
from tests.test_Service import FunctionalClass

from modules.nameReader import ChecksumTools, NamesTools

from database.medbCheckSumSchemas import GlobalFlags
from database.medbCheckSumSchemas import ChecksumFiles

from database.medbNameSchemas import Race, GenderGroups
from database.medbNameSchemas import Male, Female, Surnames

###FINISH ImportBlock

###START GlobalConstantBlock
###FINISH GlobalConstantBlock

###START DecoratorBlock
###FINISH DecoratorBlock


###START FunctionalBlock
class FileTools_Test(FunctionalClass):
    pass


class ChecksumTools_Test(FunctionalClass):
    '''
    Testing next methods of class #ChecksumTools:
    getOldCheckSumDB;
    setGlobalChecksumFlag;
    writeCheckSumDB;
    '''

    ##BEGIN ConstantBlock
    mdb_alias = ME_SETTINGS.MDB_n_Aliases['mdbCheckSum']['alias']
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

        #Using mongomock for testing
        medb.connect('mongoenginetest', 
                host='mongomock://localhost', 
                alias=cls.mdb_alias)

    @classmethod
    def tearDownClass(cls) -> typ.NoReturn:
        '''Tear down for class.'''
        medb.disconnect(alias=cls.mdb_alias)

        cls.removeTestFiles()
        cls.printTearDownClassMsg()

    def setUp(self) -> typ.NoReturn:
        '''Set up for test.'''
        self.printSetUpMethodMsg()
        
        existFlag = GlobalFlags()
        existFlag.globalExist = True
        existFlag.save()

        checksumFile = ChecksumFiles()
        checksumFile.file = 'DBNames_Test_Data'
        checksumFile.checksum = 'f8ecbed43362ae6ecf00726de6ae17ea'
        checksumFile.save()

    def tearDown(self) -> typ.NoReturn:
        '''Tear down for test.'''
        GlobalFlags.drop_collection()
        ChecksumFiles.drop_collection()

        self.printTearDownMethodMsg()

    ##END PrepareBlock
    @FunctionalClass.descript
    def test_getOldCheckSumDB_readDataFile_expectedRightData(
            self) -> typ.NoReturn:
        '''
        Testing the method of gets checksum database from db file.
        '''
        #Checksum database writed in setUp methods
        res: typ.Dict = ChecksumTools.getOldCheckSumDB(
            usingFileStoringFlag=False)

        self.assertDictEqual(res, {'DBNames_Test_Data': 
                                        'f8ecbed43362ae6ecf00726de6ae17ea',
                                   'globalExist': True})
    
    @FunctionalClass.descript
    def test_setGlobalChecksumFlag_writeDataFile_expectedTrueAnsw(
            self) -> typ.NoReturn:
        '''
        Testing the method of gets checksum database from db file.
        '''
        #Checksum database writed in setUp methods
        res: typ.Dict = ChecksumTools.setGlobalChecksumFlag(
            value=False,
            usingFileStoringFlag=False)

        self.assertTrue(res)
        
    @FunctionalClass.descript
    def test_setGlobalChecksumFlag_readDataFile_expectedFalseFlag(
            self) -> typ.NoReturn:
        '''
        Testing the method of gets checksum database from db file.
        '''
        #Checksum database writed in setUp methods
        _ = ChecksumTools.setGlobalChecksumFlag(
            value=False,
            usingFileStoringFlag=False)

        obj = GlobalFlags.objects.first()
        res = obj.globalExist

        self.assertFalse(res)

    @FunctionalClass.descript
    def test_writeCheckSumDB_writeChecksumDataToFile_expectedTrueAnsw(
            self) -> typ.NoReturn:
        '''
        Testing the answer of the method of writes database (dict) to database file.
        '''
        checkSumData: dict = dict({
            'DBNames_Test_Data':
            'f8ecbed43362ae6ecf00726de6ae17ea',
            CHECKSUM_DB_GLOBAL_FLAG:
            True
        })

        res: bool = ChecksumTools.writeCheckSumDB(
            checkSumData,
            usingFileStoringFlag=False)
        self.assertListEqual(res, ["Checksun db writed in mongoDB."])

    @FunctionalClass.descript
    def test_writeCheckSumDB_checkingWritedData_expectedEqualData(
            self) -> typ.NoReturn:
        '''
        Testing the data written to a checksum database file.
        '''
        #Write expected data in mongo database
        checkSumData: dict = dict({
            'DBNames_Test_Data':
            'f8ecbed43362ae6ecf00726de6ae17ea',
            CHECKSUM_DB_GLOBAL_FLAG:
            True
        })

        _ = ChecksumTools.writeCheckSumDB(
                checkSumData,
                usingFileStoringFlag=False)

        obj = GlobalFlags.objects.first()
        res = dict({CHECKSUM_DB_GLOBAL_FLAG: obj.globalExist})

        obj = ChecksumFiles.objects.first()
        res.update({obj.file: obj.checksum})

        self.assertDictEqual(res, dict({'DBNames_Test_Data': 
                                            'f8ecbed43362ae6ecf00726de6ae17ea',
                                        'globalExist': True}))


class NamesTools_Test(FunctionalClass):
    '''
    Testing next methods of class #NamesTools:

    eraseNamesBase;
    createNamesDB.
    '''

    ##BEGIN ConstantBlock
    mdb_alias = ME_SETTINGS.MDB_n_Aliases['mdbName']['alias']
    mdb_checksum_alias = ME_SETTINGS.MDB_n_Aliases['mdbCheckSum']['alias']
    TestFiles = {
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

        #Using mongomock for testing
        medb.connect('mongoenginetest', 
                host='mongomock://localhost', 
                alias=cls.mdb_alias)
        medb.connect('mongoenginetest2', 
                host='mongomock://localhost', 
                alias=cls.mdb_checksum_alias)

    @classmethod
    def tearDownClass(cls) -> typ.NoReturn:
        '''Tear down for class.'''
        medb.disconnect(alias=cls.mdb_alias)
        medb.disconnect(alias=cls.mdb_checksum_alias)

        cls.removeTestFiles()
        cls.printTearDownClassMsg()

    def setUp(self) -> typ.NoReturn:
        '''Set up for test.'''
        self.printSetUpMethodMsg()
        
        existFlag = GlobalFlags()
        existFlag.globalExist = True
        existFlag.save()

        race = Race()
        race.race = 'TestRace'
        race.save()

    def tearDown(self) -> typ.NoReturn:
        '''Tear down for test.'''
        GlobalFlags.drop_collection()
        ChecksumFiles.drop_collection()

        Race.drop_collection()
        GenderGroups.drop_collection()
        Male.drop_collection()
        Female.drop_collection()
        Surnames.drop_collection()

        self.printTearDownMethodMsg()

    ##END PrepareBlock
    @FunctionalClass.descript
    def test_eraseNamesBase_erasingMongoDB_expectedRightAnswer(
            self) -> typ.NoReturn:
        '''
        Testing the method of erases database file.
        '''
        res: typ.Dict = NamesTools.eraseNamesBase(self.mdb_alias)

        self.assertEqual(res, "INF: Target Mongo db erased. Recreated empty.")
    
    @FunctionalClass.descript
    def test_eraseNamesBase_erasingMongoDB_expectedErasedFile(
            self) -> typ.NoReturn:
        '''
        Testing the method of erases database file.
        '''
        _ = NamesTools.eraseNamesBase(self.mdb_alias)
        
        countRaceObjs = len(Race.objects())
        countGenderObjs = len(GenderGroups.objects())
        countMaleObjs = len(Male.objects())
        countFemaleObjs = len(Female.objects())
        countSurnamesObjs = len(Surnames.objects())
        res = tuple((countRaceObjs, countGenderObjs, countMaleObjs,
                     countFemaleObjs, countSurnamesObjs))

        self.assertTupleEqual(res, (0, 0, 0, 0, 0))
    
    @FunctionalClass.descript
    def test_eraseNamesBase_changingExistFlag_ME_expectedExistFalse(
            self) -> typ.NoReturn:
        '''
        Testing the method of erases database file.
        '''
        _ = NamesTools.eraseNamesBase(self.mdb_alias)

        obj = GlobalFlags.objects.first()
        res = obj.globalExist

        self.assertFalse(res)

    @FunctionalClass.descript
    def test_createNamesDB_creatingDatabaseInMongo_expectedCorrectResponse(
            self) -> typ.NoReturn:
        '''
        Testing the method creating Database of names and writing in DB file with verification of checksum.

        Testing a correct responce.
        '''
        obj = GlobalFlags.objects.first()
        obj.globalExist = False
        obj.save()
        
        res: str = NamesTools.createNamesDB(directory="tests/tmp/", dataBaseOfNames={})

        self.assertEqual(res, ('\nNamesDB: Created', 
                                ["Names inserted in mongoDB."]))

    @FunctionalClass.descript
    def test_createNamesDB_creatingDatabaseInMongo_expectedCorrectWritedData(
            self) -> typ.NoReturn:
        '''
        Testing the method creating Database of names and writing in DB file with verification of checksum.

        Testing a correct writed data in DB file.
        '''
        obj = GlobalFlags.objects.first()
        obj.globalExist = False
        obj.save()

        _ = NamesTools.createNamesDB(directory="tests/tmp/", dataBaseOfNames={})
        objs = Surnames.objects()
        res = [obj.name for obj in objs]

        self.assertListEqual(res, ['testName1', 'testName2', 'testName3'])

    @FunctionalClass.descript
    def test_createNamesDB_creatingDatabaseInMongo_expectedCorrectChecksumData(
            self) -> typ.NoReturn:
        '''
        Testing the method creating Database of names and writing in DB file with verification of checksum.

        Testing a correct writed data in DB file.
        '''
        obj = GlobalFlags.objects.first()
        obj.globalExist = False
        obj.save()
        
        _ = NamesTools.createNamesDB(directory="tests/tmp/", dataBaseOfNames={})

        res = dict()

        obj = GlobalFlags.objects.first()
        res.update({CHECKSUM_DB_GLOBAL_FLAG: obj.globalExist})
        
        obj = ChecksumFiles.objects.first()
        res.update({obj.file: obj.checksum})

        self.assertDictEqual(res,  {'DBNames_testRace_Surnames': 
                                        'd94f4e322384ae967806cb0ef649ad57', 
                                    'globalExist': False})

###FINISH FunctionalBlock

###START MainBlock
def main() -> typ.NoReturn:
    pass
###FINISH Mainblock
