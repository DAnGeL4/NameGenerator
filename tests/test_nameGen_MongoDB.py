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
from database.medbAnalyticSchemas import NameLettersCount, NameEndings
from database.medbAnalyticSchemas import ChainsTemplate, FirstLetters

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
    getMinMaxSize;
    getRandomKey;
    getNameSize;
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
        self.race = race

        genderGp = GenderGroups()
        genderGp.gender_group = 'TestGender'
        genderGp.save()
        self.gender = genderGp

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
        vowels_chains.save()
        
        lettersCount = NameLettersCount()
        lettersCount.race = race.id
        lettersCount.gender_group = genderGp.id
        lettersCount.key = 3
        lettersCount.count = 3
        lettersCount.chance = 3.0
        lettersCount.save()

    def tearDown(self) -> typ.NoReturn:
        '''Tear down for test.'''
        
        GlobalCounts.drop_collection()
        VowelsChains.drop_collection()
        NameLettersCount.drop_collection()
        NameEndings.drop_collection()
        FirstLetters.drop_collection()

        Race.drop_collection()
        GenderGroups.drop_collection()
        Male.drop_collection()

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
                
        self.assertListEqual(res, [{'race': {'$oid': str(self.race.id)},
                                    'gender_group': {'$oid': str(self.gender.id)},
                                    '_cls': 'NameLettersCount',
                                    'key': 3,
                                    'count': 3,
                                    'chance': 3.0}])

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

    @FunctionalClass.descript
    def test_getRandomByAnalytic_readingData_expectedRules(
            self) -> typ.NoReturn:
        '''
        Testing the method of makes prepared analytic data.
        '''
        genObj = ManualNameGen()
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'
        
        res = genObj.getRandomByAnalytic(NameLettersCount, modify=False)
                
        self.assertListEqual(res, [{'key': 3, 'range': (0, 3.0)}])

    @FunctionalClass.descript
    def test_getRandomByAnalytic_readingData_expectedModifiedRules(
            self) -> typ.NoReturn:
        '''
        Testing the method of makes prepared analytic data.
        '''
        genObj = ManualNameGen()
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'
        
        res = genObj.getRandomByAnalytic(NameLettersCount, modify=True)
                
        self.assertListEqual(res, [{'key': 3, 'range': (0, 2.97)},
                                  {'key': None, 'range': (2.97, 3.97)}])

    @FunctionalClass.descript
    def test_getRandomByAnalytic_readingEmbeddedData_expectedModifiedRules(
            self) -> typ.NoReturn:
        '''
        Testing the method of makes prepared analytic data.
        '''
        genObj = ManualNameGen()
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'
        
        res = genObj.getRandomByAnalytic(VowelsChains, 
                                        embedded='chains')
                
        self.assertListEqual(res, [{'key': 'key_6', 'range': (0, 0.594)},
                                  {'key': None, 
                                   'range': (0.594, 1.5939999999999999)}])

    @FunctionalClass.descript
    def test_getMinMaxSize_findingValues_expectedMinMaxValues(
            self) -> typ.NoReturn:
        '''
        Testing the method of finding the minimum and 
        maximum key, or key length.
        '''
        genObj = ManualNameGen()
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'
        
        lettersCount = NameLettersCount()
        lettersCount.race = self.race.id
        lettersCount.gender_group = self.gender.id
        lettersCount.key = 5
        lettersCount.count = 5
        lettersCount.chance = 5.0
        lettersCount.save()
        
        res = genObj.getMinMaxSize(NameLettersCount)
                
        self.assertTupleEqual(res, (3, 5))

    @FunctionalClass.descript
    def test_getMinMaxSize_findingValues_expectedRandomMaxValue(
            self) -> typ.NoReturn:
        '''
        Testing the method of finding the minimum and 
        maximum key, or key length.
        '''
        genObj = ManualNameGen(0)
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'
        
        lettersCount = NameLettersCount()
        lettersCount.race = self.race.id
        lettersCount.gender_group = self.gender.id
        lettersCount.key = 500
        lettersCount.count = 500
        lettersCount.chance = 500.0
        lettersCount.save()
        
        res = genObj.getMinMaxSize(NameLettersCount)
                
        self.assertTupleEqual(res, (3, 1500))

    @FunctionalClass.descript
    def test_getMinMaxSize_findingEmbeddedValues_expectedMinMaxValue(
            self) -> typ.NoReturn:
        '''
        Testing the method of finding the minimum and 
        maximum key, or key length.
        '''
        genObj = ManualNameGen()
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'
                
        embedded_vowels_chains = ChainsTemplate()
        embedded_vowels_chains.key = 'long_key_8'
        embedded_vowels_chains.count = 8
        embedded_vowels_chains.chance = 0.8
    
        vowels_chains = VowelsChains.objects.first()
        vowels_chains.chains.append(embedded_vowels_chains)
        vowels_chains.save()
        
        res = genObj.getMinMaxSize(VowelsChains, 
                                   embedded='chains')
                
        self.assertTupleEqual(res, (5, 10))

    @FunctionalClass.descript
    def test_getMinMaxSize_findingValuesInRules_expectedMinMaxValue(
            self) -> typ.NoReturn:
        '''
        Testing the method of finding the minimum and 
        maximum key, or key length.
        '''
        genObj = ManualNameGen()
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'

        data = [{'key': 'key_6', 'range': (0, 0.6)}, 
                {'key': 'long_key_8', 'range': (0.6, 1.4)}]
        
        res = genObj.getMinMaxSize(NameLettersCount, 
                                   randomRules=data)
                
        self.assertTupleEqual(res, (5, 10))

    @FunctionalClass.descript
    def test_getRandomKey_gettingKey_expectedKeyFromDB(
            self) -> typ.NoReturn:
        '''
        Testing the method of gets a random key 
        according to the rules of randomness.
        '''
        genObj = ManualNameGen(10)
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'
        
        lettersCount = NameLettersCount()
        lettersCount.race = self.race.id
        lettersCount.gender_group = self.gender.id
        lettersCount.key = 8
        lettersCount.count = 8
        lettersCount.chance = 8.0
        lettersCount.save()
        
        res = genObj.getRandomKey(NameLettersCount)
                
        self.assertEqual(res, 8)

    @FunctionalClass.descript
    def test_getRandomKey_gettingEmbeddedKey_expectedKeyFromDB(
            self) -> typ.NoReturn:
        '''
        Testing the method of gets a random key 
        according to the rules of randomness.
        '''
        genObj = ManualNameGen(10)
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'
        
        embedded_vowels_chains = ChainsTemplate()
        embedded_vowels_chains.key = 'long_key_8'
        embedded_vowels_chains.count = 8
        embedded_vowels_chains.chance = 0.8
    
        vowels_chains = VowelsChains.objects.first()
        vowels_chains.chains.append(embedded_vowels_chains)
        vowels_chains.save()
        
        res = genObj.getRandomKey(VowelsChains,
                                  embedded='chains')
                
        self.assertEqual(res, 'long_key_8')

    @FunctionalClass.descript
    def test_getRandomKey_gettingKey_expectedKey(
            self) -> typ.NoReturn:
        '''
        Testing the method of gets a random key 
        according to the rules of randomness.
        '''
        genObj = ManualNameGen(10)
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'

        data = [{'key': 6, 'range': (0, 0.6)}, 
                {'key': 8, 'range': (0.6, 1.4)}]
        
        res = genObj.getRandomKey(NameLettersCount, 
                                  randomRules=data)
                
        self.assertEqual(res, 8)

    @FunctionalClass.descript
    def test_getNameSize_gettingSize_expectedNameSize(
            self) -> typ.NoReturn:
        '''
        Testing the method of gets a random name length 
        according to analytics.
        '''
        genObj = ManualNameGen(10)
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'
        
        lettersCount = NameLettersCount()
        lettersCount.race = self.race.id
        lettersCount.gender_group = self.gender.id
        lettersCount.key = 8
        lettersCount.count = 8
        lettersCount.chance = 8.0
        lettersCount.save()
        
        res = genObj.getNameSize()
                
        self.assertEqual(res, 8)

    @FunctionalClass.descript
    def test_getNameSize_queringEmptyKeys_expectedRandomSize(
            self) -> typ.NoReturn:
        '''
        Testing the method of gets a random name length 
        according to analytics.
        '''
        genObj = ManualNameGen(10)
        genObj.race = ''
        genObj.genderGroup = ''
        
        res = genObj.getNameSize()
                
        self.assertEqual(res, 18)

    @FunctionalClass.descript
    def test_getNameSize_queringEmptyDB_expectedRandomSize(
            self) -> typ.NoReturn:
        '''
        Testing the method of gets a random name length 
        according to analytics.
        '''
        genObj = ManualNameGen(10)
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'
        
        lettersCount = NameLettersCount.objects.first()
        lettersCount.delete()
        
        res = genObj.getNameSize()
                
        self.assertEqual(res, 18)

    @FunctionalClass.descript
    def test_getNameEndSize_gettingSize_expectedNameSize(
            self) -> typ.NoReturn:
        '''
        Testing the method of gets a random name length 
        according to analytics.
        '''
        genObj = ManualNameGen(10)
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'
        
        endings = NameEndings()
        endings.race = self.race.id
        endings.gender_group = self.gender.id
        endings.key = 'ending'
        endings.count = 6
        endings.chance = 6.0
        endings.save()
                
        endings = NameEndings()
        endings.race = self.race.id
        endings.gender_group = self.gender.id
        endings.key = 'endingtwo'
        endings.count = 8
        endings.chance = 8.0
        endings.save()
        
        res = genObj.getNameEndSize()
                
        self.assertEqual(res, 9)

    @FunctionalClass.descript
    def test_getNameEndSize_queringEmptyKeys_expectedRandomSize(
            self) -> typ.NoReturn:
        '''
        Testing the method of gets a random name length 
        according to analytics.
        '''
        genObj = ManualNameGen(10)
        genObj.race = ''
        genObj.genderGroup = ''
                
        endings = NameEndings()
        endings.race = self.race.id
        endings.gender_group = self.gender.id
        endings.key = 'ending'
        endings.count = 6
        endings.chance = 6.0
        endings.save()
        
        res = genObj.getNameEndSize()
                
        self.assertEqual(res, 13)

    @FunctionalClass.descript
    def test_getNameEndSize_queringEmptyDB_expectedRandomSize(
            self) -> typ.NoReturn:
        '''
        Testing the method of gets the length 
        of the end of the name.
        '''
        genObj = ManualNameGen(10)
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'
        
        res = genObj.getNameEndSize()
                
        self.assertEqual(res, 13)

    @FunctionalClass.descript
    def test_getNameFirstLetter_gettingFirstLetter_expectedLetter(
            self) -> typ.NoReturn:
        '''
        Testing the method of gets a random first letter 
        from the analytic with a probability of any letter.
        '''
        genObj = ManualNameGen(1)
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'
        
        endings = FirstLetters()
        endings.race = self.race.id
        endings.gender_group = self.gender.id
        endings.key = 'A'
        endings.count = 6
        endings.chance = 6.0
        endings.save()
                
        endings = FirstLetters()
        endings.race = self.race.id
        endings.gender_group = self.gender.id
        endings.key = 'B'
        endings.count = 8
        endings.chance = 8.0
        endings.save()
        
        res = genObj.getNameFirstLetter()
                
        self.assertEqual(res, 'A')

    @FunctionalClass.descript
    def test_getNameFirstLetter_gettingFirstLetter_expectedRandomLetter(
            self) -> typ.NoReturn:
        '''
        Testing the method of gets a random first letter 
        from the analytic with a probability of any letter.
        '''
        genObj = ManualNameGen(10)
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'
        
        endings = FirstLetters()
        endings.race = self.race.id
        endings.gender_group = self.gender.id
        endings.key = 'A'
        endings.save()
        
        res = genObj.getNameFirstLetter()
                
        self.assertEqual(res, 'N')
                            
###FINISH FunctionalBlock

###START MainBlock
def main() -> typ.NoReturn:
    pass
###FINISH Mainblock
