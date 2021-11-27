###START ImportBlock
##systemImport
import ast
import types
import typing

##customImport
from configs.CFGNames import VOWELS_LETTERS, CONSONANTS_LETTERS
from tests.test_Service import FunctionalClass
from modules.nameAnalysis import AnalysysService, AnalyticLetters
from modules.nameAnalysis import AnalyticChains, AnalyticCombinations
from modules.nameAnalysis import Analysis

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
    initNamesAnalytics;
    initGlobNamesAnalytics;
    copyObjectData;
    isiterable;
    renameDictKey;
    getFirstUnknownDictKeyName;
    getLocalAnalyticData;
    getCountByAnalyticKey;
    getMaxCountByKey;
    getMaleNamesCount;
    getFemaleNamesCount;
    getSurnamesCount;
    getAllNamesCount;
    setRatingDataByLocalAnalytic;
    setCommonRattingData;
    calcChanceByKey;
    calculateNamesCountByLocalAnalytic;
    calcMaxNamesCount;
    calcAllChances;
    prepareRatingAnalytic;
    calculateCountByKey;
    calculateRatingByKey;
    increaceCountforAllSubkeys;
    calculateRatingforCommonSubkey;
    makeCommonRatingData;
    makeLocalAnalyticData.
    '''

    ##BEGIN ConstantBlock
    TestFiles = {
        'NameBaseInitialize.cfg': dict({'Races': [
            {'Elf': {'Genders': {
                'Female': {'Names': ['Zhuirentel']}, 
                'Male': {'Names': ['Venrie', 'Renvie']}
                }, 
                'Surnames': ['Windwalker']}}, 
            {'Ork': {'Genders': {
                'Female': {'Names': ['Aelene']}, 
                'Male': {'Names': ['Afamrail']}
                }, 
                'Surnames': ['Amaratharr', 'Armerat']}}
            ]}),
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
    def setUpClass(cls) -> typing.NoReturn:
        '''Set up for class.'''

        cls.printSetUpClassMsg()
        cls.createTestFiles()


    @classmethod
    def tearDownClass(cls) -> typing.NoReturn:
        '''Tear down for class.'''

        cls.removeTestFiles()
        cls.printTearDownClassMsg()


    def setUp(self) -> typing.NoReturn:
        '''Set up for test.'''

        self.printSetUpMethodMsg()
        nameBaseFile = str(self.TestFileDirectory + 'NameBaseInitialize.cfg')
        self.TestConstruction = AnalysysService(nameBaseFile)
        self.TestConstruction.raceNameKey = 'TestRace'
        self.TestConstruction.localAnalyticKey = 'Test_Analytic_key'
        self.TestConstruction.groupKey = 'Test_Group_Key'


    def tearDown(self) -> typing.NoReturn:
        '''Tear down for test.'''

        self.printTearDownMethodMsg()
        self.TestConstruction = None

    ##END PrepareBlock

    @FunctionalClass.descript
    def test_getBaseOfNames_checkingReadedData_expectedDict(
            self) -> typing.NoReturn:
        '''
        Testing read dictionary data from file.
        '''
        nameBaseFile = str(self.TestFileDirectory + 'NameBaseInitialize.cfg')
        self.TestConstruction.getBaseOfNames(nameBaseFile)

        res = self.TestConstruction.baseOfNames
        self.assertDictEqual(res, 
                        {'Races': [
                            {'Elf': {'Genders': {
                                'Female': {'Names': ['Zhuirentel']}, 
                                'Male': {'Names': ['Venrie', 'Renvie']}
                                }, 
                                'Surnames': ['Windwalker']}}, 
                            {'Ork': {'Genders': {
                                'Female': {'Names': ['Aelene']}, 
                                'Male': {'Names': ['Afamrail']}
                                }, 
                                'Surnames': ['Amaratharr', 'Armerat']}}
                            ]})
                        

    @FunctionalClass.descript
    def test_initNamesAnalytics_checkingCleringNamesDB_expectedEmptyDict(
            self) -> typing.NoReturn:
        '''
        Testing class variable cleanup.
        '''
        self.TestConstruction.tmp_NamesDB = dict({"some_key": "some_data"})
        self.TestConstruction.initNamesAnalytics()

        res = self.TestConstruction.tmp_NamesDB
        self.assertDictEqual(res, {})


    @FunctionalClass.descript
    def test_initNamesAnalytics_checkingStoredAnalyticData_expectedTemplate(
            self) -> typing.NoReturn:
        '''
        Testing getting Analytic template.
        '''
        self.TestConstruction.initNamesAnalytics()
        
        res = self.TestConstruction.tmp_NamesAnalytic
        self.assertDictEqual(res, 
                        {"tmp_Race":{
                            "Max_Names_Count": 0,
                            "Female_Names_Count": 0,
                            "Male_Names_Count": 0,
                            "Surnames_Count": 0,
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
                        }})

    
    @FunctionalClass.descript
    def test_initGlobNamesAnalytics_checkingStoredAnalyticData_expectedTemplate(
            self) -> typing.NoReturn:
        '''
        Testing getting global Analytic template.
        '''
        self.TestConstruction.initGlobNamesAnalytics()

        res = self.TestConstruction.globNamesAnalytic
        self.assertDictEqual(res, {"Analytics": {}})

    
    @FunctionalClass.descript
    def test_copyObjectData_checkingCopiedAnalyticValues_expectedRightValues(
            self) -> typing.NoReturn:
        '''
        Testing copied Analytic values. The rest of the variables are tested above.
        '''
        self.TestConstruction.raceNameKey = 'Test_Race'
        self.TestConstruction.groupKey = 'Test_GroupKey'
        self.TestConstruction.localAnalyticKey = 'Test_LocalKey'
        self.TestConstruction.FirstOnly = True

        nameBaseFile = str(self.TestFileDirectory + 'NameBaseInitialize.cfg')
        obj = AnalysysService(nameBaseFile)
        obj.copyObjectData(self.TestConstruction)

        res = {'raceNameKey': obj.raceNameKey, 'groupKey': obj.groupKey,
               'localAnalyticKey': obj.localAnalyticKey, 'FirstOnly': obj.FirstOnly}
        self.assertDictEqual(res, {'raceNameKey': 'Test_Race', 'groupKey': 'Test_GroupKey',
               'localAnalyticKey': 'Test_LocalKey', 'FirstOnly': True})

    
    @FunctionalClass.descript
    def test_isiterable_checkingIfIterate_expectedTrue(
            self) -> typing.NoReturn:
        '''
        Testing the iteration checking method.
        '''

        res = self.TestConstruction.isiterable([1, 2])
        self.assertEqual(res, True)

    
    @FunctionalClass.descript
    def test_renameDictKey_checkingRenamedKey_expectedRightKeyName(
            self) -> typing.NoReturn:
        '''
        Testing the method of rename key in dictionary.
        '''
        res = dict({'tmp_key': 'test_data'})
        self.TestConstruction.renameDictKey(res, 'new_tested_key', 'tmp_key')

        self.assertDictEqual(res, {'new_tested_key': 'test_data'})

    
    @FunctionalClass.descript
    def test_getFirstUnknownDictKeyName_checkingKeyName_expectedRightKeyName(
            self) -> typing.NoReturn:
        '''
        Testing of getting key from dictionary with only one key.
        '''
        test_data = dict({'tested_key': 'test_data'})

        res = self.TestConstruction.getFirstUnknownDictKeyName(test_data)
        self.assertEqual(res, 'tested_key')

    
    @FunctionalClass.descript
    def test_getLocalAnalyticData_checkingKeyName_expectedRightKeyName(
            self) -> typing.NoReturn:
        '''
        Testing of getting local analytic data for current local analytic key.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        NamesAnalyticData['TestRace'] = self.leaveKeys(['Test_Analytic_key'], 
                                                NamesAnalyticData['TestRace'])
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Test_Analytic_key'] = {'Test_Group_Key': {
                    'Test_local_Key': {'Count': 2, 'Chance': 100.0,}} }

        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData

        res = self.TestConstruction.getLocalAnalyticData()
        self.assertDictEqual(res, {'Test_Group_Key': {'Test_local_Key': {
                                    'Count': 2, 'Chance': 100.0,}} })
    
    
    @FunctionalClass.descript
    def test_getCountByAnalyticKey_checkingCountDataByKey_expectedRightCount(
            self) -> typing.NoReturn:
        '''
        Testing of getting count data from dictionary by analytic and local key.
        Used curent keys: self.raceNameKey, self.localAnalyticKey, self.groupKey.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Test_Analytic_key'] = {'Test_Group_Key': {
                    'Test_local_Key': {'Count': 2, 'Chance': 100.0,}} }

        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData

        res = self.TestConstruction.getCountByAnalyticKey('Test_local_Key')
        self.assertEqual(res, 2)
    

    @FunctionalClass.descript
    def test_getMaxCountByKey_checkingMaxCountDataByKey_expectedRightCount(
            self) -> typing.NoReturn:
        '''
        Testing of getting max count data from dictionary by analytic key.
        Used curent keys: self.raceNameKey.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Test_Max_Count_Key'] = 3

        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData

        res = self.TestConstruction.getMaxCountByKey('Test_Max_Count_Key')
        self.assertEqual(res, 3)
    

    @FunctionalClass.descript
    def test_getMaleNamesCount_checkingMaleNamesCountData_expectedRightCount(
            self) -> typing.NoReturn:
        '''
        Testing of getting male names count data from dictionary by analytic key.
        Used curent keys: self.raceNameKey.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Male_Names_Count'] = 4
        
        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData

        res = self.TestConstruction.getMaleNamesCount()
        self.assertEqual(res, 4)
    

    @FunctionalClass.descript
    def test_getFemaleNamesCount_checkingFemaleNamesCountData_expectedRightCount(
            self) -> typing.NoReturn:
        '''
        Testing of getting female names count data from dictionary by analytic key.
        Used curent keys: self.raceNameKey.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Female_Names_Count'] = 5
        
        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData

        res = self.TestConstruction.getFemaleNamesCount()
        self.assertEqual(res, 5)
    

    @FunctionalClass.descript
    def test_getSurnamesCount_checkingSurnamesCountData_expectedRightCount(
            self) -> typing.NoReturn:
        '''
        Testing of getting surnames count data from dictionary by analytic key.
        Used curent keys: self.raceNameKey.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Surnames_Count'] = 6
        
        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData

        res = self.TestConstruction.getSurnamesCount()
        self.assertEqual(res, 6)
    

    @FunctionalClass.descript
    def test_getAllNamesCount_checkingAllNamesCountData_expectedRightCount(
            self) -> typing.NoReturn:
        '''
        Testing of getting all names count data from dictionary by analytic key.
        Used curent keys: self.raceNameKey.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Max_Names_Count'] = 7
        
        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData

        res = self.TestConstruction.getAllNamesCount()
        self.assertEqual(res, 7)
    

    @FunctionalClass.descript
    def test_setRatingDataByLocalAnalytic_checkingRatingDataStorage_expectedRatingData(
            self) -> typing.NoReturn:
        '''
        Testing of the correct saving of rating data in tmp_NamesAnalytic.
        Used curent keys: self.raceNameKey, self.localAnalyticKey, self.groupKey.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Test_Analytic_key'] = {'Test_Group_Key': {
                    'Test_local_Key': {'Count': 0, 'Chance': 0,}} }

        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData

        ratingData = dict({'Test_Group_Key': {
                                'Test_local_Key': {'Count': 3, 'Chance': 100,}
                                }})
        self.TestConstruction.setRatingDataByLocalAnalytic(ratingData)

        res = self.TestConstruction.tmp_NamesAnalytic['TestRace']['Test_Analytic_key'][
                                                        'Test_Group_Key']
        self.assertDictEqual(res, {'Test_local_Key': {'Count': 3, 'Chance': 100,}})
    

    @FunctionalClass.descript
    def test_setRatingDataByLocalAnalytic_checkingRatingDataStorageBySubkey_expectedRatingData(
            self) -> typing.NoReturn:
        '''
        Testing of the correct saving of rating data in tmp_NamesAnalytic by subkey.
        Used curent keys: self.raceNameKey, self.localAnalyticKey, self.groupKey.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Test_Analytic_key'] = {'Test_Subkey':{'Test_Group_Key': {
                        'Test_local_Key': { 'Count': 0, 'Chance': 0,}}} }

        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData

        ratingData = dict({'Test_Group_Key': {
                                'Test_local_Key': {'Count': 4, 'Chance': 100,}
                                }})
        self.TestConstruction.setRatingDataByLocalAnalytic(ratingData, subKey='Test_Subkey')

        res = self.TestConstruction.tmp_NamesAnalytic['TestRace']['Test_Analytic_key'][
                                                        'Test_Subkey']['Test_Group_Key']
        self.assertDictEqual(res, {'Test_local_Key': {'Count': 4, 'Chance': 100,}})
    

    @FunctionalClass.descript
    def test_setCommonRattingData_checkingRatingDataStorage_expectedRatingData(
            self) -> typing.NoReturn:
        '''
        Testing of the correct saving of rating data for only common group key 
        in tmp_NamesAnalytic.
        Used curent keys: self.raceNameKey, self.localAnalyticKey, self.groupKey.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        NamesAnalyticData['TestRace']['Test_Analytic_key'] = dict()

        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData

        ratingData = dict({'Common': {
                                'Test_local_Key': {'Count': 3, 'Chance': 100,}
                                }})
        self.TestConstruction.setCommonRattingData(ratingData)

        res = self.TestConstruction.tmp_NamesAnalytic['TestRace']['Test_Analytic_key']
        self.assertDictEqual(res, {'Common': {'Test_local_Key': {'Count': 3, 'Chance': 100,}} })
    

    @FunctionalClass.descript
    def test_calcChanceByKey_checkingCalculating_expectedRatingChance(
            self) -> typing.NoReturn:
        '''
        Testing of calculating chance by the count and common count.
        '''
        res = self.TestConstruction.calcChanceByKey(count=5, countByGroupKey=13)
        self.assertAlmostEqual(res, 38.46, places=2)
                                        

    @FunctionalClass.descript
    def test_calculateNamesCountByLocalAnalytic_checkingCalculating_expectedRatingCount(
            self) -> typing.NoReturn:
        '''
        Testing of calculating new common count by the getting count and old common count.
        Used curent keys: self.raceNameKey.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Test_Common_Count'] = 14

        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.calculateNamesCountByLocalAnalytic(8, 'Test_Common_Count')

        res = self.TestConstruction.tmp_NamesAnalytic['TestRace']['Test_Common_Count']
        self.assertEqual(res, 22)
            

    @FunctionalClass.descript
    def test_calcMaxNamesCount_checkingCalculatingMaleNamesCount_expectedRightCount(
            self) -> typing.NoReturn:
        '''
        Testing of calculating male names count.
        Used curent keys: self.raceNameKey, self.groupKey, self.tmp_NamesDB.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        
        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.tmp_NamesDB['Male'] = ['Name1', 'Name2']
        self.TestConstruction.groupKey = 'Male'

        self.TestConstruction.calcMaxNamesCount()

        res = self.TestConstruction.tmp_NamesAnalytic['TestRace']['Male_Names_Count']
        self.assertEqual(res, 2)
            

    @FunctionalClass.descript
    def test_calcMaxNamesCount_checkingCalculatingFemaleNamesCount_expectedRightCount(
            self) -> typing.NoReturn:
        '''
        Testing of calculating female names count.
        Used curent keys: self.raceNameKey, self.groupKey, self.tmp_NamesDB.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)

        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.tmp_NamesDB['Female'] = ['Name1', 'Name2', 'Name3']
        self.TestConstruction.groupKey = 'Female'

        self.TestConstruction.calcMaxNamesCount()

        res = self.TestConstruction.tmp_NamesAnalytic['TestRace']['Female_Names_Count']
        self.assertEqual(res, 3)
            

    @FunctionalClass.descript
    def test_calcMaxNamesCount_checkingCalculatingSurnamesCount_expectedRightCount(
            self) -> typing.NoReturn:
        '''
        Testing of calculating surnames count.
        Used curent keys: self.raceNameKey, self.groupKey, self.tmp_NamesDB.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        
        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.tmp_NamesDB['Surnames'] = ['Name1', 'Name2', 
                                                         'Name3', 'Name4']
        self.TestConstruction.groupKey = 'Surnames'

        self.TestConstruction.calcMaxNamesCount()

        res = self.TestConstruction.tmp_NamesAnalytic['TestRace']['Surnames_Count']
        self.assertEqual(res, 4)
            

    @FunctionalClass.descript
    def test_calcMaxNamesCount_checkingCalculatingMaxNamesCount_expectedRightCount(
            self) -> typing.NoReturn:
        '''
        Testing of calculating max names count for all genders.
        Used curent keys: self.raceNameKey, self.groupKey, self.tmp_NamesDB.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Max_Names_Count'] = 5
                    
        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.tmp_NamesDB['Surnames'] = ['Name1', 'Name2', 
                                                         'Name3', 'Name4']
        self.TestConstruction.groupKey = 'Surnames'

        self.TestConstruction.calcMaxNamesCount()

        res = self.TestConstruction.tmp_NamesAnalytic['TestRace']['Max_Names_Count']
        self.assertEqual(res, 9)


    @FunctionalClass.descript
    def test_calcAllChances_checkingCalculatingMaxNMaleChances_expectedRightChance(
            self) -> typing.NoReturn:
        '''
        Testing of calculating male and common chances.
        Used curent keys: self.raceNameKey, self.groupKey.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Male_Names_Count'] = 2

        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.groupKey = 'Male'
        count = 1

        res = self.TestConstruction.calcAllChances(count)
        self.assertEqual(res, 50.0)


    @FunctionalClass.descript
    def test_calcAllChances_checkingCalculatingMaxNFemaleChances_expectedRightChance(
            self) -> typing.NoReturn:
        '''
        Testing of calculating female and common chances.
        Used curent keys: self.raceNameKey, self.groupKey.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Female_Names_Count'] = 3

        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.groupKey = 'Female'
        count = 2

        res = self.TestConstruction.calcAllChances(count)
        self.assertEqual(res, 66.66666666666667)


    @FunctionalClass.descript
    def test_calcAllChances_checkingCalculatingMaxNSurnamesChances_expectedRightChance(
            self) -> typing.NoReturn:
        '''
        Testing of calculating surnames and common chances.
        Used curent keys: self.raceNameKey, self.groupKey.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Surnames_Count'] = 5

        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.groupKey = 'Surnames'
        count = 3

        res = self.TestConstruction.calcAllChances(count)
        self.assertEqual(res, 60.0)


    @FunctionalClass.descript
    def test_prepareRatingAnalytic_checkingCreatingAnalyticData_expectedPreaperedTemplate(
            self) -> typing.NoReturn:
        '''
        Testing of creating right analytic data from analytic template.
        '''

        res = self.TestConstruction.prepareRatingAnalytic('Test_local_Key')
        self.assertDictEqual(res, {'Test_local_Key': {'Count': 0, 'Chance': 0,}})

    @FunctionalClass.descript
    def test_calculateCountByKey_checkingCalculatingRating_expectedCorrectCount(
            self) -> typing.NoReturn:
        '''
        Testing of creating rating data by calculating the key count.
        Used curent keys: self.raceNameKey, self.localAnalyticKey, self.groupKey.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Male_Names_Count'] = 2
        testRaceData['Test_Analytic_key'] = {'Male': {
                    'Test_local_Key': {'Count': 1, 'Chance': 0.0,}} }
        
        ratingData = NamesAnalyticData['TestRace']['Test_Analytic_key']

        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.groupKey = 'Male'

        res = self.TestConstruction.calculateCountByKey('Test_local_Key', ratingData)
        self.assertDictEqual(res, {'Male': {
                                        'Test_local_Key': {'Count': 2, 'Chance': 0.0,}
                                        }})


    @FunctionalClass.descript
    def test_calculateRatingByKey_checkingCalculatingRating_expectedRatingData(
            self) -> typing.NoReturn:
        '''
        Testing of calculating rating data for the passed key.
        Used curent keys: self.raceNameKey, self.localAnalyticKey, self.groupKey.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Male_Names_Count'] = 2
        testRaceData['Test_Analytic_key'] = {'Male': {
                    'Test_local_Key': {'Count': 1, 'Chance': 0.0,}} }
        
        ratingData = NamesAnalyticData['TestRace']['Test_Analytic_key']

        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.groupKey = 'Male'

        res = self.TestConstruction.calculateRatingByKey('Test_local_Key', ratingData)
        self.assertDictEqual(res, {'Male': {
                                        'Test_local_Key': {'Count': 1, 'Chance': 50.0,}
                                        }})


    @FunctionalClass.descript
    def test_calculateRatingforCommonSubkey_checkingCalculatingRating_expectedRatingData(
            self) -> typing.NoReturn:
        '''
        Testing of calculating rating data for the common key.
        Used curent keys: self.raceNameKey, self.localAnalyticKey, self.groupKey.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Max_Names_Count'] = 2
        testRaceData['Test_Analytic_key'] = {'Common': {
                    'Test_local_Key': {'Count': 1, 'Chance': 0.0,}} }

        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        
        ratingData = NamesAnalyticData['TestRace']['Test_Analytic_key']

        res = self.TestConstruction.calculateRatingforCommonSubkey('Test_local_Key', ratingData)
        self.assertDictEqual(res, {'Common': {
                                        'Test_local_Key': {'Count': 1, 'Chance': 50.0,}
                                        }})


    @FunctionalClass.descript
    def test_increaceCountforAllSubkeys_checkingIncreacingRating_expectedRatingData(
            self) -> typing.NoReturn:
        '''
        Testing of increacing count by all subkeys inside current local analytic key.
        Used curent keys: self.raceNameKey, self.localAnalyticKey, self.groupKey.
        '''
        destinationData = dict({'tstkey': {'Count': 3, 'Chance': 25.0,}})
        sourceData = dict({ 'tstkey': {'Count': 4, 'Chance': 75.0,}})

        res = self.TestConstruction.increaceCountforAllSubkeys(destinationData['tstkey'], 
                                                                sourceData['tstkey'])
        res = destinationData
        self.assertDictEqual(res, {'tstkey': {'Count': 7, 'Chance': 100.0, }})


    @FunctionalClass.descript
    def test_makeCommonRatingData_checkingCreatingDataByAnalyticKey_expectedAnalyticData(
            self) -> typing.NoReturn:
        '''
        Testing the creation and calculating analytic data for common group 
        key by current the analytic key (#localAnalyticKey).
        Used curent keys: self.raceNameKey, self.localAnalyticKey, 
        self.groupKey, self.tmp_NamesDB.
        '''

        def tmp_FirstLettersFunc(name: str) -> str:
            '''Gets first letter of name.'''
            firstLetter = str(name)[0]
            return firstLetter

        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Max_Names_Count'] = 10
        testRaceData['Male_Names_Count'] = 2
        testRaceData['First_letters'] = {'Male': {
                                            'V': {'Count': 1, 'Chance': 50.0,}, 
                                            'R': {'Count': 1, 'Chance': 50.0,}
                                            }}
      
        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.tmp_NamesDB['Male'] = ['Ve', 'Re']
        self.TestConstruction.localAnalyticKey = 'First_letters'
        self.TestConstruction.groupKey = 'Male'

        self.TestConstruction.makeCommonRatingData()

        res = self.TestConstruction.tmp_NamesAnalytic['TestRace']['First_letters']
        self.assertDictEqual(res,  {'Male': {
                                        'V': {'Count': 1, 'Chance': 50.0}, 
                                        'R': {'Count': 1, 'Chance': 50.0}}, 
                                    'Common': {
                                        'V': {'Count': 1, 'Chance': 10.0}, 
                                        'R': {'Count': 1, 'Chance': 10.0}}})


    @FunctionalClass.descript
    def test_makeLocalAnalyticData_checkingCreatingDataByAnalyticKey_expectedAnalyticData(
            self) -> typing.NoReturn:
        '''
        Testing the creation of analytic data by the passed temporary key 
        generation function for the analytic key.
        Used curent keys: self.raceNameKey, self.localAnalyticKey, 
        self.groupKey, self.tmp_NamesDB.
        '''

        def tmp_FirstLettersFunc(name: str) -> str:
            '''Gets first letter of name.'''
            firstLetter = str(name)[0]
            return firstLetter

        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Max_Names_Count'] = 10
        testRaceData['Male_Names_Count'] = 2
        testRaceData['First_letters'] = {'Male': {} }
      
        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.tmp_NamesDB['Male'] = ['Ve', 'Re']
        self.TestConstruction.localAnalyticKey = 'First_letters'
        self.TestConstruction.groupKey = 'Male'

        self.TestConstruction.makeLocalAnalyticData(tmp_FirstLettersFunc)

        res = self.TestConstruction.tmp_NamesAnalytic['TestRace']['First_letters']
        self.assertDictEqual(res, {'Male': {
                                        'V': {'Count': 1, 'Chance': 50.0,}, 
                                        'R': {'Count': 1, 'Chance': 50.0,}
                                        },
                                    'Common':{
                                        'V': {'Count': 1, 'Chance': 10.0,}, 
                                        'R': {'Count': 1, 'Chance': 10.0,}
                                    }})


    @FunctionalClass.descript
    def test_makeLocalAnalyticData_checkingCreatingDataByAnalyticSubkey_expectedAnalyticData(
            self) -> typing.NoReturn:
        '''
        Testing the creation of analytic data by the passed temporary key 
        generation function for the analytic subkey.
        Used curent keys: self.raceNameKey, self.localAnalyticKey, 
        self.groupKey, self.tmp_NamesDB.
        '''

        def tmp_FirstLettersFunc(name: str) -> str:
            '''Gets first letter of name.'''
            firstLetter = str(name)[0]
            return firstLetter

        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Max_Names_Count'] = 10
        testRaceData['Male_Names_Count'] = 2
        testRaceData['First_letters'] = {'Test_Subkey':{'Male': {} }}
       
        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.tmp_NamesDB['Male'] = ['Ve', 'Re']
        self.TestConstruction.localAnalyticKey = 'First_letters'
        self.TestConstruction.groupKey = 'Male'

        self.TestConstruction.makeLocalAnalyticData(tmp_FirstLettersFunc, subKey='Test_Subkey')

        res = self.TestConstruction.tmp_NamesAnalytic['TestRace']['First_letters']['Test_Subkey']
        self.assertDictEqual(res, {'Male': {
                                        'V': {'Count': 1, 'Chance': 50.0,}, 
                                        'R': {'Count': 1, 'Chance': 50.0,}
                                        },
                                    'Common':{
                                        'V': {'Count': 1, 'Chance': 10.0,}, 
                                        'R': {'Count': 1, 'Chance': 10.0, }
                                    }})


    @FunctionalClass.descript
    def test_makeLocalAnalyticData_checkingCreatingIterationDataByAnalyticKey_expectedAnalyticData(
            self) -> typing.NoReturn:
        '''
        Testing the creation of analytic data by the passed temporary 
        iteraion keys generation function for the analytic key.
        Used curent keys: self.raceNameKey, self.localAnalyticKey, 
        self.groupKey, self.tmp_NamesDB.
        '''

        def tmp_getAllLettersFunc(name: str) -> str:
            '''Gets each letter of name.'''
            for letter in name:
                edtLetter = str(letter).lower()
                yield edtLetter

        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Max_Names_Count'] = 10
        testRaceData['Male_Names_Count'] = 2
        testRaceData['Letters'] = {'Male': {}}
        
        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.tmp_NamesDB['Male'] = ['Ve', 'Re']
        self.TestConstruction.localAnalyticKey = 'Letters'
        self.TestConstruction.groupKey = 'Male'

        self.TestConstruction.makeLocalAnalyticData(tmp_getAllLettersFunc)

        res = self.TestConstruction.tmp_NamesAnalytic['TestRace']['Letters']
        self.assertDictEqual(res, {'Male': {
                                        'v': {'Count': 1, 'Chance': 50.0,}, 
                                        'e': {'Count': 2, 'Chance': 100.0,}, 
                                        'r': {'Count': 1, 'Chance': 50.0,}
                                        },
                                    'Common': {
                                        'v': {'Count': 1, 'Chance': 10.0,}, 
                                        'e': {'Count': 2, 'Chance': 20.0,}, 
                                        'r': {'Count': 1, 'Chance': 10.0,}
                                        }
                                    })


class AnalyticLetters_Test(FunctionalClass):
    '''
    Testing next methods of class #AnalyticLetters:
    getFirstLetters;
    getFirstLettersMaxCountByKey;
    setFirstLettersMaxCountByKey;
    calcFirstLetters;
    makeNameLettersCountData;
    makeVowelsCountData;
    makeConsonantsCountData;
    makeFirstLetterCountData;
    makeAllLettersData;
    makeNameEndingsData;
    '''

    ##BEGIN ConstantBlock
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
    def setUpClass(cls) -> typing.NoReturn:
        '''Set up for class.'''

        cls.printSetUpClassMsg()
        cls.createTestFiles()


    @classmethod
    def tearDownClass(cls) -> typing.NoReturn:
        '''Tear down for class.'''

        cls.removeTestFiles()
        cls.printTearDownClassMsg()


    def setUp(self) -> typing.NoReturn:
        '''Set up for test.'''

        self.printSetUpMethodMsg()
        tmp_Construction = AnalysysService()
        tmp_Construction.raceNameKey = 'TestRace'
        tmp_Construction.localAnalyticKey = 'Test_Analytic_key'
        tmp_Construction.groupKey = 'Test_Group_Key'

        self.TestConstruction = AnalyticLetters(tmp_Construction)


    def tearDown(self) -> typing.NoReturn:
        '''Tear down for test.'''

        self.printTearDownMethodMsg()
        self.TestConstruction = None

    ##END PrepareBlock


    @FunctionalClass.descript
    def test_getFirstLetters_checkingGettingDataByFirstLettersKey_expectedFirstLettersList(
            self) -> typing.NoReturn:
        '''
        Testing the get method of keys by First_Letters key from 
        names analytic.
        Used curent keys: self.raceNameKey, self.groupKey.
        '''        
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['First_Letters'] = {'Male': {
                        'V': {'Count': 0, 'Chance': 0.0,}, 
                        'R': {'Count': 0, 'Chance': 0.0,} }
                    }

        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.groupKey = 'Male'

        res = self.TestConstruction.getFirstLetters()
        self.assertListEqual(res, ['V', 'R'])


    @FunctionalClass.descript
    def test_getFirstLettersMaxCountByKey_checkingGettingCountByFirstLettersSubkey_expectedFirstLettersCount(
            self) -> typing.NoReturn:
        '''
        Testing the get method of vowels or consonants count by 
        First_Letters subkey from names analytic.
        Used curent keys: self.raceNameKey.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['First_Letters'] = {'Vowels_Count': 0, 'Consonants_Count': 4,
                    'Male': {
                        'V': {'Count': 0, 'Chance': 0.0,}, 
                        'R': {'Count': 0, 'Chance': 0.0,} }
                }

        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData

        res = self.TestConstruction.getFirstLettersMaxCountByKey('Consonants_Count')
        self.assertEqual(res, 4)


    @FunctionalClass.descript
    def test_setFirstLettersMaxCountByKey_checkingSettingCountByFirstLettersSubkey_expectedRightCount(
            self) -> typing.NoReturn:
        '''
        Testing the set method of vowels or consonants count by 
        First_Letters subkey from names analytic.
        Used curent keys: self.raceNameKey.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['First_Letters'] = {'Vowels_Count': 0, 'Consonants_Count': 4,
                    'Male': {
                        'V': {'Count': 0, 'Chance': 0.0,}, 
                        'R': {'Count': 0, 'Chance': 0.0,} }
                }
      
        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData

        self.TestConstruction.setFirstLettersMaxCountByKey('Vowels_Count', 6)

        res = self.TestConstruction.tmp_NamesAnalytic['TestRace']['First_Letters']['Vowels_Count']
        self.assertEqual(res, 6)


    @FunctionalClass.descript
    def test_calcFirstLetters_checkingCalculatingCountOfFirstLetters_expectedRightCount(
            self) -> typing.NoReturn:
        '''
        Testing calculating of vowels and consonants first letters 
        from names analytic.
        Used curent keys: self.raceNameKey, self.localAnalyticKey, 
        self.groupKey.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['First_Letters'] = {'Vowels_Count': 6, 'Consonants_Count': 4,  
                    'Male': {
                        'V': {'Count': 1, 'Chance': 0.0,}, 
                        'R': {'Count': 1, 'Chance': 0.0,},
                        'A': {'Count': 2, 'Chance': 0.0,}, }
                }
  
        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.localAnalyticKey = 'First_Letters'
        self.TestConstruction.groupKey = 'Male'

        self.TestConstruction.calcFirstLetters()
        
        vowels = self.TestConstruction.tmp_NamesAnalytic['TestRace']['First_Letters']['Vowels_Count']
        consonants = self.TestConstruction.tmp_NamesAnalytic['TestRace']['First_Letters']['Consonants_Count']
        res = tuple((vowels, consonants))
        self.assertTupleEqual(res, (8, 6))


    @FunctionalClass.descript
    def test_makeNameLettersCountData_checkingMakingCountOfLenLetters_expectedRightData(
            self) -> typing.NoReturn:
        '''
        Testing the making method of names lenght and their repeats 
        amount from names DB.
        Used curent keys: self.raceNameKey, self.localAnalyticKey, 
        self.groupKey, self.tmp_NamesDB.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Max_Names_Count'] = 10
        testRaceData['Male_Names_Count'] = 3
        testRaceData['Name_Letters_Count'] = dict()
        
        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.tmp_NamesDB['Male'] = ['Ve', 'Re', 'Al']
        self.TestConstruction.groupKey = 'Male'

        self.TestConstruction.makeNameLettersCountData()
        
        res = self.TestConstruction.tmp_NamesAnalytic['TestRace']['Name_Letters_Count']
        self.assertDictEqual(res, {'Male':{
                                        '2': {'Count': 3, 'Chance': 100.0,}
                                        },
                                    'Common':{
                                        '2': {'Count': 3, 'Chance': 30.0, }
                                    }})


    @FunctionalClass.descript
    def test_makeVowelsCountData_checkingMakingCountOfLenLetters_expectedRightData(
            self) -> typing.NoReturn:
        '''
        Testing the method of making data with vowels amount in 
        names and their repeats amount from names DB.
        Used curent keys: self.raceNameKey, self.localAnalyticKey, 
        self.groupKey, self.tmp_NamesDB.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Max_Names_Count'] = 10
        testRaceData['Male_Names_Count'] = 3
        testRaceData['Vowels_Count'] = dict()
      
        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.tmp_NamesDB['Male'] = ['Vei', 'Rei', 'Alr']
        self.TestConstruction.groupKey = 'Male'

        self.TestConstruction.makeVowelsCountData()
        
        res = self.TestConstruction.tmp_NamesAnalytic['TestRace']['Vowels_Count']
        self.assertDictEqual(res, {'Male':{
                                        1: {'Count': 1, 'Chance': 33.333333333333336,},
                                        2: {'Count': 2, 'Chance': 66.66666666666667,},
                                        },
                                    'Common':{
                                        1: {'Count': 1, 'Chance': 10.0,},
                                        2: {'Count': 2, 'Chance': 20.0,},
                                    }})


    @FunctionalClass.descript
    def test_makeConsonantsCountData_checkingMakingCountOfLenLetters_expectedRightData(
            self) -> typing.NoReturn:
        '''
        Testing the method of making data with consonants amount in 
        names and their repeats amount from names DB.
        Used curent keys: self.raceNameKey, self.localAnalyticKey, 
        self.groupKey, self.tmp_NamesDB.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Max_Names_Count'] = 10
        testRaceData['Male_Names_Count'] = 3
        testRaceData['Consonants_Count'] = dict()
    
        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.tmp_NamesDB['Male'] = ['Vei', 'Rei', 'Alr']
        self.TestConstruction.groupKey = 'Male'

        self.TestConstruction.makeConsonantsCountData()
        
        res = self.TestConstruction.tmp_NamesAnalytic['TestRace']['Consonants_Count']
        self.assertDictEqual(res, {'Male':{
                                        1: {'Count': 2, 'Chance': 66.66666666666667,},
                                        2: {'Count': 1, 'Chance': 33.333333333333336,},
                                        },
                                    'Common':{
                                        1: {'Count': 2, 'Chance': 20.0,},
                                        2: {'Count': 1, 'Chance': 10.0,},
                                    }})


    @FunctionalClass.descript
    def test_makeFirstLetterCountData_checkingMakingFirstLettersData_expectedRightDataNCount(
            self) -> typing.NoReturn:
        '''
        Testing the method of making data with first letters in names 
        and their repeats amount from names DB; counts of vowels 
        and consonant first letters.
        Used curent keys: self.raceNameKey, self.localAnalyticKey, 
        self.groupKey, self.tmp_NamesDB.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Max_Names_Count'] = 10
        testRaceData['Male_Names_Count'] = 3
        testRaceData['First_Letters'] = {'Vowels_Count': 0, 'Consonants_Count': 0,}

        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.tmp_NamesDB['Male'] = ['Vei', 'Rei', 'Alr']
        self.TestConstruction.groupKey = 'Male'

        self.TestConstruction.makeFirstLetterCountData()
        
        res = self.TestConstruction.tmp_NamesAnalytic['TestRace']['First_Letters']
        self.assertDictEqual(res, {'Vowels_Count': 1, 
                                    'Consonants_Count': 2,
                                    'Male': {
                                        'V': {'Count': 1, 'Chance': 33.333333333333336,}, 
                                        'R': {'Count': 1, 'Chance': 33.333333333333336,}, 
                                        'A': {'Count': 1, 'Chance': 33.333333333333336,},
                                        },
                                    'Common': {
                                        'V': {'Count': 1, 'Chance': 10.0,}, 
                                        'R': {'Count': 1, 'Chance': 10.0,}, 
                                        'A': {'Count': 1, 'Chance': 10.0,},
                                    }})


    @FunctionalClass.descript
    def test_makeAllLettersData_checkingMakingAllLettersData_expectedRightData(
            self) -> typing.NoReturn:
        '''
        Testing the method of making data with all letters, used in 
        names, and their repeats amount from names DB.
        Used curent keys: self.raceNameKey, self.localAnalyticKey, 
        self.groupKey, self.tmp_NamesDB.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Max_Names_Count'] = 10
        testRaceData['Male_Names_Count'] = 3
        testRaceData['Letters'] = dict()
      
        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.tmp_NamesDB['Male'] = ['Ve', 'Re', 'Al']
        self.TestConstruction.groupKey = 'Male'

        self.TestConstruction.makeAllLettersData()
        
        res = self.TestConstruction.tmp_NamesAnalytic['TestRace']['Letters']
        self.assertDictEqual(res, {'Male': {
                                        'v': {'Count': 1, 'Chance': 33.333333333333336,}, 
                                        'e': {'Count': 2, 'Chance': 66.66666666666667,}, 
                                        'r': {'Count': 1, 'Chance': 33.333333333333336,}, 
                                        'a': {'Count': 1, 'Chance': 33.333333333333336,}, 
                                        'l': {'Count': 1, 'Chance': 33.333333333333336,},
                                        },
                                    'Common': {
                                        'v': {'Count': 1, 'Chance': 10.0,}, 
                                        'e': {'Count': 2, 'Chance': 20.0,}, 
                                        'r': {'Count': 1, 'Chance': 10.0,}, 
                                        'a': {'Count': 1, 'Chance': 10.0,}, 
                                        'l': {'Count': 1, 'Chance': 10.0,},
                                    }})


    @FunctionalClass.descript
    def test_makeNameEndingsData_checkingMakingNameEndingsData_expectedRightData(
            self) -> typing.NoReturn:
        '''
        Testing the method of making data with combinations of two 
        adjacent letters chains from the ends of names, includings 
        one letter chains, and their repeats amount from names DB.
        Used curent keys: self.raceNameKey, self.localAnalyticKey, 
        self.groupKey, self.tmp_NamesDB.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Max_Names_Count'] = 10
        testRaceData['Male_Names_Count'] = 3
        testRaceData['Name_Endings'] = dict()
    
        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.tmp_NamesDB['Male'] = ['Veiste', 'Reiste', 'Alrest']
        self.TestConstruction.groupKey = 'Male'

        self.TestConstruction.makeNameEndingsData()
        
        res = self.TestConstruction.tmp_NamesAnalytic['TestRace']['Name_Endings']
        self.assertDictEqual(res, {'Male': {
                                        'eiste': {'Count': 2, 'Chance': 66.66666666666667,}, 
                                        'lrest': {'Count': 1, 'Chance': 33.333333333333336,},
                                        },
                                    'Common': {
                                        'eiste': {'Count': 2, 'Chance': 20.0,}, 
                                        'lrest': {'Count': 1, 'Chance': 10.0,},
                                    }})


class AnalyticChains_Test(FunctionalClass):
    '''
    Testing next methods of class #AnalyticChains:
    nullifyCount;
    prepareChainsAnalytic;
    getChainsDataByLocalAnalytic;
    makeChainList;
    getChain;
    getChainCount;
    sortChainsByLength;
    calcChainMaxCountInName;
    getChainMaxCountKey;
    getChainCountDataByLocalAnalytic;
    getNullifyedChainCountDataByLocalAnalytic;
    setLocalChainsAnalyticData;
    calcChainsCountInNames;
    sortChainsByLength;
    calcChainFrequency;
    prepareDataByChainsAnalyticTemplate;
    callcRatingOfChainsBySubkey;
    calcRatingForAllChainsSubkeysByLocalAnalytic;
    createChainsDataForAllSubkeysByLocalAnalytic;
    calcChainsDataForAllSubkeysByLocalAnalytic;
    makeVowelsChainsAllData;
    makeConsonantsChainsAllData;
    '''

    ##BEGIN ConstantBlock
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
    def setUpClass(cls) -> typing.NoReturn:
        '''Set up for class.'''

        cls.printSetUpClassMsg()
        cls.createTestFiles()


    @classmethod
    def tearDownClass(cls) -> typing.NoReturn:
        '''Tear down for class.'''

        cls.removeTestFiles()
        cls.printTearDownClassMsg()


    def setUp(self) -> typing.NoReturn:
        '''Set up for test.'''

        self.printSetUpMethodMsg()
        tmp_Construction = AnalysysService()
        tmp_Construction.raceNameKey = 'TestRace'
        tmp_Construction.localAnalyticKey = 'Test_Analytic_key'
        tmp_Construction.groupKey = 'Test_Group_Key'

        self.TestConstruction = AnalyticChains(tmp_Construction)


    def tearDown(self) -> typing.NoReturn:
        '''Tear down for test.'''

        self.printTearDownMethodMsg()
        self.TestConstruction = None

    ##END PrepareBlock

    @FunctionalClass.descript
    def test_nullifyCount_checkingNullifyingLenChainsData_expectedNullifyedData(
            self) -> typing.NoReturn:
        '''
        Testing the method of nullifying count data for key of chain length 
        orger by the list of chain keys.
        '''
        chainNames = {'iya': {}, 
                      'ei': {},}
        lenChainNamesData = {3: {'Count': 4},    #
                            2: {'Count': 5},}   #

        res = self.TestConstruction.nullifyCount(chainNames, lenChainNamesData)
        self.assertDictEqual(res, {3: {'Count': 0}, 
                                   2: {'Count': 0},})


    @FunctionalClass.descript
    def test_prepareChainsAnalytic_checkingPreparingTemplate_expectedRightTemplate(
            self) -> typing.NoReturn:
        '''
        Testing the method of get and prepare chains template for new key.
        '''

        res = self.TestConstruction.prepareChainsAnalytic('test_newKey')
        self.assertDictEqual(res, {"test_newKey": {
                                        "Max_Count_In_Name": 0,
                                        "Names_Count": 0,
                                        "Chance": 0,
                                        }
                                    })


    @FunctionalClass.descript
    def test_getChainsDataByLocalAnalytic_checkingGettingData_expectedRightData(
            self) -> typing.NoReturn:
        '''
        Testing the method of getting chains data by the chains 
        subkey from names DB.
        Used curent keys: self.raceNameKey, self.localAnalyticKey, 
        self.groupKey.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Max_Names_Count'] = 10
        testRaceData['Male_Names_Count'] = 3
        testRaceData['Vowels_Chains'] = {'Chains': {'Test_Group_Key': {
                        'e': {'Count': 2, 'Chance': 0.0,}, 
                        'ie': {'Count': 3, 'Chance': 100.0,} }}
                    }
     
        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.localAnalyticKey = 'Vowels_Chains'

        res = self.TestConstruction.getChainsDataByLocalAnalytic()
        self.assertDictEqual(res, {'e': {'Count': 2, 'Chance': 0.0,}, 
                                    'ie': {'Count': 3, 'Chance': 100.0,}
                                    })


    @FunctionalClass.descript
    def test_makeChainList_checkingVowelGettingChainList_expectedChainList(
            self) -> typing.NoReturn:
        '''
        Testing the method of getting vowel chains list from name.
        Used curent keys: self.alphabet.
        '''
        self.TestConstruction.alphabet = VOWELS_LETTERS

        res = self.TestConstruction.makeChainList('Testname')
        self.assertListEqual(res, ['e', 'a', 'e'])


    @FunctionalClass.descript
    def test_makeChainList_checkingConsonantGettingChainList_expectedChainList(
            self) -> typing.NoReturn:
        '''
        Testing the method of getting consonant chains list from name.
        Used curent keys: self.alphabet.
        '''
        self.TestConstruction.alphabet = CONSONANTS_LETTERS

        res = self.TestConstruction.makeChainList('Testname')
        self.assertListEqual(res, ['t', 'stn', 'm'])


    @FunctionalClass.descript
    def test_getChain_checkingIterationing_expectedChainList(
            self) -> typing.NoReturn:
        '''
        Testing the method of getting consonant chains list from name.
        Used curent keys: self.alphabet.
        '''
        self.TestConstruction.alphabet = CONSONANTS_LETTERS

        res = list(self.TestConstruction.getChain('Testname'))
        self.assertListEqual(res, ['t', 'stn', 'm'])


    @FunctionalClass.descript
    def test_getChainCount_checkingGettingIterationLenOfChain_expectedListOfLen(
            self) -> typing.NoReturn:
        '''
        Testing an iterative method for obtaining the count of vowels 
        or consonants in a chain.
        Used curent keys: self.raceNameKey, self.localAnalyticKey, 
        self.groupKey, self.FirstOnly.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Max_Names_Count'] = 10
        testRaceData['Male_Names_Count'] = 3
        testRaceData['Vowels_Chains'] = {'Chains': {'Test_Group_Key': {
                        'e': {'Count': 2, 'Chance': 0.0,}, 
                        'ie': {'Count': 3, 'Chance': 100.0,} }}
                    }

        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.localAnalyticKey = 'Vowels_Chains'
        self.TestConstruction.FirstOnly = False

        res = list(self.TestConstruction.getChainCount('Testname'))
        self.assertListEqual(res, [1, 2])


    @FunctionalClass.descript
    def test_sortChainsByLength_checkingSorting_expectedSortedChainsData(
            self) -> typing.NoReturn:
        '''
        Testing a sorting chains by the length.
        '''
        chainNames = {'e': {'Count': 2, 'Chance': 0.0, }, 
                      'ie': {'Count': 3, 'Chance': 100.0, },
                    }

        res = self.TestConstruction.sortChainsByLength(chainNames)
        self.assertEqual(res, { 'ie': {'Count': 3, 'Chance': 100.0, },
                                'e': {'Count': 2, 'Chance': 0.0, }, 
                                })


    @FunctionalClass.descript
    def test_calcChainMaxCountInName_checkingCalcLenChainsAmount_expectedLenAmount(
            self) -> typing.NoReturn:
        '''
        Testing the method of getting chains data by the chains 
        subkey from names DB.
        Used curent keys: self.raceNameKey, self.localAnalyticKey, 
        self.groupKey.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Max_Names_Count'] = 10
        testRaceData['Male_Names_Count'] = 3
        testRaceData['Vowels_Chains'] = {'Chains': {'Test_Group_Key': {
                        'e': {'Count': 2, 'Chance': 0.0,}, 
                        'ie': {'Count': 3, 'Chance': 100.0,},
                        'o': {'Count': 4, 'Chance': 0.0, }, }}
                    }
   
        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.localAnalyticKey = 'Vowels_Chains'

        res = self.TestConstruction.calcChainMaxCountInName('Venrieno')
        self.assertDictEqual(res, {2: {'Max_Count_In_Name': 1}, 
                                    1: {'Max_Count_In_Name': 2}})


    @FunctionalClass.descript
    def test_getChainMaxCountKey_checkingMakingKey_expectedRightKey(
            self) -> typing.NoReturn:
        '''
        Testing the making key consisting of the length of chain 
        and repets amount in the name.
        Used curent keys: self.raceNameKey, self.localAnalyticKey, 
        self.groupKey.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Max_Names_Count'] = 10
        testRaceData['Male_Names_Count'] = 3
        testRaceData['Vowels_Chains'] = {'Chains': {'Test_Group_Key': {
                        'e': {'Count': 2, 'Chance': 0.0,}, 
                        'ie': {'Count': 3, 'Chance': 100.0,},
                        'o': {'Count': 4, 'Chance': 0.0, }, }}
                    }
   
        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.localAnalyticKey = 'Vowels_Chains'

        res = list(self.TestConstruction.getChainMaxCountKey('Venrieno'))
        self.assertListEqual(res, ['2_1', '1_2'])


    @FunctionalClass.descript
    def test_getChainCountDataByLocalAnalytic_checkingGettingData_expectedData(
            self) -> typing.NoReturn:
        '''
        Testing the getting chains count data from temporary by local key.
        Used curent keys: self.raceNameKey, self.localAnalyticKey, 
        self.groupKey.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Max_Names_Count'] = 10
        testRaceData['Male_Names_Count'] = 3
        testRaceData['Vowels_Chains'] = {'Chain_Frequency': {'Test_Group_Key': {
                        1: {'Count': 2, 'Chance': 100.0, }, 
                        2: {'Count': 2, 'Chance': 100.0, } }}
                    }

        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.localAnalyticKey = 'Vowels_Chains'

        res = self.TestConstruction.getChainCountDataByLocalAnalytic('Chain_Frequency')
        self.assertDictEqual(res, {1: {'Count': 2, 'Chance': 100.0, }, 
                                    2: {'Count': 2, 'Chance': 100.0, }
                                    })


    @FunctionalClass.descript
    def test_getNullifyedChainCountDataByLocalAnalytic_checkingGettingData_expectedData(
            self) -> typing.NoReturn:
        '''
        Testing the getting chains count data by local key with nullifyed count.
        Used curent keys: self.raceNameKey, self.localAnalyticKey, 
        self.groupKey.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Max_Names_Count'] = 10
        testRaceData['Male_Names_Count'] = 3
        testRaceData['Vowels_Chains']['Chains'] = {'Test_Group_Key': {
                        'e': {'Count': 2, 'Chance': 0.0, }, 
                        'ie': {'Count': 3, 'Chance': 100.0, }} }
        testRaceData['Vowels_Chains']['Chain_Frequency'] = {'Test_Group_Key': {
                        1: {'Count': 2, 'Chance': 100.0, }, 
                        2: {'Count': 2, 'Chance': 50.0, }} }

        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.localAnalyticKey = 'Vowels_Chains'

        res = self.TestConstruction.getNullifyedChainCountDataByLocalAnalytic('Chain_Frequency')
        self.assertDictEqual(res, {1: {'Count': 0, 'Chance': 100.0, }, 
                                    2: {'Count': 0, 'Chance': 50.0, }
                                    })
    

    @FunctionalClass.descript
    def test_setLocalChainsAnalyticData_checkingChainsDataStorage_expectedRatingData(
            self) -> typing.NoReturn:
        '''
        Testing of sets the chains rating data by local key.
        Used curent keys: self.raceNameKey, self.localAnalyticKey, 
        self.groupKey.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Max_Names_Count'] = 10
        testRaceData['Male_Names_Count'] = 3
        testRaceData['Vowels_Chains'] = {'Chains': {'Test_Group_Key': {}},}

        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.localAnalyticKey = 'Vowels_Chains'

        ratingData = dict({ 'e': {'Count': 2, 'Chance': 0.0, }, 
                            'ie': {'Count': 3, 'Chance': 100.0, }
                            })
        self.TestConstruction.setLocalChainsAnalyticData('Chains', ratingData)

        res = self.TestConstruction.tmp_NamesAnalytic['TestRace']['Vowels_Chains'][
                                                        'Chains']['Test_Group_Key']
        self.assertDictEqual(res, { 'e': {'Count': 2, 'Chance': 0.0, }, 
                                    'ie': {'Count': 3, 'Chance': 100.0, }
                                    })


    @FunctionalClass.descript
    def test_sortChainsByLength_checkingSortingChainDict_expectedEqualDict(
            self) -> typing.NoReturn:
        '''
        Testing of sorting chains by the length.
        '''

        res = self.TestConstruction.sortChainsByLength(
                                {'a': {'Count': 2, 'Chance': 0.0, }, 
                                'aie': {'Count': 3, 'Chance': 100.0, },
                                'ai': {'Count': 4, 'Chance': 100.0, },
                                })
        self.assertEqual(res, { 'aie': {'Count': 3, 'Chance': 100.0, },
                                'ai': {'Count': 4, 'Chance': 100.0,  },
                                'a': {'Count': 2, 'Chance': 0.0, }, 
                                })


    @FunctionalClass.descript
    def test_calcChainFrequency_checkingCalculatingCount_expectedAmountOfLen(
            self) -> typing.NoReturn:
        '''
        Testing of calculating common chains count in all names.
        Used curent keys: self.raceNameKey, self.localAnalyticKey, 
        self.groupKey, self.tmp_NamesDB.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Max_Names_Count'] = 10
        testRaceData['Male_Names_Count'] = 3
        testRaceData['Vowels_Chains']['Chains'] = {'Test_Group_Key': {
                        'e': {'Count': 2, 'Chance': 0.0, }, 
                        'ei': {'Count': 2, 'Chance': 0.0, },
                        'ia': {'Count': 1, 'Chance': 0.0, },
                        'a': {'Count': 1, 'Chance': 0.0, },} }
        testRaceData['Vowels_Chains']['Chain_Frequency'] = {'Test_Group_Key': {} }

        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.tmp_NamesDB['Test_Group_Key'] = ['Veiste', 'Reist', 'Alrestia']
        self.TestConstruction.localAnalyticKey = 'Vowels_Chains'

        self.TestConstruction.calcChainFrequency()

        res = self.TestConstruction.tmp_NamesAnalytic['TestRace']['Vowels_Chains'][
                                                        'Chain_Frequency']['Test_Group_Key']
        self.assertDictEqual(res, { 1: {'Count': 3}, 
                                    2: {'Count': 3},
                                    })


    @FunctionalClass.descript
    def test_prepareDataByChainsAnalyticTemplate_checkingPreparingData_expectedStoredNewDataModel(
            self) -> typing.NoReturn:
        '''
        Testing of preparing and saving data of the lenght of chain and their 
        repets count in names.
        Used curent keys: self.raceNameKey, self.localAnalyticKey, 
        self.groupKey, self.tmp_NamesDB.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Max_Names_Count'] = 10
        testRaceData['Male_Names_Count'] = 3
        testRaceData['Vowels_Chains'] = {'Length_Count_Names': {'Test_Group_Key': {
                        '1_3': {'Count': 8,'Chance': 0.0, }, 
                        '2_4': {'Count': 9,'Chance': 0.0, }, }} }

        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.tmp_NamesDB['Test_Group_Key'] = ['Veiste', 'Reist', 'Alrestia']
        self.TestConstruction.localAnalyticKey = 'Vowels_Chains'

        self.TestConstruction.prepareDataByChainsAnalyticTemplate('Length_Count_Names')

        res = self.TestConstruction.tmp_NamesAnalytic['TestRace']['Vowels_Chains'][
                                                        'Length_Count_Names']['Test_Group_Key']
        self.assertDictEqual(res, {'1_3': {                     #
                                        'Max_Count_In_Name': 3, #
                                        'Names_Count': 8,       #
                                        'Chance': 0.0, 
                                        }, 
                                    '2_4': {                    #
                                        'Max_Count_In_Name': 4, #
                                        'Names_Count': 9,       #
                                        'Chance': 0.0, 
                                        },
                                })


    @FunctionalClass.descript
    def test_prepareDataByChainsAnalyticTemplate_checkingPreparingDataOnTheLastGroupKey_expectedStoredNewDataModel(
            self) -> typing.NoReturn:
        '''
        Testing of preparing and saving data of the lenght of chain and their 
        repets count in names.
        Used curent keys: self.raceNameKey, self.localAnalyticKey, 
        self.groupKey, self.tmp_NamesDB.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Max_Names_Count'] = 10
        testRaceData['Surnames_Count'] = 4
        testRaceData['Vowels_Chains'] = {'Length_Count_Names': {
                    'Surnames': {
                        '1_3': {'Count': 8,'Chance': 0.0, }, 
                        '2_4': {'Count': 9,'Chance': 0.0, }, },
                    "Common":{
                        '1_3': {'Count': 10,'Chance': 0.0, }, 
                        '2_4': {'Count': 11,'Chance': 0.0, }, }},
                }

        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.tmp_NamesDB['Surnames'] = ['Veiste', 'Reist', 'Alrestia']
        self.TestConstruction.groupKey = 'Surnames'
        self.TestConstruction.localAnalyticKey = 'Vowels_Chains'

        self.TestConstruction.prepareDataByChainsAnalyticTemplate('Length_Count_Names')

        res = self.TestConstruction.tmp_NamesAnalytic['TestRace']['Vowels_Chains'][
                                                        'Length_Count_Names']
        self.assertDictEqual(res, 
                    {'Surnames': {
                            '1_3': {'Max_Count_In_Name': 3, 'Names_Count': 8, 'Chance': 0.0,}, 
                            '2_4': {'Max_Count_In_Name': 4, 'Names_Count': 9, 'Chance': 0.0,},
                        },
                        "Common":{
                            '1_3': {'Max_Count_In_Name': 3, 'Names_Count': 10, 'Chance': 0.0,}, #
                            '2_4': {'Max_Count_In_Name': 4, 'Names_Count': 11, 'Chance': 0.0,}, #
                            }
                        })


    @FunctionalClass.descript
    def test_callcRatingOfChainsBySubkey_checkingCalculatingRating_expectedRightChances(
            self) -> typing.NoReturn:
        '''
        Testing of calculating local and common chances for vowels or consonant 
        chains by the subkey.
        Used curent keys: self.raceNameKey, self.localAnalyticKey, 
        self.groupKey.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Max_Names_Count'] = 10
        testRaceData['Male_Names_Count'] = 3
        testRaceData['Vowels_Chains'] = {'Chains': {'Male': {
                        'e': {'Count': 1, 'Chance': 0.0,},  
                        'ei': {'Count': 2,'Chance': 0.0,},  
                        'ia': {'Count': 3, 'Chance': 0.0,}, }},
                }
        
        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.groupKey = 'Male'
        self.TestConstruction.localAnalyticKey = 'Vowels_Chains'

        self.TestConstruction.callcRatingOfChainsBySubkey('Chains')

        res = self.TestConstruction.tmp_NamesAnalytic['TestRace']['Vowels_Chains'][
                                                        'Chains']['Male']
        self.assertDictEqual(res, { 'e': {'Count': 1, 'Chance': 33.333333333333336,},         
                                    'ei': {'Count': 2, 'Chance': 66.66666666666667,},         
                                    'ia': {'Count': 3, 'Chance': 100.0,},         
                                    })


    @FunctionalClass.descript
    def test_calcRatingForAllChainsSubkeysByLocalAnalytic_checkingCalculatingRating_expectedRightChances(
            self) -> typing.NoReturn:
        '''
        Testing of calculating chances for the chains (vowels or consonant) by all subkey.
        Used curent keys: self.raceNameKey, self.localAnalyticKey, 
        self.groupKey.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Max_Names_Count'] = 10
        testRaceData['Male_Names_Count'] = 3
        testRaceData['Vowels_Chains']['Chains'] = {'Male': {
                        'e': {'Count': 1, 'Chance': 0.0,},  
                        'ei': {'Count': 2, 'Chance': 0.0,},  
                        'ia': {'Count': 3, 'Chance': 0.0,}, } }
        testRaceData['Vowels_Chains']['Chain_Frequency'] = {'Male': {
                        1: {'Count': 6,'Chance': 0.0,},  
                        2: {'Count': 7,'Chance': 0.0,}, }, }
        
        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.groupKey = 'Male'
        self.TestConstruction.localAnalyticKey = 'Vowels_Chains'

        self.TestConstruction.calcRatingForAllChainsSubkeysByLocalAnalytic()

        res = self.TestConstruction.tmp_NamesAnalytic['TestRace']['Vowels_Chains']
        self.assertDictEqual(res, {'Chains': {
                                        'Male': {
                                            'e': {'Count': 1, 'Chance': 33.333333333333336,},         
                                            'ei': {'Count': 2, 'Chance': 66.66666666666667,},         
                                            'ia': {'Count': 3, 'Chance': 100.0,}
                                            }
                                        },
                                    'Chain_Frequency': {
                                        'Male': {
                                            1: {'Count': 6,'Chance': 200.0,},         
                                            2: {'Count': 7,'Chance': 233.333333333333334,}         
                                            }
                                        }, 
                                    'Length_Count_Names': {}
                                    })


    @FunctionalClass.descript
    def test_createChainsDataForAllSubkeysByLocalAnalytic_checkingFormatOfCreatedData_expectedRightDataFormat(
            self) -> typing.NoReturn:
        '''
        Testing of creating and formating chains data.
        Used curent keys: self.raceNameKey, self.localAnalyticKey, 
        self.groupKey, self.tmp_NamesDB.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Max_Names_Count'] = 10
        testRaceData['Male_Names_Count'] = 3
        testRaceData['Vowels_Chains']['Chains'] = {'Male': {}}
        testRaceData['Vowels_Chains']['Chain_Frequency'] = {'Male': {}}
        testRaceData['Vowels_Chains']['Length_Count_Names'] = {'Male': {}}
        
        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.tmp_NamesDB['Male'] = ['Veiste', 'Reist', 'Alrestia']
        self.TestConstruction.groupKey = 'Male'
        self.TestConstruction.localAnalyticKey = 'Vowels_Chains'
        self.TestConstruction.alphabet = VOWELS_LETTERS

        self.TestConstruction.createChainsDataForAllSubkeysByLocalAnalytic()
        
        res = self.TestConstruction.tmp_NamesAnalytic['TestRace']['Vowels_Chains']
        self.assertDictEqual(res, {'Chains': {
                                        'Male': {
                                            'ei': {'Count': 2, 'Chance': 66.66666666666667,}, 
                                            'e': {'Count': 2, 'Chance': 66.66666666666667,},
                                            'a': {'Count': 1, 'Chance': 33.333333333333336,}, 
                                            'ia': {'Count': 1, 'Chance': 33.333333333333336,}},
                                        'Common': {
                                            'ei': {'Count': 2, 'Chance': 20.0,}, 
                                            'e': {'Count': 2, 'Chance': 20.0,},
                                            'a': {'Count': 1, 'Chance': 10.0,}, 
                                            'ia': {'Count': 1, 'Chance': 10.0,}}}, 
                                    'Chain_Frequency': {    #stub data; will be edited after
                                        'Male': {}
                                    }, 
                                    'Length_Count_Names': {
                                        'Male': {
                                            '2_1': {'Count': 3, 'Chance': 100.0,}, 
                                            '1_1': {'Count': 1, 'Chance': 33.333333333333336,}, 
                                            '1_2': {'Count': 1, 'Chance': 33.333333333333336,}},
                                        'Common': {
                                            '2_1': {'Count': 3, 'Chance': 30.0,}, 
                                            '1_1': {'Count': 1, 'Chance': 10.0,}, 
                                            '1_2': {'Count': 1, 'Chance': 10.0,}}}
                                })


    @FunctionalClass.descript
    def test_calcChainsDataForAllSubkeysByLocalAnalytic_checkingCalculatingChainsData_expectedRightData(
            self) -> typing.NoReturn:
        '''
        Testing of calculating all chains data for all subkeys.
        Used curent keys: self.raceNameKey, self.localAnalyticKey, 
        self.groupKey, self.tmp_NamesDB.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Max_Names_Count'] = 10
        testRaceData['Male_Names_Count'] = 3
        testRaceData['Vowels_Chains']['Chains'] = {
                    'Male': {
                        'ei': {'Count': 2, 'Chance': 66.66666666666667,}, 
                        'e': {'Count': 2, 'Chance': 66.66666666666667,},
                        'a': {'Count': 1, 'Chance': 33.333333333333336,}, 
                        'ia': {'Count': 1, 'Chance': 33.333333333333336,} },
                    'Common': {
                        'ei': {'Count': 2, 'Chance': 20.0,}, 
                        'e': {'Count': 2, 'Chance': 20.0,}, 
                        'a': {'Count': 1, 'Chance': 10.0,}, 
                        'ia': {'Count': 1, 'Chance': 10.0,} }
                }
        testRaceData['Vowels_Chains']['Chain_Frequency'] = {'Male': {
                        2: {'Count': 2, 'Chance': 66.66666666666667,}, 
                        1: {'Count': 2, 'Chance': 66.66666666666667,} }}
        testRaceData['Vowels_Chains']['Length_Count_Names'] = {
                    'Male': {
                        '2_1': {'Count': 3, 'Chance': 100.0, }, 
                        '1_1': {'Count': 1, 'Chance': 33.333333333333336,}, 
                        '1_2': {'Count': 1, 'Chance': 33.333333333333336,} },
                    'Common': {
                        '2_1': {'Count': 3, 'Chance': 30.0,}, 
                        '1_1': {'Count': 1, 'Chance': 10.0,}, 
                        '1_2': {'Count': 1, 'Chance': 10.0,} }
                }
        
        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.tmp_NamesDB['Male'] = ['Veiste', 'Reist', 'Alrestia']
        self.TestConstruction.groupKey = 'Male'
        self.TestConstruction.localAnalyticKey = 'Vowels_Chains'
        self.TestConstruction.alphabet = VOWELS_LETTERS

        self.TestConstruction.calcChainsDataForAllSubkeysByLocalAnalytic()
        
        res = self.TestConstruction.tmp_NamesAnalytic['TestRace']['Vowels_Chains']
        self.assertDictEqual(res, {'Chains': {
                                        'Male': {
                                            'ei': {'Count': 2, 'Chance': 66.66666666666667,}, 
                                            'e': {'Count': 2, 'Chance': 66.66666666666667,}, 
                                            'a': {'Count': 1, 'Chance': 33.333333333333336,}, 
                                            'ia': {'Count': 1, 'Chance': 33.333333333333336,}
                                            },
                                        'Common': {
                                            'ei': {'Count': 2, 'Chance': 20.0,}, 
                                            'e': {'Count': 2, 'Chance': 20.0,}, 
                                            'a': {'Count': 1, 'Chance': 10.0,}, 
                                            'ia': {'Count': 1, 'Chance': 10.0,}
                                        }}, 
                                    'Chain_Frequency': {
                                        'Male': {
                                            2: {'Count': 3, 'Chance': 100.0,}, 
                                            1: {'Count': 3, 'Chance': 100.0,}
                                            },
                                        'Common': {         #
                                            2: {'Count': 3, 'Chance': 30.0,}, 
                                            1: {'Count': 3, 'Chance': 30.0,}
                                        }}, 
                                    'Length_Count_Names': {
                                        'Male': {
                                            '2_1': {
                                                'Max_Count_In_Name': 1, 
                                                'Names_Count': 3, 
                                                'Chance': 100.0, 
                                                }, 
                                            '1_1': {
                                                'Max_Count_In_Name': 1, 
                                                'Names_Count': 1, 
                                                'Chance': 33.333333333333336, 
                                                }, 
                                            '1_2': {
                                                'Max_Count_In_Name': 2, 
                                                'Names_Count': 1, 
                                                'Chance': 33.333333333333336, 
                                                }
                                            },
                                        'Common': {
                                            '2_1': {'Count': 3, 'Chance': 30.0,}, 
                                            '1_1': {'Count': 1, 'Chance': 10.0,}, 
                                            '1_2': {'Count': 1, 'Chance': 10.0,}
                                        }}
                                    })


    @FunctionalClass.descript
    def test_makeVowelsChainsAllData_checkingMakingVowelChainsData_expectedRightData(
            self) -> typing.NoReturn:
        '''
        Testing of making all vowel chains data for all subkeys.
        Used curent keys: self.raceNameKey, self.groupKey, self.tmp_NamesDB.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Max_Names_Count'] = 10
        testRaceData['Male_Names_Count'] = 3
        testRaceData['Vowels_Chains'] = {'Chains': {}, 'Chain_Frequency': {},
                                'Length_Count_Names': {}}

        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.tmp_NamesDB['Male'] = ['Veiste', 'Reist', 'Alrestia']
        self.TestConstruction.groupKey = 'Male'

        self.TestConstruction.makeVowelsChainsAllData()
        
        res = self.TestConstruction.tmp_NamesAnalytic['TestRace']['Vowels_Chains']
        self.assertDictEqual(res, {'Chains': {
                                        'Male': {
                                            'ei': {'Count': 2, 'Chance': 66.66666666666667,}, 
                                            'e': {'Count': 2, 'Chance': 66.66666666666667,}, 
                                            'a': {'Count': 1, 'Chance': 33.333333333333336,}, 
                                            'ia': {'Count': 1, 'Chance': 33.333333333333336,}
                                            },
                                        'Common': {
                                            'ei': {'Count': 2, 'Chance': 20.0,}, 
                                            'e': {'Count': 2, 'Chance': 20.0,}, 
                                            'a': {'Count': 1, 'Chance': 10.0,}, 
                                            'ia': {'Count': 1, 'Chance': 10.0,}
                                        }}, 
                                    'Chain_Frequency': {
                                        'Male': {
                                            2: {'Count': 3, 'Chance': 100.0,}, 
                                            1: {'Count': 3, 'Chance': 100.0,}
                                            },
                                        'Common': {
                                            2: {'Count': 3, 'Chance': 30.0,}, 
                                            1: {'Count': 3, 'Chance': 30.0,}
                                        }}, 
                                    'Length_Count_Names': {
                                        'Male': {
                                            '2_1': {
                                                'Max_Count_In_Name': 1, 
                                                'Names_Count': 3, 
                                                'Chance': 100.0, 
                                                }, 
                                            '1_1': {
                                                'Max_Count_In_Name': 1, 
                                                'Names_Count': 1, 
                                                'Chance': 33.333333333333336, 
                                                }, 
                                            '1_2': {
                                                'Max_Count_In_Name': 2, 
                                                'Names_Count': 1, 
                                                'Chance': 33.333333333333336, 
                                                }
                                        },
                                        'Common': {
                                            '2_1': {'Count': 3, 'Chance': 30.0,}, 
                                            '1_1': {'Count': 1, 'Chance': 10.0,}, 
                                            '1_2': {'Count': 1, 'Chance': 10.0,}
                                        }}
                                    })


    @FunctionalClass.descript
    def test_makeConsonantsChainsAllData_checkingMakingConsonantChainsData_expectedRightData(
            self) -> typing.NoReturn:
        '''
        Testing of making all consonant chains data for all subkeys.
        Used curent keys: self.raceNameKey, self.groupKey, self.tmp_NamesDB.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Max_Names_Count'] = 10
        testRaceData['Male_Names_Count'] = 3
        testRaceData['Consonants_Chains'] = {'Chains': {}, 'Chain_Frequency': {},
                                'Length_Count_Names': {}}
        
        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.tmp_NamesDB['Male'] = ['Veiste', 'Reist', 'Alrestia']
        self.TestConstruction.groupKey = 'Male'

        self.TestConstruction.makeConsonantsChainsAllData()
        
        res = self.TestConstruction.tmp_NamesAnalytic['TestRace']['Consonants_Chains']
        self.assertDictEqual(res, {'Chains': {
                                        'Male': {
                                            'v': {'Count': 1, 'Chance': 33.333333333333336,}, 
                                            'st': {'Count': 3, 'Chance': 100.0,}, 
                                            'r': {'Count': 1, 'Chance': 33.333333333333336,}, 
                                            'lr': {'Count': 1, 'Chance': 33.333333333333336,}
                                            },
                                        'Common': {
                                            'v': {'Count': 1, 'Chance': 10.0,}, 
                                            'st': {'Count': 3, 'Chance': 30.0,}, 
                                            'r': {'Count': 1, 'Chance': 10.0,}, 
                                            'lr': {'Count': 1, 'Chance': 10.0,}
                                        }}, 
                                    'Chain_Frequency': {
                                        'Male': {
                                            2: {'Count': 4, 'Chance': 133.333333333333334,}, 
                                            1: {'Count': 2, 'Chance': 66.66666666666667,}
                                            },
                                        'Common': {
                                            2: {'Count': 4, 'Chance': 40.0}, 
                                            1: {'Count': 2, 'Chance': 20.0,}
                                        }}, 
                                    'Length_Count_Names': {
                                        'Male': {
                                            '2_2': {
                                                'Max_Count_In_Name': 2, 
                                                'Names_Count': 1, 
                                                'Chance': 33.333333333333336, 
                                                }, 
                                            '2_1': {
                                                'Max_Count_In_Name': 1, 
                                                'Names_Count': 2, 
                                                'Chance': 66.66666666666667, 
                                                }, 
                                            '1_1': {
                                                'Max_Count_In_Name': 1, 
                                                'Names_Count': 2, 
                                                'Chance': 66.66666666666667, 
                                                }
                                        },
                                        'Common': {
                                            '2_2': {'Count': 1, 'Chance': 10.0,}, 
                                            '2_1': {'Count': 2, 'Chance': 20.0,}, 
                                            '1_1': {'Count': 2, 'Chance': 20.0,}
                                        }}
                                    })


class AnalyticCombinations_Test(FunctionalClass):
    '''
    Testing next methods of class #AnalyticChains:
    getListChainsData;
    makeAllChainList;
    makeChainsCombinationsInOrderData;
    '''

    ##BEGIN ConstantBlock
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

    ##Begin PrepareBlock
    @classmethod
    def setUpClass(cls) -> typing.NoReturn:
        '''Set up for class.'''

        cls.printSetUpClassMsg()
        cls.createTestFiles()


    @classmethod
    def tearDownClass(cls) -> typing.NoReturn:
        '''Tear down for class.'''

        cls.removeTestFiles()
        cls.printTearDownClassMsg()


    def setUp(self) -> typing.NoReturn:
        '''Set up for test.'''

        self.printSetUpMethodMsg()
        tmp_Construction = AnalysysService()
        tmp_Construction.raceNameKey = 'TestRace'
        tmp_Construction.localAnalyticKey = 'Test_Analytic_key'
        tmp_Construction.groupKey = 'Test_Group_Key'

        self.TestConstruction = AnalyticCombinations(tmp_Construction)


    def tearDown(self) -> typing.NoReturn:
        '''Tear down for test.'''

        self.printTearDownMethodMsg()
        self.TestConstruction = None

    ##END PrepareBlock

    @FunctionalClass.descript
    def test_getListChainsData_checkingChainsDataFromName_expectedRightData(
            self) -> typing.NoReturn:
        '''
        Testing the method of obtaining chains and 
        information about them from the name.
        '''

        res = self.TestConstruction.getListChainsData('Someonesname')
        self.assertDictEqual(res, dict({'first': ['s', 'm', 'n', 'sn', 'm'], 
                                        'second': ['o', 'eo', 'e', 'a', 'e'], 
                                        'first_len': 5, 
                                        'second_len': 5}))


    @FunctionalClass.descript
    def test_makeAllChainList_checkingChainsDataFromName_expectedChainsByOrder(
            self) -> typing.NoReturn:
        '''
        Testing the method of obtaining chains from a name in order.
        '''

        res = self.TestConstruction.makeAllChainList('Someonesname')
        self.assertListEqual(res, list(['s', 'o', 'm', 'eo', 'n', 
                                        'e', 'sn', 'a', 'm', 'e']))


    @FunctionalClass.descript
    def test_makeChainsCombinationsInOrderData_checkingMakingChainsCombinationsData_expectedRightData(
            self) -> typing.NoReturn:
        '''
        Testing the method of making combinations of chains in order from a names.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Max_Names_Count'] = 10
        testRaceData['Male_Names_Count'] = 3
        testRaceData['Chains_Combinations'] = dict()
        
        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.tmp_NamesDB['Male'] = ['Veiste', 'Reist']
        self.TestConstruction.groupKey = 'Male'

        self.TestConstruction.makeChainsCombinationsInOrderData()
        
        res = self.TestConstruction.tmp_NamesAnalytic['TestRace']['Chains_Combinations']
        self.assertDictEqual(res, {'Male': {
                                        'veist': {'Count': 1, 'Chance': 33.333333333333336}, 
                                        'eiste': {'Count': 1, 'Chance': 33.333333333333336}, 
                                        'vei': {'Count': 1, 'Chance': 33.333333333333336}, 
                                        'eist': {'Count': 2, 'Chance': 66.66666666666667}, 
                                        'ste': {'Count': 1, 'Chance': 33.333333333333336}, 
                                        'reist': {'Count': 1, 'Chance': 33.333333333333336}, 
                                        'rei': {'Count': 1, 'Chance': 33.333333333333336}
                                        }, 
                                    'Common': {    
                                        'veist': {'Count': 1, 'Chance': 10.0}, 
                                        'eiste': {'Count': 1, 'Chance': 10.0}, 
                                        'vei': {'Count': 1, 'Chance': 10.0}, 
                                        'eist': {'Count': 2, 'Chance': 20.0}, 
                                        'ste': {'Count': 1, 'Chance': 10.0}, 
                                        'reist': {'Count': 1, 'Chance': 10.0}, 
                                        'rei': {'Count': 1, 'Chance': 10.0}
                                        }
                                    })


class Analysis_Test(FunctionalClass):
    '''
    Testing next methods of class #AnalyticChains:
    makeFunctionsList;
    formatRespond;
    initLocalAnalyticDataByGroupKey;
    makeLocalAnalyticDataByGroupKey;
    initLocalAnalyticDB;
    makeLocalAnalyticDB;
    formatLocalAnalyticDB;
    extractingNamesByGroupKey;
    fillGlobNamesAnalyticVar;
    makeAnalyticData;
    printResponds;
    makeAnalyticDB;
    '''

    ##BEGIN ConstantBlock
    TestFiles = {
        'tmpLOGTESTNames.log': str(),
        'tmpDBAnalytic.cfg': str(),
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
    def setUpClass(cls) -> typing.NoReturn:
        '''Set up for class.'''

        cls.printSetUpClassMsg()
        cls.createTestFiles()


    @classmethod
    def tearDownClass(cls) -> typing.NoReturn:
        '''Tear down for class.'''

        cls.removeTestFiles()
        cls.printTearDownClassMsg()


    def setUp(self) -> typing.NoReturn:
        '''Set up for test.'''

        self.printSetUpMethodMsg()

        tmp_Construction = AnalysysService()
        self.TestConstruction = Analysis(tmp_Construction)

        self.TestConstruction.raceNameKey = 'TestRace'
        self.TestConstruction.localAnalyticKey = 'Test_Analytic_key'
        self.TestConstruction.groupKey = 'Test_Group_Key'
        
        tmpLogTestNames = str(self.TestFileDirectory + 'tmpLOGTESTNames.log')
        self.TestConstruction.logFilePath = tmpLogTestNames


    def tearDown(self) -> typing.NoReturn:
        '''Tear down for test.'''

        self.printTearDownMethodMsg()
        self.TestConstruction = None

    ##END PrepareBlock

    @FunctionalClass.descript
    def test_makeFunctionsList_checkingDataListType_expectedFunctionsList(
            self) -> typing.NoReturn:
        '''
        Checking the type of list of returned data.
        '''

        res = self.TestConstruction.makeFunctionsList()

        resTypes = list()
        compareTypesList = list()
        for r in res:
            resTypes.append(type(r))
            compareTypesList.append(types.MethodType)
        
        self.assertListEqual(resTypes, compareTypesList)


    @FunctionalClass.descript
    def test_formatRespond_checkingRespond_expectedCorrectRespond(
            self) -> typing.NoReturn:
        '''
        Testing the method of formating initial message of respond.
        '''

        res = self.TestConstruction.formatRespond()
        self.assertEqual(res, "*AnalyticDB* (Group Key: Test_Group_Key) \t| ")
        

    @FunctionalClass.descript
    def test_initLocalAnalyticDataByGroupKey_checkingInitialValues_expectedCountedValues(
            self) -> typing.NoReturn:
        '''
        Testing the method of initialize base values in analytic data by group key.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        allowedKeys = ['Max_Names_Count', 'Male_Names_Count', 'Female_Names_Count',
                    'Surnames_Count']
        NamesAnalyticData['TestRace'] = self.leaveKeys(allowedKeys, NamesAnalyticData['TestRace'])
        
        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.tmp_NamesDB['Male'] = ['Veiste', 'Reist']
        self.TestConstruction.groupKey = 'Male'

        self.TestConstruction.initLocalAnalyticDataByGroupKey()
        
        res = self.TestConstruction.tmp_NamesAnalytic['TestRace']
        self.assertDictEqual(res, { 'Max_Names_Count': 2,
                                    'Male_Names_Count': 2,
                                    'Female_Names_Count': 0,
                                    'Surnames_Count': 0,
                                    })

        
    @FunctionalClass.descript
    def test_makeLocalAnalyticDataByGroupKey_checkingCreatedValues_expectedCountedValues(
            self) -> typing.NoReturn:
        '''
        Testing the method of making analytic data by group key.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Max_Names_Count'] = 1
        testRaceData['Male_Names_Count'] = 1
     
        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.tmp_NamesDB['Male'] = ['Ve']
        self.TestConstruction.groupKey = 'Male'

        self.TestConstruction.makeLocalAnalyticDataByGroupKey()
        
        res = self.TestConstruction.tmp_NamesAnalytic['TestRace']
        self.assertDictEqual(res, {
                                    'Max_Names_Count': 1, 
                                    'Male_Names_Count': 1, 
                                    'Female_Names_Count': 0, 
                                    'Surnames_Count': 0, 
                                    'Name_Letters_Count': {
                                        'Male': {
                                            '2': {'Count': 1, 'Chance': 100.0}}, 
                                        'Common': {
                                            '2': {'Count': 1, 'Chance': 100.0}}}, 
                                    'Vowels_Count': {
                                        'Male': {
                                            1: {'Count': 1, 'Chance': 100.0}}, 
                                        'Common': {
                                            1: {'Count': 1, 'Chance': 100.0}}}, 
                                    'Consonants_Count': {
                                        'Male': {
                                            1: {'Count': 1, 'Chance': 100.0}}, 
                                        'Common': {
                                            1: {'Count': 1, 'Chance': 100.0}}}, 
                                    'First_Letters': {
                                        'Vowels_Count': 0, 
                                        'Consonants_Count': 1, 
                                        'Male': {
                                            'V': {'Count': 1, 'Chance': 100.0}}, 
                                        'Common': {
                                            'V': {'Count': 1, 'Chance': 100.0}}}, 
                                    'Letters': {
                                        'Male': {
                                            'v': {'Count': 1, 'Chance': 100.0}, 
                                            'e': {'Count': 1, 'Chance': 100.0}}, 
                                        'Common': {
                                            'v': {'Count': 1, 'Chance': 100.0}, 
                                            'e': {'Count': 1, 'Chance': 100.0}}}, 
                                    'Vowels_Chains': {
                                        'Chains': {
                                            'Male': {
                                                'e': {'Count': 1, 'Chance': 100.0}}, 
                                            'Common': {
                                                'e': {'Count': 1, 'Chance': 100.0}}}, 
                                        'Chain_Frequency': {
                                            'Male': {
                                                1: {'Count': 1, 'Chance': 100.0}}, 
                                            'Common': {
                                                1: {'Count': 1, 'Chance': 100.0}}}, 
                                        'Length_Count_Names': {
                                            'Male': {
                                                '1_1': {'Max_Count_In_Name': 1, 'Names_Count': 1, 'Chance': 100.0}}, 
                                            'Common': {
                                                '1_1': {'Count': 1, 'Chance': 100.0}}}}, 
                                    'Consonants_Chains': {
                                        'Chains': {
                                            'Male': {
                                                'v': {'Count': 1, 'Chance': 100.0}}, 
                                            'Common': {
                                                'v': {'Count': 1, 'Chance': 100.0}}}, 
                                        'Chain_Frequency': {
                                            'Male': {
                                                1: {'Count': 1, 'Chance': 100.0}}, 
                                            'Common': {
                                                1: {'Count': 1, 'Chance': 100.0}}}, 
                                        'Length_Count_Names': {
                                            'Male': {
                                                '1_1': {'Max_Count_In_Name': 1, 'Names_Count': 1, 'Chance': 100.0}}, 
                                            'Common': {
                                                '1_1': {'Count': 1, 'Chance': 100.0}}}}, 
                                    'Chains_Combinations': {
                                        'Male': {
                                            've': {'Count': 1, 'Chance': 100.0}}, 
                                        'Common': {
                                            've': {'Count': 1, 'Chance': 100.0}}}, 
                                    'Name_Endings': {
                                        'Male': {
                                            've': {'Count': 1, 'Chance': 100.0}}, 
                                        'Common': {
                                            've': {'Count': 1, 'Chance': 100.0}}}
                                    })

        
    @FunctionalClass.descript
    def test_initLocalAnalyticDB_checkingInitialValues_expectedCountedValues(
            self) -> typing.NoReturn:
        '''
        Testing the method of initialize base values in analytic data 
        for all group keys.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        allowedKeys = ['Max_Names_Count', 'Male_Names_Count', 'Female_Names_Count',
                    'Surnames_Count']
        NamesAnalyticData['TestRace'] = self.leaveKeys(allowedKeys, NamesAnalyticData['TestRace'])
     
        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.tmp_NamesDB = {'Male': ['Ma'],
                                             'Female': ['Fa', 'Fe'], 
                                             'Surnames': ['Sa', 'Se', 'Su']}

        groupKeys = ['Male', 'Female', 'Surnames']

        self.TestConstruction.initLocalAnalyticDB(groupKeys)
        
        res = self.TestConstruction.tmp_NamesAnalytic['TestRace']
        self.assertDictEqual(res, { 'Max_Names_Count': 6, 
                                    'Male_Names_Count': 1, 
                                    'Female_Names_Count': 2, 
                                    'Surnames_Count': 3, 
                                    #...
                                    })

        
    @FunctionalClass.descript
    def test_makeLocalAnalyticDB_checkingCreatedValues_expectedCountedValues(
            self) -> typing.NoReturn:
        '''
        Testing the method of making analytic data for all group keys.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Max_Names_Count'] = 3
        testRaceData['Male_Names_Count'] = 1
        testRaceData['Female_Names_Count'] = 1
        testRaceData['Surnames_Count'] = 1
     
        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.tmp_NamesDB = {'Male': ['Ma'],
                                             'Female': ['Fe'], 
                                             'Surnames': ['Su']}

        groupKeys = ['Male', 'Female', 'Surnames']

        self.TestConstruction.makeLocalAnalyticDB(groupKeys)
        
        res = self.TestConstruction.tmp_NamesAnalytic['TestRace']
        self.assertDictEqual(res, {
                                    'Max_Names_Count': 3, 
                                    'Male_Names_Count': 1, 
                                    'Female_Names_Count': 1, 
                                    'Surnames_Count': 1, 
                                    'Name_Letters_Count': {
                                        'Male': {
                                            '2': {'Count': 1, 'Chance': 100.0}}, 
                                        'Common': {
                                            '2': {'Count': 3, 'Chance': 100.0}}, 
                                        'Female': {
                                            '2': {'Count': 1, 'Chance': 100.0}}, 
                                        'Surnames': {
                                            '2': {'Count': 1, 'Chance': 100.0}}
                                        }, 
                                    'Vowels_Count': {
                                        'Male': {
                                            1: {'Count': 1, 'Chance': 100.0}}, 
                                        'Common': {
                                            1: {'Count': 3, 'Chance': 100.0}}, 
                                        'Female': {
                                            1: {'Count': 1, 'Chance': 100.0}}, 
                                        'Surnames': {
                                            1: {'Count': 1, 'Chance': 100.0}}}, 
                                    'Consonants_Count': {
                                        'Male': {
                                            1: {'Count': 1, 'Chance': 100.0}}, 
                                        'Common': {
                                            1: {'Count': 3, 'Chance': 100.0}}, 
                                        'Female': {
                                            1: {'Count': 1, 'Chance': 100.0}}, 
                                        'Surnames': {
                                            1: {'Count': 1, 'Chance': 100.0}}}, 
                                    'First_Letters': {
                                        'Vowels_Count': 0, 
                                        'Consonants_Count': 3, 
                                        'Male': {
                                            'M': {'Count': 1, 'Chance': 100.0}}, 
                                        'Common': {
                                            'M': {'Count': 1, 'Chance': 33.333333333333336}, 
                                            'F': {'Count': 1, 'Chance': 33.333333333333336}, 
                                            'S': {'Count': 1, 'Chance': 33.333333333333336}}, 
                                        'Female': {
                                            'F': {'Count': 1, 'Chance': 100.0}}, 
                                        'Surnames': {
                                            'S': {'Count': 1, 'Chance': 100.0}}}, 
                                    'Letters': {
                                        'Male': {
                                            'm': {'Count': 1, 'Chance': 100.0}, 
                                            'a': {'Count': 1, 'Chance': 100.0}}, 
                                        'Common': {
                                            'm': {'Count': 1, 'Chance': 33.333333333333336}, 
                                            'a': {'Count': 1, 'Chance': 33.333333333333336}, 
                                            'f': {'Count': 1, 'Chance': 33.333333333333336}, 
                                            'e': {'Count': 1, 'Chance': 33.333333333333336}, 
                                            's': {'Count': 1, 'Chance': 33.333333333333336}, 
                                            'u': {'Count': 1, 'Chance': 33.333333333333336}}, 
                                        'Female': {
                                            'f': {'Count': 1, 'Chance': 100.0}, 
                                            'e': {'Count': 1, 'Chance': 100.0}}, 
                                        'Surnames': {
                                            's': {'Count': 1, 'Chance': 100.0}, 
                                            'u': {'Count': 1, 'Chance': 100.0}}}, 
                                    'Vowels_Chains': {
                                        'Chains': {
                                            'Male': {
                                                'a': {'Count': 1, 'Chance': 100.0}}, 
                                            'Common': {
                                                'a': {'Count': 1, 'Chance': 33.333333333333336}, 
                                                'e': {'Count': 1, 'Chance': 33.333333333333336}, 
                                                'u': {'Count': 1, 'Chance': 33.333333333333336}}, 
                                            'Female': {
                                                'e': {'Count': 1, 'Chance': 100.0}}, 
                                            'Surnames': {
                                                'u': {'Count': 1, 'Chance': 100.0}}}, 
                                        'Chain_Frequency': {
                                            'Male': {
                                                1: {'Count': 1, 'Chance': 100.0}}, 
                                            'Common': {
                                                1: {'Count': 3, 'Chance': 100.0}}, 
                                            'Female': {
                                                1: {'Count': 1, 'Chance': 100.0}}, 
                                            'Surnames': {
                                                1: {'Count': 1, 'Chance': 100.0}}}, 
                                        'Length_Count_Names': {
                                            'Male': {
                                                '1_1': {
                                                    'Max_Count_In_Name': 1, 
                                                    'Names_Count': 1, 
                                                    'Chance': 100.0}}, 
                                            'Common': {
                                                '1_1': {
                                                    'Max_Count_In_Name': 1, 
                                                    'Names_Count': 3, 
                                                    'Chance': 100.0}}, 
                                            'Female': {
                                                '1_1': {
                                                    'Max_Count_In_Name': 1, 
                                                    'Names_Count': 1, 
                                                    'Chance': 100.0}}, 
                                            'Surnames': {
                                                '1_1': {
                                                    'Max_Count_In_Name': 1, 
                                                    'Names_Count': 1, 
                                                    'Chance': 100.0}}}
                                        }, 
                                    'Consonants_Chains': {
                                        'Chains': {
                                            'Male': {
                                                'm': {'Count': 1, 'Chance': 100.0}}, 
                                            'Common': {
                                                'm': {'Count': 1, 'Chance': 33.333333333333336}, 
                                                'f': {'Count': 1, 'Chance': 33.333333333333336}, 
                                                's': {'Count': 1, 'Chance': 33.333333333333336}}, 
                                            'Female': {
                                                'f': {'Count': 1, 'Chance': 100.0}}, 
                                            'Surnames': {
                                                's': {'Count': 1, 'Chance': 100.0}}}, 
                                        'Chain_Frequency': {
                                            'Male': {
                                                1: {'Count': 1, 'Chance': 100.0}}, 
                                            'Common': {
                                                1: {'Count': 3, 'Chance': 100.0}}, 
                                            'Female': {
                                                1: {'Count': 1, 'Chance': 100.0}}, 
                                            'Surnames': {
                                                1: {'Count': 1, 'Chance': 100.0}}}, 
                                        'Length_Count_Names': {
                                            'Male': {
                                                '1_1': {
                                                    'Max_Count_In_Name': 1, 
                                                    'Names_Count': 1, 
                                                    'Chance': 100.0}}, 
                                            'Common': {
                                                '1_1': {'Max_Count_In_Name': 1, 
                                                'Names_Count': 3, 
                                                'Chance': 100.0}}, 
                                            'Female': {
                                                '1_1': {
                                                    'Max_Count_In_Name': 1, 
                                                    'Names_Count': 1, 
                                                    'Chance': 100.0}}, 
                                            'Surnames': {
                                                '1_1': {
                                                    'Max_Count_In_Name': 1, 
                                                    'Names_Count': 1, 
                                                    'Chance': 100.0}}}
                                        }, 
                                    'Chains_Combinations': {
                                        'Male': {
                                            'ma': {'Count': 1, 'Chance': 100.0}}, 
                                        'Common': {
                                            'ma': {'Count': 1, 'Chance': 33.333333333333336}, 
                                            'fe': {'Count': 1, 'Chance': 33.333333333333336}, 
                                            'su': {'Count': 1, 'Chance': 33.333333333333336}}, 
                                        'Female': {
                                            'fe': {'Count': 1, 'Chance': 100.0}}, 
                                        'Surnames': {
                                            'su': {'Count': 1, 'Chance': 100.0}}}, 
                                    'Name_Endings': {
                                        'Male': {
                                            'ma': {'Count': 1, 'Chance': 100.0}}, 
                                        'Common': {
                                            'ma': {'Count': 1, 'Chance': 33.333333333333336}, 
                                            'fe': {'Count': 1, 'Chance': 33.333333333333336}, 
                                            'su': {'Count': 1, 'Chance': 33.333333333333336}}, 
                                        'Female': {
                                            'fe': {'Count': 1, 'Chance': 100.0}}, 
                                        'Surnames': {
                                            'su': {'Count': 1, 'Chance': 100.0}}}
                                })

        
    @FunctionalClass.descript
    def test_formatLocalAnalyticDB_checkingCreatedValues_expectedCountedValues(
            self) -> typing.NoReturn:
        '''
        Testing the method of making analytic data base. 
        Only sample data is used to verify.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
     
        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData
        self.TestConstruction.tmp_NamesDB = {'Male': ['Ma'],
                                             'Female': ['Fe'], 
                                             'Surnames': ['Su']}

        groupKeys = ['Male', 'Female', 'Surnames']

        self.TestConstruction.formatLocalAnalyticDB(groupKeys)
        
        data = self.TestConstruction.tmp_NamesAnalytic['TestRace']
        res = { 'Max_Names_Count': data['Max_Names_Count'], 
                'Male_Names_Count': data['Male_Names_Count'], 
                'Female_Names_Count': data['Female_Names_Count'], 
                'Surnames_Count': data['Surnames_Count'],
                'First_Letters': data['First_Letters']}

        self.assertDictEqual(res, {
                                    'Max_Names_Count': 3, 
                                    'Male_Names_Count': 1, 
                                    'Female_Names_Count': 1, 
                                    'Surnames_Count': 1,
                                    'First_Letters': {
                                        'Vowels_Count': 0, 
                                        'Consonants_Count': 3, 
                                        'Male': {
                                            'M': {'Count': 1, 'Chance': 100.0}}, 
                                        'Common': {
                                            'M': {'Count': 1, 'Chance': 33.333333333333336}, 
                                            'F': {'Count': 1, 'Chance': 33.333333333333336}, 
                                            'S': {'Count': 1, 'Chance': 33.333333333333336}}, 
                                        'Female': {
                                            'F': {'Count': 1, 'Chance': 100.0}}, 
                                        'Surnames': {
                                            'S': {'Count': 1, 'Chance': 100.0}}}, 
                                    })


    @FunctionalClass.descript
    def test_extractingNamesByGroupKey_checkingCreatedDB_expectedGenderLists(
            self) -> typing.NoReturn:
        '''
        Testing the method of extracting a lists of names 
        and saving by the gender/surname.
        '''
        race = {'TestRace': {'Genders': {
            'Female': {'Names': ['Fe']}, 
            'Male': {'Names': ['Ma', 'Me']}}, 
            'Surnames': ['Su']}}

        self.TestConstruction.extractingNamesByGroupKey(race)
        
        res = self.TestConstruction.tmp_NamesDB

        self.assertDictEqual(res,  {'Female': ['Fe'], 
                                    'Male': ['Ma', 'Me'],
                                    'Surnames': ['Su']})

        
    @FunctionalClass.descript
    def test_fillGlobNamesAnalyticVar_checkingCopyedData_expectedCopyedData(
            self) -> typing.NoReturn:
        '''
        Testing the method of filling a global naming 
        analytic database variable.
        '''
        NamesAnalyticData = self.deepCopy(self.NamesAnalyticData)
        allowedKeys = ['Max_Names_Count', 'Male_Names_Count', 'Female_Names_Count',
                    'Surnames_Count', 'First_Letters']
        NamesAnalyticData['TestRace'] = self.leaveKeys(allowedKeys, NamesAnalyticData['TestRace'])
        
        testRaceData = NamesAnalyticData['TestRace']
        testRaceData['Max_Names_Count'] = 3
        testRaceData['Male_Names_Count'] = 1
        testRaceData['Female_Names_Count'] = 1
        testRaceData['Surnames_Count'] = 1
        testRaceData['First_Letters'] = {'Vowels_Count': 0, 'Consonants_Count': 3, 
                'Male': { 'M': {'Count': 1, 'Chance': 100.0}}, 
                'Common': {
                    'M': {'Count': 1, 'Chance': 33.333333333333336}, 
                    'F': {'Count': 1, 'Chance': 33.333333333333336}, 
                    'S': {'Count': 1, 'Chance': 33.333333333333336}}, 
                'Female': { 'F': {'Count': 1, 'Chance': 100.0}}, 
                'Surnames': { 'S': {'Count': 1, 'Chance': 100.0}}}
     
        self.TestConstruction.globNamesAnalytic = {"Analytics": {}}
        self.TestConstruction.tmp_NamesAnalytic = NamesAnalyticData

        self.TestConstruction.fillGlobNamesAnalyticVar()

        res = self.TestConstruction.globNamesAnalytic
        self.assertDictEqual(res, {"Analytics": {'TestRace': {
                                        'Max_Names_Count': 3, 
                                        'Male_Names_Count': 1, 
                                        'Female_Names_Count': 1, 
                                        'Surnames_Count': 1,
                                        'First_Letters': {
                                            'Vowels_Count': 0, 
                                            'Consonants_Count': 3, 
                                            'Male': {
                                                'M': {'Count': 1, 'Chance': 100.0}}, 
                                            'Common': {
                                                'M': {'Count': 1, 'Chance': 33.333333333333336}, 
                                                'F': {'Count': 1, 'Chance': 33.333333333333336}, 
                                                'S': {'Count': 1, 'Chance': 33.333333333333336}}, 
                                            'Female': {
                                                'F': {'Count': 1, 'Chance': 100.0}}, 
                                            'Surnames': {
                                                'S': {'Count': 1, 'Chance': 100.0}}}, 
                                        }}
                                    })

        
    @FunctionalClass.descript
    def test_makeAnalyticData_checkingCreatedValues_expectedCountedValues(
            self) -> typing.NoReturn:
        '''
        Testing the method of making all analytic data base. 
        Only sample data is used to verify.
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

        self.TestConstruction.makeAnalyticData()
        
        data = self.TestConstruction.globNamesAnalytic[
                                        'Analytics']['TestRace']
        res = { 'Max_Names_Count': data['Max_Names_Count'], 
                'Male_Names_Count': data['Male_Names_Count'], 
                'Female_Names_Count': data['Female_Names_Count'], 
                'Surnames_Count': data['Surnames_Count'],
                'First_Letters': data['First_Letters']}
                
        self.assertDictEqual(res, { 'Max_Names_Count': 4, 
                                    'Male_Names_Count': 2, 
                                    'Female_Names_Count': 1, 
                                    'Surnames_Count': 1,
                                    'First_Letters': {
                                        'Vowels_Count': 0, 
                                        'Consonants_Count': 4, 
                                        'Male': {
                                            'M': {'Count': 2, 'Chance': 100.0}}, 
                                        'Common': {
                                            'M': {'Count': 2, 'Chance': 50.0}, 
                                            'F': {'Count': 1, 'Chance': 25.0}, 
                                            'S': {'Count': 1, 'Chance': 25.0}}, 
                                        'Female': {
                                            'F': {'Count': 1, 'Chance': 100.0}}, 
                                        'Surnames': {
                                            'S': {'Count': 1, 'Chance': 100.0}}
                                        }, 
                                    })

        
    @FunctionalClass.descript
    def test_printResponds_checkingCreatedValues_expectedCountedValues(
            self) -> typing.NoReturn:
        '''
        Testing the method of making all analytic data base. 
        Only sample data is used to verify.
        '''
        
        responds = dict({'testRace': ["TestRespond", "TestRespondTwo"]})
        expected_responds = list(['---ANALYSIS-STARTED---', '', '',
                                '*AnalyticDB* Race:  testRace', 
                                'TestRespond', 'TestRespondTwo', '', 
                                '---ANALYSIS-FINISHED---',])
        obtained_responds = list()

        self.TestConstruction.printResponds(responds)

        with open(self.TestConstruction.logFilePath, 'r') as f:
            obtained_responds = [str(name).strip('\n') for name in f]

        self.assertEqual(obtained_responds, expected_responds)

        
    @FunctionalClass.descript
    def test_makeAnalyticDB_checkingCreatedDB_expectedWritedData(
            self) -> typing.NoReturn:
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

        testDBFile = self.TestFileDirectory + 'tmpDBAnalytic.cfg'
        self.TestConstruction.makeAnalyticDB(testDBFile)

        with open(testDBFile, 'r') as f:
            readedData = f.read()
            if readedData:
                readedData = dict(ast.literal_eval(readedData))

        data = readedData['Analytics']['TestRace']
        res = { 'Max_Names_Count': data['Max_Names_Count'], 
                'Male_Names_Count': data['Male_Names_Count'], 
                'Female_Names_Count': data['Female_Names_Count'], 
                'Surnames_Count': data['Surnames_Count'],
                'First_Letters': data['First_Letters']}
        
        self.assertDictEqual(res, { 'Max_Names_Count': 4, 
                                    'Male_Names_Count': 2, 
                                    'Female_Names_Count': 1, 
                                    'Surnames_Count': 1,
                                    'First_Letters': {
                                        'Vowels_Count': 0, 
                                        'Consonants_Count': 4, 
                                        'Male': {
                                            'M': {'Count': 2, 'Chance': 100.0}}, 
                                        'Common': {
                                            'M': {'Count': 2, 'Chance': 50.0}, 
                                            'F': {'Count': 1, 'Chance': 25.0}, 
                                            'S': {'Count': 1, 'Chance': 25.0}}, 
                                        'Female': {
                                            'F': {'Count': 1, 'Chance': 100.0}}, 
                                        'Surnames': {
                                            'S': {'Count': 1, 'Chance': 100.0}}
                                        }, 
                                    })
###FINISH FunctionalBlock

###START MainBlock
def main():
    pass
###FINISH Mainblock