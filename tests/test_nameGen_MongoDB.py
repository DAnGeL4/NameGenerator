###START ImportBlock
##systemImport
import typing as typ
import mongoengine as medb

##customImport
from configs.CFGNames import ME_SETTINGS
from tests.test_Service import FunctionalClass

from database.medbNameSchemas import Race, GenderGroups, Male
from database.medbAnalyticSchemas import GlobalCounts, VowelsChains
from database.medbAnalyticSchemas import NameLettersCount, NameEndings
from database.medbAnalyticSchemas import ChainsTemplate, FirstLetters
from database.medbAnalyticSchemas import ConsonantsChains, Letters
from database.medbAnalyticSchemas import ChainFrequencyTemplate

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
    getCollectionByType;
    makeFrequencyData;
    makeChainsOrder;
    getChainsData;
    getChainsList;
    makeAllNamesLetters;
    prepareCreationChain;
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
        
        cons_chains = ConsonantsChains()
        cons_chains.race = race.id
        cons_chains.gender_group = genderGp.id
        cons_chains.save()
        
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
        ConsonantsChains.drop_collection()
        NameLettersCount.drop_collection()
        NameEndings.drop_collection()
        FirstLetters.drop_collection()
        Letters.drop_collection()

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
    
    @FunctionalClass.descript
    def test_getCollectionByType_getsCollectionData_expectedConsonant(
            self) -> typ.NoReturn:
        '''
        Testing the method of getting a Mongoengine collection 
        by chain type and embedded type.
        '''
        res = ManualNameGen().getCollectionByType("consonant")
        self.assertTupleEqual(res, (ConsonantsChains, "chains"))
    
    @FunctionalClass.descript
    def test_getCollectionByType_getsCollectionData_expectedVowel(
            self) -> typ.NoReturn:
        '''
        Testing the method of getting a Mongoengine collection 
        by chain type and embedded type.
        '''
        res = ManualNameGen().getCollectionByType("vowel",
                                                 embeddedType='testType')
        self.assertTupleEqual(res, (VowelsChains, "testType"))
                
    @FunctionalClass.descript
    def test_makeFrequencyData_makingData_expectedCollectionData(
            self) -> typ.NoReturn:
        '''
        Testing the method of making the chain frequency, 
        ordered by chain type.
        '''
        genObj = ManualNameGen(10)
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'
                
        embedded = ChainFrequencyTemplate()
        embedded.key = 4
        embedded.chance = 40.0
                
        vow_chains = VowelsChains.objects.first()
        vow_chains.chainFrequency.append(embedded)
        vow_chains.save()
                
        res = genObj.makeFrequencyData()
        self.assertDictEqual(res, {'consonant': [], 
                                   'vowel': [{
                                       'key':4,
                                       'count': 0,
                                       'chance': 40.0
                                   }]})
                
    @FunctionalClass.descript
    def test_makeChainsOrder_makingOrderStartsVow_expectedIntList(self) -> typ.NoReturn:
        '''
        Testing the method of making 
        the order of chains by type and length.
        '''
        genObj = ManualNameGen(10)
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'
        genObj.lastLetter = 'a'

        collections = [ConsonantsChains, VowelsChains]
        for collection in collections:
            chains = collection.objects.first()
            
            for i in range(3):
                embedded = ChainFrequencyTemplate()
                embedded.key = i
                embedded.chance = 6.0 - i
                chains.chainFrequency.append(embedded)
            chains.save()
                
        res = genObj.makeChainsOrder(croppedSize=7)
        self.assertListEqual(res, [2,1,2,2])
                
    @FunctionalClass.descript
    def test_makeChainsOrder_makingOrderStartsCons_expectedIntList(self) -> typ.NoReturn:
        '''
        Testing the method of making 
        the order of chains by type and length.
        '''
        genObj = ManualNameGen(1)
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'
        genObj.lastLetter = 'b'

        collections = [ConsonantsChains, VowelsChains]
        for collection in collections:
            chains = collection.objects.first()
            
            for i in range(3):
                embedded = ChainFrequencyTemplate()
                embedded.key = i
                embedded.chance = 6.0 - i
                chains.chainFrequency.append(embedded)
            chains.save()
                
        res = genObj.makeChainsOrder(croppedSize=7)
        self.assertListEqual(res, [2,1,1,1,2])
                
    @FunctionalClass.descript
    def test_makeChainsOrder_makingOrderLowestSize_expectedIntList(self) -> typ.NoReturn:
        '''
        Testing the method of making 
        the order of chains by type and length.
        '''
        genObj = ManualNameGen(1)
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'
        genObj.lastLetter = 'a'

        embedded = ChainFrequencyTemplate()
        embedded.key = 1
        embedded.chance = 5.0
        
        chains = VowelsChains.objects.first()
        chains.chainFrequency.append(embedded)
        chains.save()
                
        res = genObj.makeChainsOrder(croppedSize=1)
        self.assertListEqual(res, [1])
                
    @FunctionalClass.descript
    def test_makeChainsOrder_makingOrderEmptySize_expectedEmptyList(self) -> typ.NoReturn:
        '''
        Testing the method of making 
        the order of chains by type and length.
        '''
        genObj = ManualNameGen(1)
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'
        genObj.lastLetter = 'a'

        embedded = ChainFrequencyTemplate()
        embedded.key = 1
        embedded.chance = 5.0
        
        chains = VowelsChains.objects.first()
        chains.chainFrequency.append(embedded)
        chains.save()
                
        res = genObj.makeChainsOrder(croppedSize=0)
        self.assertListEqual(res, [])
                
    @FunctionalClass.descript
    def test_getChainsData_readingVowelDBData_expectedData(self) -> typ.NoReturn:
        '''
        Testing the method of reading chains data 
        from database by chain type.
        '''
        genObj = ManualNameGen(10)
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'
                
        res = genObj.getChainsData(chainType='vowel')
        self.assertListEqual(res, [{'count': 6, 'chance': 0.6, 
                                    'key': 'key_6'}])
                
    @FunctionalClass.descript
    def test_getChainsData_readingConsonantDBData_expectedData(self) -> typ.NoReturn:
        '''
        Testing the method of reading chains data 
        from database by chain type.
        '''
        genObj = ManualNameGen(10)
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'

        embedded = ChainsTemplate()
        embedded.key = 'key_3'
        embedded.count = 3
        embedded.chance = 3.6
    
        cons_chains = ConsonantsChains.objects.first()
        cons_chains.chains.append(embedded)
        cons_chains.save()
                
        res = genObj.getChainsData(chainType='consonant')
        self.assertListEqual(res, [{'count': 3, 'chance': 3.6, 
                                    'key': 'key_3'}])
                
    @FunctionalClass.descript
    def test_getChainsData_checkingChainType_expectedRaise(self) -> typ.NoReturn:
        '''
        Testing the method of reading chains data 
        from database by chain type.
        '''
        genObj = ManualNameGen(10)
        
        self.assertRaises(AssertionError, 
                          genObj.getChainsData, 
                          chainType='wrong_type')
                
    @FunctionalClass.descript
    def test_getChainsList_readingVowelDBData_expectedChains(self) -> typ.NoReturn:
        '''
        Testing the method of making list 
        of chains from chain rules.
        '''
        genObj = ManualNameGen(10)
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'
                
        res = genObj.getChainsList(chainType='vowel')
        self.assertListEqual(res, ['key_6'])
                
    @FunctionalClass.descript
    def test_getChainsList_makingChains_expectedChains(self) -> typ.NoReturn:
        '''
        Testing the method of making list 
        of chains from chain rules.
        '''
        genObj = ManualNameGen(10)
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'

        data = [{'count': 3, 'chance': 3.6, 'key': 'chain_3'},
                {'count': 4, 'chance': 4.8, 'key': 'chain_4'}]
                
        res = genObj.getChainsList(chainType='vowel',
                                  chainRules=data)
        self.assertListEqual(res, ['chain_3', 'chain_4'])
                
    @FunctionalClass.descript
    def test_makeAllNamesLetters_makingLettersRules_expectedVowels(self) -> typ.NoReturn:
        '''
        Testing the method of making rules 
        by the chances of all letters.
        '''
        genObj = ManualNameGen(10)
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'

        race = Race.objects.first()
        genderGp = GenderGroups.objects.first()
        
        letter = Letters()
        letter.race = race.id
        letter.gender_group = genderGp.id
        letter.key = 'a'
        letter.count = 3
        letter.chance = 3.0
        letter.save()
                
        res = genObj.makeAllNamesLetters(chainType='vowel')
        self.assertListEqual(res, [{'key': 'a', 'range': (0, 3.0)}])
                
    @FunctionalClass.descript
    def test_makeAllNamesLetters_makingLettersRules_expectedConsonants(self) -> typ.NoReturn:
        '''
        Testing the method of making rules 
        by the chances of all letters.
        '''
        genObj = ManualNameGen(10)
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'

        race = Race.objects.first()
        genderGp = GenderGroups.objects.first()
        
        letter = Letters()
        letter.race = race.id
        letter.gender_group = genderGp.id
        letter.key = 'b'
        letter.count = 4
        letter.chance = 4.0
        letter.save()
                
        res = genObj.makeAllNamesLetters(chainType='consonant')
        self.assertListEqual(res, [{'key': 'b', 'range': (0, 4.0)}])
                
    @FunctionalClass.descript
    def test_makeAllNamesLetters_makingLettersRules_expectedEmpty(self) -> typ.NoReturn:
        '''
        Testing the method of making rules 
        by the chances of all letters.
        '''
        genObj = ManualNameGen(10)
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'
                
        res = genObj.makeAllNamesLetters(chainType='consonant')
        self.assertListEqual(res, [])
                
    @FunctionalClass.descript
    def test_prepareCreationChain_preparingData_expectedData(self) -> typ.NoReturn:
        '''
        Testing the method of preparing data for chain creation.
        '''
        genObj = ManualNameGen(1)
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'

        data = [{'count': 3, 'chance': 3.6, 'key': 'aei'},
                {'count': 4, 'chance': 4.8, 'key': 'oi'}]
        
        race = Race.objects.first()
        genderGp = GenderGroups.objects.first()
        
        letter = Letters()
        letter.race = race.id
        letter.gender_group = genderGp.id
        letter.key = 'u'
        letter.count = 4
        letter.chance = 4.0
        letter.save()
                
        res = genObj.prepareCreationChain(lenChain=3,
                                          chainType='vowel',
                                          chainsRules=data)
        self.assertDictEqual(res, {'acl': [{'key': 'a', 'range': (0, 50.0)},
                                           {'key': 'e', 'range': (50.0, 100.0)},
                                           {'key': 'i', 'range': (100.0, 200.0)},
                                           {'key': 'o', 'range': (200.0, 250.0)}],
                                   'anl': [{'key': 'u', 'range': (0, 4.0)}],
                                   'fcl': [],
                                   'tmp': [{'chance': 3.6, 'count': 3, 'key': 'aei'}]
                                  })
                
    @FunctionalClass.descript
    def test_prepareCreationChain_checkingEmptyData_expectedData(self) -> typ.NoReturn:
        '''
        Testing the method of preparing data for chain creation.
        '''
        genObj = ManualNameGen(1)
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'
                
        res = genObj.prepareCreationChain(lenChain=3,
                                          chainType='vowel',
                                          chainsRules=[])
        self.assertDictEqual(res, {'acl': [{'range': (0, 100.0), 'key': 'k'}, 
                                           {'range': (100.0, 200.0), 'key': 'e'}, 
                                           {'range': (200.0, 300.0), 'key': 'y'}, 
                                           {'range': (300.0, 400.0), 'key': '_'}, 
                                           {'range': (400.0, 500.0), 'key': '6'}],
                                   'anl': [], 'fcl': [], 'tmp': []})
                
    @FunctionalClass.descript
    def test_prepareCreationChain_checkingFirstLetter_expectedReducedLen(self) -> typ.NoReturn:
        '''
        Testing the method of preparing data for chain creation.
        '''
        genObj = ManualNameGen(1)
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'
        genObj.lastLetter = 'a'
                
        _ = genObj.prepareCreationChain(lenChain=3,
                                        chainType='vowel',
                                        chainsRules=[])
        res = genObj.tmp_len
        self.assertEqual(res, 2)
                
    @FunctionalClass.descript
    def test_prepareCreationChain_checkingFirstLetter_expectedGenChain(self) -> typ.NoReturn:
        '''
        Testing the method of preparing data for chain creation.
        '''
        genObj = ManualNameGen(1)
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'
        genObj.lastLetter = 'a'
                
        _ = genObj.prepareCreationChain(lenChain=3,
                                        chainType='vowel',
                                        chainsRules=[])
        res = genObj.tmp_gen_chain
        self.assertEqual(res, 'a')
                
    @FunctionalClass.descript
    def test_prepareCreationChain_checkingFirstLetter_expectedData(self) -> typ.NoReturn:
        '''
        Testing the method of preparing data for chain creation.
        '''
        genObj = ManualNameGen(1)
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'
        genObj.lastLetter = 'a'

        data = [{'count': 3, 'chance': 3.6, 'key': 'aei'},
                {'count': 4, 'chance': 4.8, 'key': 'oi'}]
                
        res = genObj.prepareCreationChain(lenChain=3,
                                          chainType='vowel',
                                          chainsRules=data)
        self.assertDictEqual(res, {'acl': [{'key': 'a', 'range': (0, 50.0)},
                                           {'key': 'e', 'range': (50.0, 100.0)},
                                           {'key': 'i', 'range': (100.0, 200.0)},
                                           {'key': 'o', 'range': (200.0, 250.0)}],
                                   'anl': [],
                                   'fcl': [],
                                   'tmp': [{'chance': 3.6, 'count': 3, 'key': 'ei'}]
                                  })
                
    @FunctionalClass.descript
    def test_createChain_makingChain_expectedVowelChain(self) -> typ.NoReturn:
        '''
        Testing the method of making chain.
        '''
        genObj = ManualNameGen(1)
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'

        data = [{'count': 3, 'chance': 3.6, 'key': 'ae'},
                {'count': 4, 'chance': 4.8, 'key': 'oi'}]
        
        race = Race.objects.first()
        genderGp = GenderGroups.objects.first()
        
        letter = Letters()
        letter.race = race.id
        letter.gender_group = genderGp.id
        letter.key = 'u'
        letter.count = 4
        letter.chance = 4.0
        letter.save()
                
        res = genObj.createChain(lenChain=3,
                                 chainType='vowel',
                                 chainsRules=data)
        self.assertEqual(res, 'oue')
                
    @FunctionalClass.descript
    def test_createChain_checkingEmptyLetters_expectedVowelChain(self) -> typ.NoReturn:
        '''
        Testing the method of making chain.
        '''
        genObj = ManualNameGen(1)
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'

        data = [{'count': 3, 'chance': 3.6, 'key': 'ae'},
                {'count': 4, 'chance': 4.8, 'key': 'oi'}]
                
        res = genObj.createChain(lenChain=3,
                                 chainType='vowel',
                                 chainsRules=data)
        self.assertEqual(res, 'oeo')
                
    @FunctionalClass.descript
    def test_createChain_checkingEmptyRules_expectedVowelChain(self) -> typ.NoReturn:
        '''
        Testing the method of making chain.
        '''
        genObj = ManualNameGen(1)
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'
        
        race = Race.objects.first()
        genderGp = GenderGroups.objects.first()
        
        letter = Letters()
        letter.race = race.id
        letter.gender_group = genderGp.id
        letter.key = 'u'
        letter.count = 4
        letter.chance = 4.0
        letter.save()
                
        res = genObj.createChain(lenChain=3,
                                 chainType='vowel',
                                 chainsRules=[])
        self.assertEqual(res, 'yue')
                
    @FunctionalClass.descript
    def test_createChain_makingChain_expectedConsonantChain(self) -> typ.NoReturn:
        '''
        Testing the method of making chain.
        '''
        genObj = ManualNameGen(10)
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'

        data = [{'count': 3, 'chance': 3.6, 'key': 'bt'},
                {'count': 4, 'chance': 4.8, 'key': 'fs'}]
        
        race = Race.objects.first()
        genderGp = GenderGroups.objects.first()
        
        letter = Letters()
        letter.race = race.id
        letter.gender_group = genderGp.id
        letter.key = 'l'
        letter.count = 4
        letter.chance = 4.0
        letter.save()
                
        res = genObj.createChain(lenChain=3,
                                 chainType='consonant',
                                 chainsRules=data)
        self.assertEqual(res, 'bst')
                
    @FunctionalClass.descript
    def test_createChain_checkingConsFirstLetter_expectedVowelChain(self) -> typ.NoReturn:
        '''
        Testing the method of making chain.
        '''
        genObj = ManualNameGen(1)
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'
        genObj.lastLetter = 'b'

        data = [{'count': 3, 'chance': 3.6, 'key': 'ae'},
                {'count': 4, 'chance': 4.8, 'key': 'oi'}]
        
        race = Race.objects.first()
        genderGp = GenderGroups.objects.first()
        
        letter = Letters()
        letter.race = race.id
        letter.gender_group = genderGp.id
        letter.key = 'u'
        letter.count = 4
        letter.chance = 4.0
        letter.save()
                
        res = genObj.createChain(lenChain=3,
                                 chainType='vowel',
                                 chainsRules=data)
        self.assertEqual(res, 'bou')
                
    @FunctionalClass.descript
    def test_createChain_checkingVowFirstLetter_expectedVowelChain(self) -> typ.NoReturn:
        '''
        Testing the method of making chain.
        '''
        genObj = ManualNameGen(1)
        genObj.race = 'TestRace'
        genObj.genderGroup = 'TestGender'
        genObj.lastLetter = 'y'

        data = [{'count': 3, 'chance': 3.6, 'key': 'ae'},
                {'count': 4, 'chance': 4.8, 'key': 'oi'}]
        
        race = Race.objects.first()
        genderGp = GenderGroups.objects.first()
        
        letter = Letters()
        letter.race = race.id
        letter.gender_group = genderGp.id
        letter.key = 'u'
        letter.count = 4
        letter.chance = 4.0
        letter.save()
                
        res = genObj.createChain(lenChain=3,
                                 chainType='vowel',
                                 chainsRules=data)
        self.assertEqual(res, 'you')
        
###FINISH FunctionalBlock

###START MainBlock
def main() -> typ.NoReturn:
    pass
###FINISH Mainblock
