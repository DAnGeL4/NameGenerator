###START ImportBlock
##systemImport
import typing as typ
import json
import mongoengine as medb
#from mongomock import MongoClient
#from mongomock import Database

##customImport
from configs.CFGNames import ME_SETTINGS
from tests.test_Service import FunctionalClass

#from database.medbCheckSumSchemas import GlobalFlags
#from database.medbCheckSumSchemas import ChecksumFiles
from database.medbNameSchemas import Race, GenderGroups, Male
from database.medbAnalyticSchemas import GlobalCounts, VowelsChains
from database.medbAnalyticSchemas import FirstLettersCounts, NameLettersCount
from database.medbAnalyticSchemas import ChainsTemplate

#from database.medbAnalyticSchemas import FirstLetters

from modules.nameGen import ManualNameGen

###FINISH ImportBlock

###START GlobalConstantBlock
###FINISH GlobalConstantBlock

###START DecoratorBlock
###FINISH DecoratorBlock


###START FunctionalBlock            
class ManualNameGen_Test(FunctionalClass):
    '''
    Testing next methods of class #ManualNameGen:
    getDBAnalyticData;
    
    getRandomByAnalytic;
    getRandomChance;
    inRange;
    getMinMaxSize;
    getMaxRange;
    getRandomKey;
    getAlphabetByChainType;
    getRandomLetter;
    getNameSize;
    getEndSizeChances;
    convertDictToListRules;
    getNameEndSize;
    getNameFirstLetter;
    getLetterType;
    getNextLetterType;
    getCollectionByType;
    makeFrequencyData;
    makeRangesByTypes;
    prepareFrequencyData;
    getChainSize;
    makeChainsOrder;
    getChainsData;
    getChainsList;
    prepareLettersAnalytic;
    getCombinationsAnalyticObject;
    getChainsAnalyticObject;
    makeAllChainLettersData;
    makeAllNamesLetters;
    getGivenLengthChains;
    prepareFirstChainLetters;
    cutChains;
    prepareLettersRules;
    makeLetterRules;
    getLettersRules;
    cutChance;
    createChain;
    findValidCombinations;
    createCombinationChances;
    setCombinationLetter;
    createNamePart;
    makeEndingChainsRules;
    printLogLine;
    createCharacterName.
    '''

    ##BEGIN ConstantBlock
    mdb_alias = ME_SETTINGS.MDB_n_Aliases['mdbName']['alias']
    mdb_analytic_alias = ME_SETTINGS.MDB_n_Aliases['mdbAnalytic']['alias']

    #tst_mdbNAliases = MongoDBTools.mdbNAliases
    #tst_getConnectString = MongoDBTools.getConnectString
    #mdb_test = 'test_db'
    #mdb_test_alias = 'test_alias'
    TestFiles = {}
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
                alias=cls.mdb_analytic_alias)

    @classmethod
    def tearDownClass(cls) -> typ.NoReturn:
        '''Tear down for class.'''
        medb.disconnect(alias=cls.mdb_alias)
        medb.disconnect(alias=cls.mdb_analytic_alias)

        cls.removeTestFiles()
        cls.printTearDownClassMsg()

    def setUp(self) -> typ.NoReturn:
        '''Set up for test.'''
        self.printSetUpMethodMsg()

        race = Race()
        race.race = 'TestRace'
        race.save()

        genderGp = GenderGroups()
        genderGp.gender_group = 'TestGender'
        genderGp.save()

        male = Male()
        male.race = race
        male.name = 'TestName'
        male.save()
        
        embedded_vowels_chains = ChainsTemplate()
        embedded_vowels_chains.key = 'key_6'
        embedded_vowels_chains.count = 6
        embedded_vowels_chains.chance = 0.6
    
        vowels_chains = VowelsChains()
        vowels_chains.race = race.id
        vowels_chains.gender_group = genderGp.id
        vowels_chains.chains.append(embedded_vowels_chains)
        #vowels_chains.chainFrequency.append(embedded_vowels_frequency)
        #vowels_chains.lengthCountNames.append(embedded_vowels_lencount)
        vowels_chains.save()
        
        lettersCount = NameLettersCount()
        lettersCount.race = race.id
        lettersCount.gender_group = genderGp.id
        lettersCount.key = 3
        lettersCount.save()

    def tearDown(self) -> typ.NoReturn:
        '''Tear down for test.'''
        #Return class data back after manipulation in tests
        #MongoDBTools.mdbNAliases = self.tst_mdbNAliases
        #MongoDBTools.getConnectString = self.tst_getConnectString
        
        GlobalCounts.drop_collection()
        VowelsChains.drop_collection()
        NameLettersCount.drop_collection()

        Race.drop_collection()
        GenderGroups.drop_collection()
        Male.drop_collection()

        #medb.disconnect(alias=self.mdb_test_alias)

        self.printTearDownMethodMsg()

    ##END PrepareBlock

    @FunctionalClass.descript
    def test_getDBAnalyticData_readingData_expectedData(
            self) -> typ.NoReturn:
        '''
        Testing the method of reads analytic data from 
        the database by race and gender group keys.
        '''
        genObj = ManualNameGen()
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'
        
        res = genObj.getDBAnalyticData(NameLettersCount)
        for r in res: r.pop('_id')

        race = Race.objects(race='TestRace').first()
        gender = GenderGroups.objects(gender_group='TestGender').first()
                
        self.assertListEqual(res, [{'race': {'$oid': str(race.id)},
                                    'gender_group': {'$oid': str(gender.id)},
                                    '_cls': 'NameLettersCount',
                                    'key': 3,
                                    'count': 0,
                                    'chance': 0.0}])

    @FunctionalClass.descript
    def test_getDBAnalyticData_readingData_expectedEmbeddedData(
            self) -> typ.NoReturn:
        '''
        Testing the method of reads analytic data from 
        the database by race and gender group keys.
        '''
        genObj = ManualNameGen()
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'
        
        res = genObj.getDBAnalyticData(VowelsChains, 
                                       embedded='chains')
                
        self.assertListEqual(res, [{'chance': 0.6, 
                                    'count': 6, 
                                    'key': 'key_6'}])
                            
###FINISH FunctionalBlock

###START MainBlock
def main() -> typ.NoReturn:
    pass
###FINISH Mainblock
