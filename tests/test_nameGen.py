###START ImportBlock
##systemImport
import typing as typ

##customImport
from tests.test_Service import FunctionalClass
from modules.nameGen import ManualNameGen_Stub

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

###FINISH FunctionalBlock

###START MainBlock
def main() -> typ.NoReturn:
    pass
###FINISH Mainblock
