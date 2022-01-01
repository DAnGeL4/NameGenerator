###START ImportBlock
##systemImport
import typing as typ
import mongoengine as medb

##customImport
from configs.CFGNames import ME_SETTINGS
from tests.test_Service import FunctionalClass

from modules.nameAnalysis import AnalysysService, Analysis

from database.medbNameSchemas import Race, GenderGroups
from database.medbNameSchemas import Male, Female, Surnames

from database.medbCheckSumSchemas import GlobalFlags

from database.medbAnalyticSchemas import GlobalCounts, NameLettersCount, VowelsCount
from database.medbAnalyticSchemas import ConsonantsCount, FirstLetters, Letters
from database.medbAnalyticSchemas import VowelsChains, ConsonantsChains
from database.medbAnalyticSchemas import ChainsCombinations, NameEndings

###FINISH ImportBlock

###START GlobalConstantBlock
###FINISH GlobalConstantBlock

###START DecoratorBlock
###FINISH DecoratorBlock

###START FunctionalBlock
class AnalysysService_Test(FunctionalClass):
    '''
    Testing next methods of class #AnalysysService:
    getBaseOfNames;
    '''

    ##BEGIN ConstantBlock
    mdb_names_alias = ME_SETTINGS.MDB_n_Aliases['mdbName']['alias']
    TestFiles = {}
    NamesAnalyticData = {}
    ##END ConstantBlock

    ##BEGIN PrepareBlock
    @classmethod
    def setUpClass(cls) -> typ.NoReturn:
        '''Set up for class.'''
        cls.printSetUpClassMsg()
        cls.createTestFiles()

        #Using mongomock for testing
        medb.connect('mongoenginetest2', 
                host='mongomock://localhost', 
                alias=cls.mdb_names_alias)

    @classmethod
    def tearDownClass(cls) -> typ.NoReturn:
        '''Tear down for class.'''
        medb.disconnect(alias=cls.mdb_names_alias)

        cls.removeTestFiles()
        cls.printTearDownClassMsg()


    def setUp(self) -> typ.NoReturn:
        '''Set up for test.'''
        self.printSetUpMethodMsg()
        
        race = Race()
        race.race = 'TestRace'
        race.save()

        gender_male = Male()
        gender_male.name = 'TestMale'
        gender_male.race = race
        gender_male.save()

        gender_female = Female()
        gender_female.name = 'TestFemale'
        gender_female.race = race
        gender_female.save()
        
        gender_surname = Surnames()
        gender_surname.name = 'TestSurname'
        gender_surname.race = race
        gender_surname.save()
        
        self.TestConstruction = AnalysysService(usingFileStoringFlag=False)


    def tearDown(self) -> typ.NoReturn:
        '''Tear down for test.'''
        Race.drop_collection()
        Male.drop_collection()
        Female.drop_collection()
        Surnames.drop_collection()

        self.printTearDownMethodMsg()
        self.TestConstruction = None

    ##END PrepareBlock

    @FunctionalClass.descript
    def test_getBaseOfNames_checkingReadedMongoData_expectedDict(
            self) -> typ.NoReturn:
        '''
        Testing read dictionary data from mongodb.
        '''
        self.TestConstruction.getBaseOfNames(usingFileStoringFlag=False)

        res = self.TestConstruction.baseOfNames
        self.assertDictEqual(res, 
                        {'Races': [
                            {'TestRace': {'Genders': {
                                'Female': {'Names': ['TestFemale']}, 
                                'Male': {'Names': ['TestMale']}
                                }, 
                                'Surnames': ['TestSurname']}}
                            ]})


class AnalyticLetters_Test(FunctionalClass):
    pass


class AnalyticChains_Test(FunctionalClass):
    pass


class AnalyticCombinations_Test(FunctionalClass):
    pass


class Analysis_Test(FunctionalClass):
    '''
    Testing next methods of class #AnalyticChains:
    makeAnalyticDB;
    '''

    ##BEGIN ConstantBlock
    mdb_alias = ME_SETTINGS.MDB_n_Aliases['mdbAnalytic']['alias']
    mdb_names_alias = ME_SETTINGS.MDB_n_Aliases['mdbName']['alias']
    mdb_checksum_alias = ME_SETTINGS.MDB_n_Aliases['mdbCheckSum']['alias']
    TestFiles = {
        'tmpLOGTESTNames.log': str(),
    }
    NamesAnalyticData = {'TestRace': {
            'Max_Names_Count': 0,
            'Male_Names_Count': 0,
            'Female_Names_Count': 0,
            'Surnames_Count': 0,
            "Name_Letters_Count": {},
            "Vowels_Count": {},
            "Consonants_Count": {},
            "First_Letters": {
                "Vowels_Count": 0,
                "Consonants_Count": 0,
            },
            "Letters": {},
            "Vowels_Chains": {
                "Chains": {},
                "Chain_Frequency": {},
                "Length_Count_Names": {}
            },
            "Consonants_Chains": {
                "Chains": {},
                "Chain_Frequency": {},
                "Length_Count_Names": {}
            },
            "Chains_Combinations": {},
            "Name_Endings": {}
        }}
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
                alias=cls.mdb_names_alias)
        medb.connect('mongoenginetest3', 
                host='mongomock://localhost', 
                alias=cls.mdb_checksum_alias)


    @classmethod
    def tearDownClass(cls) -> typ.NoReturn:
        '''Tear down for class.'''
        medb.disconnect(alias=cls.mdb_checksum_alias)
        medb.disconnect(alias=cls.mdb_names_alias)
        medb.disconnect(alias=cls.mdb_alias)

        cls.removeTestFiles()
        cls.printTearDownClassMsg()


    def setUp(self) -> typ.NoReturn:
        '''Set up for test.'''
        self.printSetUpMethodMsg()
        
        existFlag = GlobalFlags()
        existFlag.globalExist = False
        existFlag.save()
        
        race = Race()
        race.race = 'TestRace'
        race.save()

        gender_groups = GenderGroups()
        gender_groups.gender_group = 'Male'
        gender_groups.save()

        gender_groups = GenderGroups()
        gender_groups.gender_group = 'Female'
        gender_groups.save()

        gender_groups = GenderGroups()
        gender_groups.gender_group = 'Surnames'
        gender_groups.save()

        gender_groups = GenderGroups()
        gender_groups.gender_group = 'Common'
        gender_groups.save()

        tmp_Construction = AnalysysService(usingFileStoringFlag=False)
        self.TestConstruction = Analysis(tmp_Construction, 
                                         usingFileStoringFlag=False)

        self.TestConstruction.raceNameKey = 'TestRace'
        self.TestConstruction.localAnalyticKey = 'Test_Analytic_key'
        self.TestConstruction.groupKey = 'Test_Group_Key'
        
        tmpLogTestNames = str(self.TestFileDirectory + 'tmpLOGTESTNames.log')
        self.TestConstruction.logFilePath = tmpLogTestNames


    def tearDown(self) -> typ.NoReturn:
        '''Tear down for test.'''
        GlobalFlags.drop_collection()

        Race.drop_collection()
        GenderGroups.drop_collection()
        Male.drop_collection()
        Female.drop_collection()
        Surnames.drop_collection()
        
        GlobalCounts.drop_collection()
        NameLettersCount.drop_collection()
        VowelsCount.drop_collection()
        ConsonantsCount.drop_collection()
        FirstLetters.drop_collection()
        Letters.drop_collection()
        VowelsChains.drop_collection()
        ConsonantsChains.drop_collection()
        ChainsCombinations.drop_collection()
        NameEndings.drop_collection()

        self.printTearDownMethodMsg()
        self.TestConstruction = None

    ##END PrepareBlock        
    @FunctionalClass.descript
    def test_makeAnalyticDB_checkingCreatedMongoDB_expectedWritedData(
            self) -> typ.NoReturn:
        '''
        Testing the method of making analytic database and write 
        in analytic database file.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)

        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.baseOfNames = {'Races': [
                {'TestRace': {
                    'Genders': {
                        'Female': {'Names': ['Fe']}, 
                        'Male': {'Names': ['Me', 'Ma']}
                        }, 
                    'Surnames': ['Su']}}
                ]}

        answ = self.TestConstruction.makeAnalyticDB(usingFileStoringFlag=False)

        res = dict()

        obj = GlobalCounts.objects.first()
        res.update({'Max_Names_Count': obj.maxNamesCount,
                    'Male_Names_Count': obj.maleNamesCount,
                    'Female_Names_Count': obj.femaleNamesCount,
                    'Surnames_Count': obj.surnamesCount,
                    'First_Letters': dict()
                })
        res['First_Letters'].update({
            'Vowels_Count': obj.firstLettersCounts.vowelsCount, 
            'Consonants_Count': obj.firstLettersCounts.consonantsCount})
        
        gender = GenderGroups.objects(gender_group='Male').first()
        obj = FirstLetters.objects(gender_group=gender).first()
        res['First_Letters'].update({'Male': {
                                        obj.key: {
                                            'Count': obj.count,
                                            'Chance': obj.chance
                                        }
                                    }})
        
        self.assertDictEqual(res, { 'Max_Names_Count': 4, 
                                    'Male_Names_Count': 2, 
                                    'Female_Names_Count': 1, 
                                    'Surnames_Count': 1,
                                    'First_Letters': {
                                        'Vowels_Count': 0, 
                                        'Consonants_Count': 4, 
                                        'Male': {
                                            'M': {'Count': 2, 'Chance': 100.0}}
                                        }, 
                                    })
###FINISH FunctionalBlock

###START MainBlock
def main() -> typ.NoReturn:
    pass
###FINISH Mainblock