###START ImportBlock
##systemImport
import typing as typ

##customImport
from tests.test_Service import FunctionalClass
from modules.nameGen import ManualNameGen_Stub
from modules.nameGen import ManualNameGen

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

###FINISH FunctionalBlock

###START MainBlock
def main() -> typ.NoReturn:
    pass
###FINISH Mainblock
