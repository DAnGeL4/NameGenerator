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

###FINISH FunctionalBlock

###START MainBlock
def main() -> typ.NoReturn:
    pass
###FINISH Mainblock
