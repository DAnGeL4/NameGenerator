###START ImportBlock
##systemImport
import typing as typ

##customImport
from tests.test_Service import FunctionalClass
from modules.nameGen import ManualNameGen_Stub
from modules.nameGen import ManualNameGen

from modules.nameAnalysis import AnalyticChains, AnalyticCombinations
from modules.nameAnalysis import AnalyticLetters

###FINISH ImportBlock

###START GlobalConstantBlock
###FINISH GlobalConstantBlock

###START DecoratorBlock
###FINISH DecoratorBlock


###START FunctionalBlock
class ManualNameGen_Stub_Test(FunctionalClass):
    '''
    Testing next methods of class #FileTools:
    randomNameSize;
    randomLetter;
    createCharacterName.
    '''

    ##BEGIN ConstantBlock
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
    def test_randomNameSize_checkingRandom_expectedNumber(
            self) -> typ.NoReturn:
        '''
        Testing the method of generating random integer number.
        '''
        obj = ManualNameGen_Stub(seed=11)

        res = obj.randomNameSize(5, 10)
        self.assertEqual(res, 8)

    @FunctionalClass.descript
    def test_randomLetter_checkingRandom_expectedLetter(
            self) -> typ.NoReturn:
        '''
        Testing the method of generating random 
        lowercase letter from the alphabet.
        '''
        obj = ManualNameGen_Stub(seed=11)

        res = obj.randomLetter()
        self.assertEqual(res, 'o')

    @FunctionalClass.descript
    def test_createCharacterName_creatingName_expectedName(
            self) -> typ.NoReturn:
        '''
        Testing the method of random generation of a name.
        '''
        obj = ManualNameGen_Stub(seed=11)

        res = obj.createCharacterName()
        self.assertEqual(res, 'Ryqsut')         

                
class ManualNameGen_Test(FunctionalClass):
    '''
    Testing next methods of class #ManualNameGen:
    modifyChance;
    getFreeRandomChance;
    prepareEmbeddedData;
    setRangeByChances;
    getRandomChance;
    inRange;
    getMaxRange;
    getAlphabetByChainType;
    getRandomLetter;
    getEndSizeChances;
    convertDictToListRules;
    getLetterType;
    getNextLetterType;
    makeRangesByTypes;
    prepareFrequencyData;
    getChainSize;
    prepareLettersAnalytic;
    getCombinationsAnalyticObject;
    getChainsAnalyticObject;
    makeAllChainLettersData;
    getGivenLengthChains;
    prepareFirstChainLetters;
    cutChains;
    prepareLettersRules;
    makeLetterRules;
    getLettersRules;
    cutChance;
    '''

    ##BEGIN ConstantBlock
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
    def test_modifyChance_updatingChance_expectedModifiedChance(
            self) -> typ.NoReturn:
        '''
        Testing the method of modifies the chance to 
        a free global random chance.
        '''
        res = ManualNameGen().modifyChance(65.5)
        self.assertEqual(res, 64.845)
    
    @FunctionalClass.descript
    def test_getFreeRandomChance_makingRule_expectedRule(
            self) -> typ.NoReturn:
        '''
        Testing the method of makes range rule 
        for a free global random chance.
        '''
        res = ManualNameGen().getFreeRandomChance(65.5)
        self.assertDictEqual(res, { 'range': tuple((65.5, 66.5)),
                                    'key': None})
    
    @FunctionalClass.descript
    def test_prepareEmbeddedData_extractingData_expectedPreparedData(
            self) -> typ.NoReturn:
        '''
        Testing the method of extracts data 
        from embedded field.
        '''
        data = [{'embedded':[{'data'}, {'data'}]}]
                
        res = ManualNameGen().prepareEmbeddedData('embedded', data)
        self.assertListEqual(res, [{'data'}, {'data'}])
    
    @FunctionalClass.descript
    def test_setRangeByChances_makingRanges_expectedRules(
            self) -> typ.NoReturn:
        '''
        Testing the method of specifies key ranges by 
        key chances for analytic data.
        '''
        data = [{'key': 'a', 'count': 3, 'chance': 5.0},
               {'key': 'b', 'count': 4, 'chance': 6.67}]
                
        res = ManualNameGen().setRangeByChances(data, modify=False)
        self.assertListEqual(res, [{'range': tuple((0, 5.0)),
                                    'key': 'a'},
                                   {'range': tuple((5.0, 11.67)),
                                    'key': 'b'},
                                  ])
    
    @FunctionalClass.descript
    def test_setRangeByChances_makingRanges_expectedModifiedRules(
            self) -> typ.NoReturn:
        '''
        Testing the method of specifies key ranges by 
        key chances for analytic data.
        '''
        data = [{'key': 'a', 'count': 3, 'chance': 5.0},
               {'key': 'b', 'count': 4, 'chance': 6.67}]
                
        res = ManualNameGen().setRangeByChances(data, modify=True)
        self.assertListEqual(res, [{'range': tuple((0, 4.95)),
                                    'key': 'a'},
                                   {'range': tuple((4.95, 11.5533)),
                                    'key': 'b'},
                                   {'range': tuple((11.5533, 12.5533)),
                                    'key': None}
                                  ])
    
    @FunctionalClass.descript
    def test_getRandomChance_generingChance_expectedRandomChance(
            self) -> typ.NoReturn:
        '''
        Testing the method of generating a random floating 
        point chance within the given range.
        '''
        res = ManualNameGen(10).getRandomChance()
        self.assertEqual(res, 57.14025946899135)
    
    @FunctionalClass.descript
    def test_getRandomChance_generingChance_expectedInRangeChance(
            self) -> typ.NoReturn:
        '''
        Testing the method of generating a random floating 
        point chance within the given range.
        '''
        res = ManualNameGen(10).getRandomChance(5, 50)
        self.assertEqual(res, 24.28688323895389)
    
    @FunctionalClass.descript
    def test_inRange_checkingChance_expectedTrue(
            self) -> typ.NoReturn:
        '''
        Testing the method of checking the chance 
        is in the target range.
        '''
        res = ManualNameGen().inRange(24.28688323895389, 
                                      5, 50)
        self.assertTrue(res)
    
    @FunctionalClass.descript
    def test_inRange_checkingChance_expectedFalse(
            self) -> typ.NoReturn:
        '''
        Testing the method of checking the chance 
        is in the target range.
        '''
        res = ManualNameGen().inRange(57.14025946899135, 
                                      5, 50)
        self.assertFalse(res)
    
    @FunctionalClass.descript
    def test_getMaxRange_findingMaxKey_expectedMaxKey(
            self) -> typ.NoReturn:
        '''
        Testing the method of getting the max possible 
        range in rules.
        ''' 
        data = [{'key': 'key_6', 'range': (0, 0.6)}, 
                {'key': 'long_key_8', 'range': (0.6, 1.4)}]
        
        res = ManualNameGen().getMaxRange(randomRules=data)
        self.assertEqual(res, 1.4)
    
    @FunctionalClass.descript
    def test_getAlphabetByChainType_gettingAlphabet_expectedVowel(
            self) -> typ.NoReturn:
        '''
        Testing the method of getting a string of 
        letters (vowels, consonants, or all) by chain type.
        '''         
        res = ManualNameGen().getAlphabetByChainType('vowel')
        self.assertEqual(res, "aeiouy")
    
    @FunctionalClass.descript
    def test_getAlphabetByChainType_gettingAlphabet_expectedConsonant(
            self) -> typ.NoReturn:
        '''
        Testing the method of getting a string of 
        letters (vowels, consonants, or all) by chain type.
        '''         
        res = ManualNameGen().getAlphabetByChainType('consonant')
        self.assertEqual(res, "bcdfghjklmnpqrstvwxz")
    
    @FunctionalClass.descript
    def test_getAlphabetByChainType_gettingAlphabet_expectedAll(
            self) -> typ.NoReturn:
        '''
        Testing the method of getting a string of 
        letters (vowels, consonants, or all) by chain type.
        '''         
        res = ManualNameGen().getAlphabetByChainType('')
        self.assertEqual(res, "abcdefghijklmnopqrstuvwxyz")
    
    @FunctionalClass.descript
    def test_getRandomLetter_gettingLetter_expectedVowel(
            self) -> typ.NoReturn:
        '''
        Testing the method of getting a random letter 
        from the alphabet by chain type.
        '''         
        res = ManualNameGen(10).getRandomLetter('vowel')
        self.assertEqual(res, "u")
    
    @FunctionalClass.descript
    def test_getRandomLetter_gettingLetter_expectedConsonant(
            self) -> typ.NoReturn:
        '''
        Testing the method of getting a random letter 
        from the alphabet by chain type.
        '''         
        res = ManualNameGen(10).getRandomLetter('consonant')
        self.assertEqual(res, "x")
    
    @FunctionalClass.descript
    def test_getRandomLetter_gettingLetter_expectedAll(
            self) -> typ.NoReturn:
        '''
        Testing the method of getting a random letter 
        from the alphabet by chain type.
        '''         
        res = ManualNameGen(10).getRandomLetter('')
        self.assertEqual(res, "s")
    
    @FunctionalClass.descript
    def test_getEndSizeChances_makingData_expectedLengthChanceData(
            self) -> typ.NoReturn:
        '''
        Testing the method of making the chances 
        of the length of the endings.
        '''
        data = [{'key': 'abcd', 'count': 3, 'chance': 5.0},
               {'key': 'e', 'count': 4, 'chance': 6.67}]
                
        res = ManualNameGen().getEndSizeChances(data)
        self.assertDictEqual(res, {4: 5.0, 1: 6.67})
    
    @FunctionalClass.descript
    def test_convertDictToListRules_convertingData_expectedConvertedData(
            self) -> typ.NoReturn:
        '''
        Testing the method of making the chances 
        of the length of the endings.
        '''
        data = {4: 5.0, 1: 6.67}
                
        res = ManualNameGen().convertDictToListRules(data, preparing=False)
        self.assertListEqual(res, [{'key': 4, 'chance': 5.0}, 
                                   {'key': 1, 'chance': 6.67}])
    
    @FunctionalClass.descript
    def test_convertDictToListRules_convertingData_expectedRules(
            self) -> typ.NoReturn:
        '''
        Testing the method of making the chances 
        of the length of the endings.
        '''
        data = {4: 5.0, 1: 6.67}
                
        res = ManualNameGen().convertDictToListRules(data)
        self.assertListEqual(res, [{'key': 4, 'range': (0, 5.0)}, 
                                   {'key': 1, 'range': (5.0, 11.67)}])
    
    @FunctionalClass.descript
    def test_getLetterType_checkingType_expectedVowel(
            self) -> typ.NoReturn:
        '''
        Testing the method of checking type (vowel 
        or consonant) for target letter.
        '''
        res = ManualNameGen().getLetterType('a')
        self.assertEqual(res, "vowel")
    
    @FunctionalClass.descript
    def test_getLetterType_checkingType_expectedConsonant(
            self) -> typ.NoReturn:
        '''
        Testing the method of checking type (vowel 
        or consonant) for target letter.
        '''
        res = ManualNameGen().getLetterType('b')
        self.assertEqual(res, "consonant")
    
    @FunctionalClass.descript
    def test_getNextLetterType_checkingType_expectedConsonant(
            self) -> typ.NoReturn:
        '''
        Testing the method of getting the next letter type 
        (vowel or consonant) given the current type.
        '''
        res = ManualNameGen().getNextLetterType("vowel")
        self.assertEqual(res, "consonant")
    
    @FunctionalClass.descript
    def test_getNextLetterType_checkingType_expectedVowel(
            self) -> typ.NoReturn:
        '''
        Testing the method of getting the next letter type 
        (vowel or consonant) given the current type.
        '''
        res = ManualNameGen().getNextLetterType("consonant")
        self.assertEqual(res, "vowel")
                
    @FunctionalClass.descript
    def test_makeRangesByTypes_makingRanges_expectedData(
            self) -> typ.NoReturn:
        '''
        Testing the method of making the chain ranges, 
        ordered by chain type.
        '''
        data = {'consonant': [], 
                'vowel': [{
                   'key':4,
                   'count': 0,
                   'chance': 40.0
                }]}
                
        res = ManualNameGen(10).makeRangesByTypes(data)
        self.assertDictEqual(res, {'consonant': (0, 0), 'vowel': (4, 4)})
                
    @FunctionalClass.descript
    def test_prepareFrequencyData_cuttingData_expectedCuttedData(
            self) -> typ.NoReturn:
        '''
        Testing the method of preaparing rules 
        by match of the range.
        '''
        min_max = tuple((2, 4))
        data = [{'key': 4, 'range': tuple((0, 5.0))}, 
                {'key': 1, 'range': tuple((5.0, 11.0))}]
                
        res = ManualNameGen().prepareFrequencyData(min_max, data)
        self.assertListEqual(res, [{'key': 4, 'range': tuple((0, 5.0))}])
                
    @FunctionalClass.descript
    def test_prepareFrequencyData_cuttingData_expectedEmptyData(
            self) -> typ.NoReturn:
        '''
        Testing the method of preaparing rules 
        by match of the range.
        '''
        min_max = tuple((2, 3))
        data = [{'key': 4, 'range': tuple((0, 5.0))}, 
                {'key': 1, 'range': tuple((5.0, 11.0))}]
                
        res = ManualNameGen().prepareFrequencyData(min_max, data)
        self.assertListEqual(res, [])
                
    @FunctionalClass.descript
    def test_getChainSize_gettingProbablySize_expectedSize(
            self) -> typ.NoReturn:
        '''
        Testing the method of getting a 
        random chain size by analytics.
        '''
        croppedSize = 7
        min_max = tuple((1, 4))
        data = [{'key': 3, 'count': 0, 'chance': 5.0}, 
                {'key': 2, 'count': 0, 'chance': 5.0},
                {'key': 1, 'count': 0, 'chance': 9.0}]
                
        res = ManualNameGen(10).getChainSize(croppedSize, 
                                           min_max, data)
        self.assertEqual(res, 1)
                
    @FunctionalClass.descript
    def test_getChainSize_gettingWithoutProbableSize_expectedCroppedSize(
            self) -> typ.NoReturn:
        '''
        Testing the method of getting a 
        random chain size by analytics.
        '''
        croppedSize = 2
        min_max = tuple((1, 4))
        data = [{'key': 3, 'count': 0, 'chance': 50.0}, 
                {'key': 2, 'count': 0, 'chance': 0.0},
                {'key': 1, 'count': 0, 'chance': 0.0}]
                
        res = ManualNameGen(10).getChainSize(croppedSize, 
                                           min_max, data)
        self.assertEqual(res, 2)
                
    @FunctionalClass.descript
    def test_getChainSize_checkingLowestCroppedSize_expectedCroppedSize(
            self) -> typ.NoReturn:
        '''
        Testing the method of getting a 
        random chain size by analytics.
        '''
        croppedSize = 1
        min_max = tuple((2, 4))
        data = [{'key': 3, 'count': 0, 'chance': 50.0}, 
                {'key': 2, 'count': 0, 'chance': 0.0},
                {'key': 1, 'count': 0, 'chance': 0.0}]
                
        res = ManualNameGen(10).getChainSize(croppedSize, 
                                           min_max, data)
        self.assertEqual(res, 1)
                
    @FunctionalClass.descript
    def test_prepareLettersAnalytic_fillingObject_expectedFilledData(
            self) -> typ.NoReturn:
        '''
        Testing the method of prepares initial data 
        for an analytic object.
        '''
        data = ['chainone', 'chaintwo', 'chainthree']
                
        obj = ManualNameGen(10).prepareLettersAnalytic(chainList=data)
        res = obj.tmp_NamesDB['Common']
        self.assertListEqual(res, ['chainone', 'chaintwo', 
                                   'chainthree'])
                
    @FunctionalClass.descript
    def test_prepareLettersAnalytic_fillingObject_expectedFilledTemplate(
            self) -> typ.NoReturn:
        '''
        Testing the method of prepares initial data 
        for an analytic object.
        '''
        data = ['chainone', 'chaintwo', 'chainthree']
                
        obj = ManualNameGen(10).prepareLettersAnalytic(chainList=data)
        res = obj.tmp_NamesAnalytic
        self.assertDictEqual(res, {'tmp_Race': {
                                        'Max_Names_Count': 3,
                                        'First_Letters': {
                                            'Vowels_Count': 0,
                                            'Consonants_Count': 0,
                                        },
                                        "Letters": {}
                                    }})
                
    @FunctionalClass.descript
    def test_prepareLettersAnalytic_fillingObject_expectedObject(
            self) -> typ.NoReturn:
        '''
        Testing the method of prepares initial data 
        for an analytic object.
        '''
        data = ['chainone', 'chaintwo', 'chainthree']
                
        res = ManualNameGen(10).prepareLettersAnalytic(chainList=data)
        self.assertIsInstance(res, AnalyticLetters)
                
    @FunctionalClass.descript
    def test_getCombinationsAnalyticObject_initializingObject_expectedObject(
            self) -> typ.NoReturn:
        '''
        Testing the method of initializing 
        combination analytics object.
        '''
        res = ManualNameGen(10).getCombinationsAnalyticObject()
        self.assertIsInstance(res, AnalyticCombinations)
                
    @FunctionalClass.descript
    def test_getChainsAnalyticObject_initializingObject_expectedObject(
            self) -> typ.NoReturn:
        '''
        Testing the method of initializing 
        chains analytics object.
        '''
        res = ManualNameGen(10).getChainsAnalyticObject()
        self.assertIsInstance(res, AnalyticChains)
                
    @FunctionalClass.descript
    def test_makeAllChainLettersData_makingAnalytic_expectedChancesData(
            self) -> typ.NoReturn:
        '''
        Testing the method of makes rules by the chances 
        of all letters in chains from the data.
        '''
        data = ['cho', 'cht']
                
        res = ManualNameGen(10).makeAllChainLettersData(chainList=data)
        self.assertListEqual(res, [{'key': 'c', 'range': (0, 100.0)},
                                   {'key': 'h', 'range': (100.0, 200.0)},
                                   {'key': 'o', 'range': (200.0, 250.0)},
                                   {'key': 't', 'range': (250.0, 300.0)}])
                
    @FunctionalClass.descript
    def test_getGivenLengthChains_findingKeys_expectedKeys(
            self) -> typ.NoReturn:
        '''
        Testing the method of finding a list of chains 
        of the given length.
        '''
        data = [{'key': 'chainone', 'count': 0, 'chance': 0.0}, 
                {'key': 'chaintwo', 'count': 0, 'chance': 0.0}, 
                {'key': 'chainother', 'count': 0, 'chance': 0.0}]
                
        res = ManualNameGen(10).getGivenLengthChains(chainsData=data,
                                                     lenChain=8)
        self.assertListEqual(res, [{'key': 'chainone', 'count': 0, 'chance': 0.0}, 
                                   {'key': 'chaintwo', 'count': 0, 'chance': 0.0}])
                
    @FunctionalClass.descript
    def test_getGivenLengthChains_checkingEmptyLength_expectedRaise(
            self) -> typ.NoReturn:
        '''
        Testing the method of finding a list of chains 
        of the given length.
        '''
        genObj = ManualNameGen()
                
        self.assertRaises(AssertionError, 
                          genObj.getGivenLengthChains, 
                          chainsData=[], lenChain=None)
                
    @FunctionalClass.descript
    def test_getGivenLengthChains_checkingNegativeLength_expectedRaise(
            self) -> typ.NoReturn:
        '''
        Testing the method of finding a list of chains 
        of the given length.
        '''
        genObj = ManualNameGen()
                
        self.assertRaises(AssertionError, 
                          genObj.getGivenLengthChains, 
                          chainsData=[], lenChain=-1)
                
    @FunctionalClass.descript
    def test_prepareFirstChainLetters_cutingLetters_expectedFirstLetters(
            self) -> typ.NoReturn:
        '''
        Testing the method of gets the first letters 
        in chains from rules.
        '''
        data = [{'key': 'onechain', 'count': 0, 'chance': 1.0}, 
                {'key': 'twochain', 'count': 0, 'chance': 2.0}, 
                {'key': 'anotherchain', 'count': 0, 'chance': 10.0}]
                
        res = ManualNameGen(10).prepareFirstChainLetters(chainsData=data)
        self.assertListEqual(res, [{'key': 'o', 'count': 0, 'chance': 1.0}, 
                                   {'key': 't', 'count': 0, 'chance': 2.0}, 
                                   {'key': 'a', 'count': 0, 'chance': 10.0}])
                
    @FunctionalClass.descript
    def test_cutChains_cutingLetters_expectedCroppedChains(
            self) -> typ.NoReturn:
        '''
        Testing the method of selects chains and discards 
        this received letter from each chain.
        '''
        data = [{'key': 'onechain', 'count': 0, 'chance': 1.0}, 
                {'key': 'twochain', 'count': 0, 'chance': 2.0}, 
                {'key': 'anotherchain', 'count': 0, 'chance': 10.0}]
                
        res = ManualNameGen(10).cutChains(chainsData=data,
                                          prewLetter='o')
        self.assertListEqual(res, [{'key': 'nechain', 
                                    'count': 0, 
                                    'chance': 1.0}])
                
    @FunctionalClass.descript
    def test_cutChains_checkingNotExistLetter_expectedEmptyList(
            self) -> typ.NoReturn:
        '''
        Testing the method of selects chains and discards 
        this received letter from each chain.
        '''
        data = [{'key': 'onechain', 'count': 0, 'chance': 1.0}, 
                {'key': 'twochain', 'count': 0, 'chance': 2.0}, 
                {'key': 'anotherchain', 'count': 0, 'chance': 10.0}]
                
        res = ManualNameGen(10).cutChains(chainsData=data,
                                          prewLetter='z')
        self.assertListEqual(res, [])
                
    @FunctionalClass.descript
    def test_cutChains_checkingNoneLetter_expectedRaise(
            self) -> typ.NoReturn:
        '''
        Testing the method of selects chains and discards 
        this received letter from each chain.
        '''
        genObj = ManualNameGen(10)
                
        self.assertRaises(AssertionError, 
                          genObj.cutChains, 
                          chainsData=[], prewLetter=None)
                
    @FunctionalClass.descript
    def test_prepareLettersRules_makingData_expectedData(
            self) -> typ.NoReturn:
        '''
        Testing the method of prepares rules by types.
        '''
        data = {'fcl': [{'key': 'a', 'range': (0, 10.0)}], 
                'acl': [], 
                'anl': []}
                
        res = ManualNameGen(10).prepareLettersRules(rulesData=data)
        self.assertListEqual(res, [(70.0, [{'key': 'a', 
                                            'range': (0, 10.0)}]),
                                   (18.0, []),
                                   (9.0, []),
                                   (3.0, None)
                                  ])
                
    @FunctionalClass.descript
    def test_prepareLettersRules_checkingEmptyFirstKey_expectedData(
            self) -> typ.NoReturn:
        '''
        Testing the method of prepares rules by types.
        '''
        data = {'fcl': [], 'acl': [], 'anl': []}
                
        res = ManualNameGen(10).prepareLettersRules(rulesData=data)
        self.assertListEqual(res, [(0.0, []),
                                   (18.0, []),
                                   (9.0, []),
                                   (3.0, None)])
                
    @FunctionalClass.descript
    def test_prepareLettersRules_checkingNotExistKey_expectedRaise(
            self) -> typ.NoReturn:
        '''
        Testing the method of prepares rules by types.
        '''
        genObj = ManualNameGen(10)
        data = {'fcl': [], 'acl': []}
                
        self.assertRaises(AssertionError, 
                          genObj.prepareLettersRules, 
                          rulesData=data)
                
    @FunctionalClass.descript
    def test_makeLetterRules_makingRules_expectedRules(
            self) -> typ.NoReturn:
        '''
        Testing the method of makes rules 
        for several letter variants, 
        chosen randomly according to their rules.
        '''
        data = [(70.0, [{'key': 'd', 'range': (0.0, 10.0)}]),
               (18.0, [{'key': 'b', 'range': (0.0, 11.0)},
                       {'key': 'f', 'range': (11.0, 12.0)}]),
               (9.0, [{'key': 'c', 'range': (0.0, 12.0)}]),
               (3.0, None)]
                
        res = ManualNameGen(10).makeLetterRules(chainType='consonant', 
                                                dataList=data)
        self.assertListEqual(res, [{'key': 'd', 'range': (0.0, 70.0)},
                                   {'key': 'b', 'range': (70.0, 88.0)},
                                   {'key': 'c', 'range': (88.0, 97.0)},
                                   {'key': 'j', 'range': (97.0, 100.0)}])
                
    @FunctionalClass.descript
    def test_makeLetterRules_checkingEmptyRule_expectedRules(
            self) -> typ.NoReturn:
        '''
        Testing the method of makes rules 
        for several letter variants, 
        chosen randomly according to their rules.
        '''
        data = [(70.0, [{'key': 'd', 'range': (0.0, 10.0)}]),
               (18.0, [{'key': 'b', 'range': (0.0, 11.0)},
                       {'key': 'f', 'range': (11.0, 12.0)}]),
               (9.0, []),
               (3.0, None)]
                
        res = ManualNameGen(10).makeLetterRules(chainType='consonant', 
                                                dataList=data)
        self.assertListEqual(res, [{'key': 'd', 'range': (0.0, 70.0)},
                                   {'key': 'b', 'range': (70.0, 88.0)},
                                   {'key': 'x', 'range': (88.0, 97.0)},
                                   {'key': 'b', 'range': (97.0, 100.0)}])
                
    @FunctionalClass.descript
    def test_getLettersRules_makingRules_expectedRules(
            self) -> typ.NoReturn:
        '''
        Testing the method of prepares and makes rules 
        for several variants of letters.
        '''
        data = {'fcl': [{'key': 'd', 'range': (0.0, 10.0)}], 
                'acl': [{'key': 'b', 'range': (0.0, 11.0)},
                       {'key': 'f', 'range': (11.0, 12.0)}], 
                'anl': [{'key': 'c', 'range': (0.0, 12.0)}]}
                
        res = ManualNameGen(10).getLettersRules(chainType='consonant', 
                                                rulesData=data)
        self.assertListEqual(res, [{'key': 'd', 'range': (0.0, 70.0)},
                                   {'key': 'b', 'range': (70.0, 88.0)},
                                   {'key': 'c', 'range': (88.0, 97.0)},
                                   {'key': 'j', 'range': (97.0, 100.0)}])
                
    @FunctionalClass.descript
    def test_getLettersRules_checkingEmptyRule_expectedRules(
            self) -> typ.NoReturn:
        '''
        Testing the method of prepares and makes rules 
        for several variants of letters.
        '''
        data = {'fcl': [{'key': 'd', 'range': (0.0, 10.0)}], 
                'acl': [{'key': 'b', 'range': (0.0, 11.0)},
                       {'key': 'f', 'range': (11.0, 12.0)}], 
                'anl': []}
                
        res = ManualNameGen(10).getLettersRules(chainType='consonant', 
                                                rulesData=data)
        self.assertListEqual(res, [{'key': 'd', 'range': (0.0, 70.0)},
                                   {'key': 'b', 'range': (70.0, 88.0)},
                                   {'key': 'x', 'range': (88.0, 97.0)},
                                   {'key': 'b', 'range': (97.0, 100.0)}])
                
    @FunctionalClass.descript
    def test_cutChance_recalculatingRanges_expectedRecalcRules(
            self) -> typ.NoReturn:
        '''
        Testing the method of reduces the chance of dropping 
        an already dropped letter and recalculates the ranges.
        '''
        data = [{'key': 'b', 'range': (0.0, 11.0)},
                {'key': 'f', 'range': (11.0, 12.0)}]
                
        res = ManualNameGen(10).cutChance(currLetter='b', 
                                          letterRules=data)
        self.assertListEqual(res, [{'key': 'b', 'range': (0.0, 0.11)},
                                   {'key': 'f', 'range': (0.11, 1.11)}])
                
    @FunctionalClass.descript
    def test_cutChance_checkingNotExistLetter_expectedRules(
            self) -> typ.NoReturn:
        '''
        Testing the method of reduces the chance of dropping 
        an already dropped letter and recalculates the ranges.
        '''
        data = [{'key': 'b', 'range': (0.0, 11.0)},
                {'key': 'f', 'range': (11.0, 12.0)}]
                
        res = ManualNameGen(10).cutChance(currLetter='c', 
                                          letterRules=data)
        self.assertListEqual(res, [{'key': 'b', 'range': (0.0, 11.0)},
                                   {'key': 'f', 'range': (11.0, 12.0)}])
                
    @FunctionalClass.descript
    def test_cutChance_checkingEmptyRules_expectedEmptyList(
            self) -> typ.NoReturn:
        '''
        Testing the method of reduces the chance of dropping 
        an already dropped letter and recalculates the ranges.
        '''
        res = ManualNameGen(10).cutChance(currLetter='b', 
                                          letterRules=[])
        self.assertListEqual(res, [])

###FINISH FunctionalBlock

###START MainBlock
def main() -> typ.NoReturn:
    pass
###FINISH Mainblock
