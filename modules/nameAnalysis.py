###START ImportBlock
##systemImport
import functools
import pickle as cPickle

import typing
from contextlib import redirect_stdout
from typing import Union
from pathlib import Path as PathType

##customImport
from configs.CFGNames import ANALYTIC_DB_FILE
from configs.CFGNames import LOCAL_ANALYSIS_LOG_FILE
from configs.CFGNames import VOWELS_LETTERS, CONSONANTS_LETTERS
from configs.CFGNames import GROUP_KEYS

from templates.templateAnalysis import TEMPLATE_GLOBAL_ANALYTIC
from templates.templateAnalysis import TEMPLATE_NAMES_ANALYTIC
from templates.templateAnalysis import TEMPLATE_RATING_ANALYTIC
from templates.templateAnalysis import TEMPLATE_CHAINS_ANALYTIC

from modules.nameReader import FileWork

###FINISH ImportBlock

###START GlobalConstantBlock
###FINISH GlobalConstantBlock


###START DecoratorBlock
def redirectOutput(redirectedFunction: typing.Callable) -> typing.Callable:
    '''
    Redirects output to log file for #redirectedFunction. After returns stdout back.
    '''
    @functools.wraps(redirectedFunction)
    def wrapper(*args, **kwargs):
        self = args[0]
        
        with open(self.logFilePath, 'w') as f, redirect_stdout(f):
            print("---ANALYSIS-STARTED---\n")
            res = redirectedFunction(*args, **kwargs)
            print("\n---ANALYSIS-FINISHED---")

        return res

    return wrapper

###FINISH DecoratorBlock


###START FunctionalBlock
class AnalysysService:
    def __init__(self,
                 testFile: Union[str, PathType] = None) -> typing.NoReturn:
        self.logFilePath = LOCAL_ANALYSIS_LOG_FILE
        
        self.baseOfNames = dict(
        )  #variable for storing names from #DBNames/NamesBaseInitializing.cfg
        self.globNamesAnalytic = dict(
        )  #variable for storing complete analytic of names
        self.tmp_NamesAnalytic = dict(
        )  #variable for temporary storing analytic of names
        self.tmp_NamesDB = dict(
        )  #variable for temporary storing names for current race
        self.raceNameKey = ""  #current race name
        self.groupKey = ""  #gender or surname (male, female, surname)
        self.localAnalyticKey = ""  #contains one key from keys pasts in AnalyticDB
        self.FirstOnly = None  #using for the only first iteration
        self._tmp_groupKey = None

        self.getBaseOfNames(testFile)
        self.initGlobNamesAnalytics()

        #Group keys
        self.GroupKey_Male = GROUP_KEYS[0]
        self.GroupKey_Female = GROUP_KEYS[1]
        self.GroupKey_Surnames = GROUP_KEYS[2]
        self.GroupSubKey_Common = "Common"

        #Keys used
        self.maxNamesCountKey = "Max_Names_Count"
        self.maleNamesCountKey = "Male_Names_Count"
        self.femaleNamesCountKey = "Female_Names_Count"
        self.surnamesCountKey = "Surnames_Count"

        #Keys of #TEMPLATE_RATING_ANALYTIC
        self.ratingAnalytic_CountKey = "Count"
        self.ratingAnalytic_ChanceKey = "Chance"

    def initNamesAnalytics(self) -> typing.NoReturn:
        '''
        Initializing #tmp_NamesAnalytic by value #TEMPLATE_NAMES_ANALYTIC.
        '''
        self.tmp_NamesDB = dict()

        _tmpDump = cPickle.dumps(TEMPLATE_NAMES_ANALYTIC, -1)
        self.tmp_NamesAnalytic = cPickle.loads(_tmpDump)

    def initGlobNamesAnalytics(self) -> typing.NoReturn:
        '''
        Initializing instance variables by initial values.
        '''
        _tmpDump = cPickle.dumps(TEMPLATE_GLOBAL_ANALYTIC, -1)
        self.globNamesAnalytic = cPickle.loads(_tmpDump)

        self.initNamesAnalytics()

    def isiterable(self, checkedObject: typing.Any) -> bool:
        '''Checks if object is iterable.'''
        try:
            iter(checkedObject)
        except TypeError:
            return False
        return True

    def islastgropkey(self) -> bool:
        '''
        Check is a group key last.
        '''
        lastGroupKey = GROUP_KEYS[-1]
        if self.groupKey == lastGroupKey:
            return True
        return False

    def copyObjectData(self, obj: object) -> typing.NoReturn:
        '''Copies object data to global variables.'''
        self.globNamesAnalytic = obj.globNamesAnalytic
        self.tmp_NamesAnalytic = obj.tmp_NamesAnalytic
        self.tmp_NamesDB = obj.tmp_NamesDB
        self.raceNameKey = obj.raceNameKey
        self.groupKey = obj.groupKey
        self.localAnalyticKey = obj.localAnalyticKey
        self.FirstOnly = obj.FirstOnly

    def renameDictKey(self, tmp_dict: dict, key1: str,
                      key2: str) -> typing.NoReturn:
        '''Renames first key name on second in dictionary.'''
        tmp_dict[key1] = tmp_dict.pop(key2)

    def increaceCountforAllSubkeys(self,
                                         destinationData: typing.Dict[str,
                                                                      dict],
                                         sourceData: typing.Dict[str, dict]):
        '''
        Increaces count by all subkeys inside current local analytic key.
        '''
        for localSubkey in sourceData:
            destinationData[localSubkey] += sourceData[localSubkey]

    def getBaseOfNames(self,
                       testFile: Union[str,
                                       PathType] = None) -> typing.NoReturn:
        '''
        Gets base of names from file and saves data to #self.baseOfNames.
        '''
        if not testFile:
            self.baseOfNames = FileWork.readDataFile()
        else:
            self.baseOfNames = FileWork.readDataFile(fileName=testFile)

    def getFirstUnknownDictKeyName(self,
                                   tmp_dict: dict) -> typing.Union[str, None]:
        '''
        Returns key name from dictionary if have only one key.
        '''

        if len(tmp_dict.keys()) == 1:
            for unknownKeyName in tmp_dict.keys():
                return unknownKeyName

        return None

    def getLocalAnalyticData(self) -> typing.Dict[str, dict]:
        '''
        Returns local analytic data for current local analytic key.
        Used deepcopy analogue.
        '''
        raceData = self.tmp_NamesAnalytic[self.raceNameKey]

        _tmpDump = cPickle.dumps(raceData[self.localAnalyticKey], -1)
        localAnalyticData = cPickle.loads(_tmpDump)

        return localAnalyticData

    def getCountByAnalyticKey(self, key: str) -> int:
        '''
        Returns rating count key by local analytic for current key.
        '''
        countKey = self.ratingAnalytic_CountKey

        localAnalyticData = self.getLocalAnalyticData()
        count = localAnalyticData[self.groupKey][key][countKey]

        return count

    def getMaxCountByKey(self, key: str) -> int:
        '''Returns count of names by key by current race.'''
        return self.tmp_NamesAnalytic[self.raceNameKey][key]

    def getMaleNamesCount(self) -> int:
        '''Returns count of male names by current race.'''
        return self.getMaxCountByKey(self.maleNamesCountKey)

    def getFemaleNamesCount(self) -> int:
        '''Returns count of female names by current race.'''
        return self.getMaxCountByKey(self.femaleNamesCountKey)

    def getSurnamesCount(self) -> int:
        '''Returns count of surnames by current races.'''
        return self.getMaxCountByKey(self.surnamesCountKey)

    def getAllNamesCount(self) -> int:
        '''
        Returns count of names for all (male, female, surnames) 
        by current race.
        '''
        return self.getMaxCountByKey(self.maxNamesCountKey)

    def setCommonGroupKey(self) -> typing.NoReturn:
        '''
        Sets current the group key to common.
        The current group key is stored in tmp var.
        '''
        self._tmp_groupKey = self.groupKey
        self.groupKey = self.GroupSubKey_Common

    def unsetCommonGroupKey(self) -> typing.NoReturn:
        '''
        Restores group key from tmp var.
        '''
        if self._tmp_groupKey:
            self.groupKey = self._tmp_groupKey
            self._tmp_groupKey = None

    def setRatingDataByLocalAnalytic(self,
                                     ratingData: typing.Dict[str, dict],
                                     subKey: str = None) -> bool:
        '''
        Sets the new local data to temporary Names AnalyticDB by local key.
        '''
        if subKey:
            self.tmp_NamesAnalytic[self.raceNameKey][self.localAnalyticKey][
                subKey][self.groupKey] = ratingData[self.groupKey]
            return True

        else:
            self.tmp_NamesAnalytic[self.raceNameKey][self.localAnalyticKey][
                self.groupKey] = ratingData[self.groupKey]
            return True

        return False

    def setCommonRattingData(self,
                             ratingData: typing.Dict[str, dict],
                             subKey: str = None) -> bool:
        '''
        Sets the new only common data to temporary Names AnalyticDB by local key.
        '''
        self.setCommonGroupKey()

        doneFlag = self.setRatingDataByLocalAnalytic(ratingData, subKey)
        self.unsetCommonGroupKey()

        if not doneFlag:
            return False
        return True

    def prepareRatingAnalytic(self, newKey: str) -> typing.Dict[str, dict]:
        '''
        Returns prepared template of rating analytic (#TEMPLATE_RATING_ANALYTIC) 
        for the certain key (#newKey).
        '''
        _tmpDump = cPickle.dumps(TEMPLATE_RATING_ANALYTIC, -1)
        localAnalytic = cPickle.loads(_tmpDump)

        self.renameDictKey(localAnalytic, newKey, "tmp_Key")
        return dict(localAnalytic)

    def calcChanceByKey(self, count: int, countByGroupKey: int) -> float:
        '''
        Calculates chance by count key of the current group key.
        '''
        if not countByGroupKey:
            return float(0)

        chance = count * 100 / countByGroupKey
        return chance

    def calculateNamesCountByLocalAnalytic(
            self, namesCount: int, localAnalyticKey: str) -> typing.NoReturn:
        '''
        Calculates how much names by the group key.
        '''
        oldCount = self.tmp_NamesAnalytic[self.raceNameKey][localAnalyticKey]
        newCount = oldCount + namesCount
        self.tmp_NamesAnalytic[self.raceNameKey][localAnalyticKey] = newCount

    def calcMaxNamesCount(self) -> str:
        '''
        Calculates how much names in initialized DB.
        '''

        namesCount = len(self.tmp_NamesDB[self.groupKey])
        self.calculateNamesCountByLocalAnalytic(namesCount,
                                                self.maxNamesCountKey)

        if self.groupKey == self.GroupKey_Male:
            self.calculateNamesCountByLocalAnalytic(namesCount,
                                                    self.maleNamesCountKey)

        elif self.groupKey == self.GroupKey_Female:
            self.calculateNamesCountByLocalAnalytic(namesCount,
                                                    self.femaleNamesCountKey)

        elif self.groupKey == self.GroupKey_Surnames:
            self.calculateNamesCountByLocalAnalytic(namesCount,
                                                    self.surnamesCountKey)

        else:
            return ("calcMaxNamesCount: Error: Unknown Key Name: %s" %
                    self.groupKey)

        return "calcMaxNamesCount: Done"

    def calcAllChances(self, count: int) -> typing.Tuple[float, float]:
        '''
        Calculates chance and common chance by count key of the current group key.
        '''
        chance = 0

        if self.groupKey == self.GroupKey_Male:
            maleCount = self.getMaleNamesCount()
            chance = self.calcChanceByKey(count, maleCount)

        elif self.groupKey == self.GroupKey_Female:
            femCount = self.getFemaleNamesCount()
            chance = self.calcChanceByKey(count, femCount)

        elif self.groupKey == self.GroupKey_Surnames:
            surCount = self.getSurnamesCount()
            chance = self.calcChanceByKey(count, surCount)

        elif self.groupKey == self.GroupSubKey_Common:
            allCount = self.getAllNamesCount()
            chance = self.calcChanceByKey(count, allCount)

        return chance

    def calculateCountByKey(
            self, key: str,
            ratingData: typing.Dict[str, dict]) -> typing.Dict[str, dict]:
        '''
        Creates rating data by calculating the key count.
        Used keys: self.groupKey.
        '''
        countKey = self.ratingAnalytic_CountKey

        if not key in ratingData[self.groupKey]:
            localAnaliticData = self.prepareRatingAnalytic(key)
            ratingData[self.groupKey][key] = dict(localAnaliticData[key])

        ratingData[self.groupKey][key][countKey] += 1

        return ratingData

    def calculateRatingByKey(
            self, key: str,
            ratingData: typing.Dict[str, dict]) -> typing.Dict[str, dict]:
        '''
        Calculating chance of occurrence key.
        Used keys: self.groupKey.
        '''
        countKey = self.ratingAnalytic_CountKey
        chanceKey = self.ratingAnalytic_ChanceKey

        curCount = ratingData[self.groupKey][key][countKey]
        curChance = self.calcAllChances(curCount)

        ratingData[self.groupKey][key][chanceKey] = curChance

        return ratingData

    def calculateRatingforCommonSubkey(self, subKey: str,
                                       ratingData: typing.Dict[str, dict]):
        '''
        Calculating chance of common subkey.
        '''
        self.setCommonGroupKey()

        ratingData = self.calculateRatingByKey(subKey, ratingData)

        self.unsetCommonGroupKey()

        return ratingData

    def makeCommonRatingData(self, subKey: str = None) -> bool:
        '''
        Creates, calculates and save maked analytic data for common group 
        key by current the analytic key (#localAnalyticKey).
        '''
        commonAnalyticData = dict({self.GroupSubKey_Common: {}})
        localAnalyticData = self.getLocalAnalyticData()

        if subKey:
            localAnalyticData = localAnalyticData[subKey]

        if self.GroupSubKey_Common in localAnalyticData:
            commonAnalyticData[self.GroupSubKey_Common] = localAnalyticData[
                self.GroupSubKey_Common]

        for localKey in localAnalyticData[self.groupKey]:
            if localKey not in commonAnalyticData[
                    self.GroupSubKey_Common].keys():
                commonAnalyticData[self.GroupSubKey_Common][
                    localKey] = localAnalyticData[self.groupKey][localKey]

            else:
                self.increaceCountforAllSubkeys(
                    commonAnalyticData[self.GroupSubKey_Common][localKey],
                    localAnalyticData[self.groupKey][localKey])

            commonAnalyticData = self.calculateRatingforCommonSubkey(
                localKey, commonAnalyticData)

        if not self.setCommonRattingData(commonAnalyticData, subKey):
            return False

        return True

    def makeLocalAnalyticData(self,
                              localFunc: typing.Callable,
                              subKey: str = None) -> bool:
        '''
        Creates, calculates and save maked analytic data for current the analytic key (#localAnalyticKey).
        '''

        self.FirstOnly = False
        ratingData = dict({self.groupKey: {}})

        for name in self.tmp_NamesDB[self.groupKey]:
            returnedData = localFunc(name)

            if self.isiterable(returnedData):
                for iterationKey in returnedData:
                    ratingData = self.calculateCountByKey(
                        iterationKey, ratingData)
                    ratingData = self.calculateRatingByKey(
                        iterationKey, ratingData)

            else:
                tmp_key = returnedData
                ratingData = self.calculateCountByKey(tmp_key, ratingData)
                ratingData = self.calculateRatingByKey(tmp_key, ratingData)

        if not self.setRatingDataByLocalAnalytic(ratingData, subKey):
            return False

        if not self.makeCommonRatingData(subKey):
            return False

        return True


class AnalyticLetters(AnalysysService):
    def __init__(self,
                 analysisObj: object,
                 testFile: Union[str, PathType] = None):
        super().__init__(testFile)

        self.copyObjectData(analysisObj)

        #Keys used
        self.nameLettersCountKey = "Name_Letters_Count"
        self.vowelsCountKey = "Vowels_Count"
        self.consonantsCountKey = "Consonants_Count"

        self.firstLettersKey = "First_Letters"
        self.firstLetters_VowelsCountSubkey = "Vowels_Count"
        self.firstLetters_ConsonantsCountSubkey = "Consonants_Count"

        self.lettersKey = "Letters"
        self.nameEndingsKey = "Name_Endings"

    def getFirstLetters(self) -> typing.List[str]:
        '''
        Returns all first letters.
        '''
        raceData = self.tmp_NamesAnalytic[self.raceNameKey]
        firstLetters = raceData[self.firstLettersKey][self.groupKey]
        return list(firstLetters.keys())

    def getFirstLettersMaxCountByKey(self, key: str) -> int:
        '''
        Returns the max counts of first letters by the key.
        '''
        raceData = self.tmp_NamesAnalytic[self.raceNameKey]
        count = raceData[self.firstLettersKey][key]
        return count

    def setFirstLettersMaxCountByKey(self, key: str, count: int) -> bool:
        '''
        Sets the max counts of first letters by the key.
        '''
        self.tmp_NamesAnalytic[self.raceNameKey][
            self.firstLettersKey][key] = count
        return True

    def calcFirstLetters(self) -> bool:
        '''
        Calculates vowel and consonant letters between all first letters.
        '''
        vowKey = self.firstLetters_VowelsCountSubkey
        consKey = self.firstLetters_ConsonantsCountSubkey

        vowCount = self.getFirstLettersMaxCountByKey(vowKey)
        consCount = self.getFirstLettersMaxCountByKey(consKey)
        firstLetters = self.getFirstLetters()

        for letter in firstLetters:
            letterCount = self.getCountByAnalyticKey(letter)

            if str(letter).lower() in VOWELS_LETTERS:
                vowCount += letterCount
            else:
                consCount += letterCount

        if not self.setFirstLettersMaxCountByKey(vowKey, vowCount):
            return False
        if not self.setFirstLettersMaxCountByKey(consKey, consCount):
            return False

        return True

    def makeNameLettersCountData(self) -> str:
        '''
        Makes data with a names lenght and their repeats amount.
        '''
        self.localAnalyticKey = self.nameLettersCountKey

        def tmp_getNameLenghtFunc(name: str) -> str:
            '''Gets name lenght.'''
            res = len(str(name))
            return str(res)

        if not self.makeLocalAnalyticData(tmp_getNameLenghtFunc):
            return "makeNameLettersCountData: Error: Can't make data"

        return "makeNameLettersCountData: Done"

    def makeVowelsCountData(self) -> str:
        '''
        Makes data with vowels amount in names and their repeats amount.
        '''
        self.localAnalyticKey = self.vowelsCountKey

        def tmp_getVowelsCountFunc(name: str) -> int:
            """Gets count of vowel letters in name."""
            count = 0

            for letter in str(name.lower()):
                if letter in VOWELS_LETTERS:
                    count += 1

            return count

        if not self.makeLocalAnalyticData(tmp_getVowelsCountFunc):
            return "makeVowelsCountData: Error: Can't make data"

        return "makeVowelsCountData: Done"

    def makeConsonantsCountData(self) -> str:
        '''
        Makes data with consonants amount in names and their repeats amount.
        '''
        self.localAnalyticKey = self.consonantsCountKey

        def tmp_getConsonantsCountFunc(name: str) -> int:
            """Gets count of consonant letters in name."""
            count = 0

            for letter in str(name.lower()):
                if letter not in VOWELS_LETTERS:
                    count += 1

            return count

        if not self.makeLocalAnalyticData(tmp_getConsonantsCountFunc):
            return "makeConsonantsCountData: Error: Can't make data"

        return "makeConsonantsCountData: Done"

    def makeFirstLetterCountData(self) -> str:
        '''
        Makes data with first letters in names and their repeats amount. 
        Also counts names with a vowels and consonant first letters.
        '''
        self.localAnalyticKey = self.firstLettersKey

        def tmp_FirstLettersFunc(name: str) -> str:
            '''Gets first letter of name.'''
            firstLetter = str(name)[0]
            return firstLetter

        if not self.makeLocalAnalyticData(tmp_FirstLettersFunc):
            return "makeFirstLetterCountData: Error: Can't make data"
        if not self.calcFirstLetters():
            return "makeFirstLetterCountData: Error: Can't calculate first letters"

        return "makeFirstLetterCountData: Done"

    def makeAllLettersData(self) -> str:
        '''
        Makes data with all letters, used in names, and their repeats 
        amount.
        '''
        self.localAnalyticKey = self.lettersKey

        def tmp_getAllLettersFunc(name: str) -> str:
            '''Gets each letter of name.'''
            for letter in name:
                edtLetter = str(letter).lower()
                yield edtLetter

        if not self.makeLocalAnalyticData(tmp_getAllLettersFunc):
            return "makeAllLettersData: Error: Can't make data"

        return "makeAllLettersData: Done"

    def makeNameEndingsData(self):
        '''
        Makes data with combinations of two adjacent letters chains from 
        the ends of names, includings one letter chains, and their repeats 
        amount.
        '''
        self.localAnalyticKey = self.nameEndingsKey

        def tmp_getNameEndingsData(name: str) -> str:
            '''
            Gets names endings from #maxChangesCount 
            changes consonant or vowel letters.
            (Yield cuz str is iterable, but need all string)
            '''
            reversedName = ''.join(reversed(name))
            changesCount = 0
            maxChangesCount = 3
            nameEnding = ''
            alphabet = ''

            for letter in reversedName:
                letter = letter.lower()

                if letter in VOWELS_LETTERS:
                    if alphabet == 'cons' or alphabet == '':
                        alphabet = 'vow'
                        changesCount += 1

                if letter not in VOWELS_LETTERS:
                    if alphabet == 'vow' or alphabet == '':
                        alphabet = 'cons'
                        changesCount += 1

                if changesCount > maxChangesCount:
                    break

                nameEnding += letter

            nameEnding = ''.join(reversed(nameEnding))
            yield nameEnding

        if not self.makeLocalAnalyticData(tmp_getNameEndingsData):
            return "makeNameEndingsData: Error: Can't make data"

        return "makeNameEndingsData: Done"


class AnalyticChains(AnalysysService):
    def __init__(self,
                 analysisObj: object,
                 testFile: Union[str, PathType] = None):
        super().__init__(testFile)

        self.copyObjectData(analysisObj)

        self.alphabet = ""

        #Keys used
        self.vowelsChainsKey = "Vowels_Chains"
        self.consonantsChainsKey = "Consonants_Chains"

        self.xChains_ChainsSubkey = "Chains"
        self.xChains_ChainsCountsSubkey = "Chains_Counts"
        self.xChains_ChainFrequencySubkey = "Chain_Frequency"
        self.xChains_LengthCountNamesSubkey = "Length_Count_Names"

        #Keys of #TEMPLATE_CHAINS_ANALYTIC
        self.chainsAnalytic_MaxCountInNameSubkey = "Max_Count_In_Name"
        self.chainsAnalytic_NamesCountSubkey = "Names_Count"
        self.chainsAnalytic_ChanceSubkey = self.ratingAnalytic_ChanceKey

    def nullifyCount(
            self, chainNames: typing.Dict[str, dict],
            lenChainNamesData: typing.Dict[str,
                                           dict]) -> typing.Dict[str, dict]:
        '''
        Makes certain count data equal to zero.
        '''
        countKey = self.ratingAnalytic_CountKey

        for chainName in chainNames.keys():
            lenChainName = len(str(chainName))

            if lenChainName not in lenChainNamesData:
                lenChainNamesData[lenChainName] = dict()

            lenChainNamesData[lenChainName][countKey] = 0

        return dict(lenChainNamesData)

    def sortChainsByLength(
            self, chainNames: typing.Dict[str,
                                          dict]) -> typing.Dict[str, dict]:
        '''
        Sorts chains by the length.
        '''
        sortedChainNames = dict()

        for key in sorted(chainNames, key=len, reverse=True):
            sortedChainNames[key] = chainNames[key]

        return sortedChainNames

    def makeChainList(self, name: str) -> typing.List[str]:
        '''
        Creates list of chains from the name by current alphabet. Vowel or 
        consonant chain determines by key #self.localAnalyticKey.
        '''
        сhains = list()
        currentChain = str("")

        for letter in name:
            correctedLetter = str(letter).lower()

            if correctedLetter in self.alphabet:
                currentChain += correctedLetter

            elif currentChain != "":
                сhains.append(currentChain)
                currentChain = str("")

            else:
                currentChain = str("")

        if currentChain != "":
            сhains.append(currentChain)

        return list(сhains)

    def getChainsDataByLocalAnalytic(self) -> typing.Dict[str, dict]:
        '''
        Returns chains data from temporary Names AnalyticDB by 
        current Local Analytic Key.
        '''
        localAnalyticData = self.getLocalAnalyticData()
        chainNames = localAnalyticData[self.xChains_ChainsSubkey][
            self.groupKey]

        return dict(chainNames)

    def getChain(self, name: str) -> typing.Iterable[str]:
        '''
        Returns iterate keys for dict. returned key is vowel or 
        consonant chain.
        '''
        сhains = self.makeChainList(name)

        for chain in сhains:
            yield chain

    def getChainCount(self, name: str) -> typing.Iterable[int]:
        '''
        Returns iterate keys for dict. Key is count of vowel or consonant in
        chains. Vowel or consonant determines key #self.localAnalyticKey
        '''
        chainNames = self.getChainsDataByLocalAnalytic()

        keysCounter = 0
        keysAmount = len(chainNames.keys())
        if not self.FirstOnly:

            for chainName in chainNames.keys():
                keysCounter += 1
                if keysCounter >= (keysAmount - 1):
                    self.FirstOnly = True

                lenChainName = len(str(chainName))
                yield lenChainName

    def getChainMaxCountKey(self, name: str) -> typing.Iterable[str]:
        '''
        Returns a key consisting of the length of chain and repets count 
        in the name.
        '''
        countKey = self.chainsAnalytic_MaxCountInNameSubkey
        lenChainNamesData = self.calcChainMaxCountInName(name)

        for lenChainName in lenChainNamesData.keys():
            maxCountInNames = lenChainNamesData[lenChainName][countKey]
            ChainMaxCountKey = ("%s_%s" % (lenChainName, maxCountInNames))
            yield ChainMaxCountKey

    def getChainCountDataByLocalAnalytic(
            self, localKey: str) -> typing.Dict[str, dict]:
        '''
        Returns chains count data from temporary Names AnalyticDB by 
        local key.
        '''
        localAnalyticData = self.getLocalAnalyticData()
        dataByLocalKey = localAnalyticData[localKey]

        if self.groupKey not in dataByLocalKey:
            dataByLocalKey[self.groupKey] = dict()

        lenChainNamesData = dataByLocalKey[self.groupKey]

        return dict(lenChainNamesData)

    def getNullifyedChainCountDataByLocalAnalytic(
            self, localKey: str) -> typing.Dict[str, dict]:
        '''
        Returns chains count data from temporary Names AnalyticDB by 
        local key with nullifyed count.
        '''
        chainNames = self.getChainsDataByLocalAnalytic()
        lenChainNamesData = self.getChainCountDataByLocalAnalytic(localKey)
        lenChainNamesData = self.nullifyCount(chainNames, lenChainNamesData)

        return dict(lenChainNamesData)

    def setLocalChainsAnalyticData(
            self, localKey: str,
            localChainsAnalyticData: typing.Dict[str, dict]) -> bool:
        '''
        Sets the chains rating data to temporary Names AnalyticDB by local key.
        '''
        ratingData = {self.groupKey: dict(localChainsAnalyticData)}

        if not self.setRatingDataByLocalAnalytic(ratingData, localKey):
            return False

        return True

    def transposeDataByChainsAnalyticTemplate(self,
                                              lenChainNamesData: dict) -> bool:
        '''
        Creates and transpose data by #TEMPLATE_CHAINS_ANALYTIC model.
        '''
        countKey = self.ratingAnalytic_CountKey
        maxCountKey = self.chainsAnalytic_MaxCountInNameSubkey
        namesCount = self.chainsAnalytic_NamesCountSubkey
        chanceKey = self.chainsAnalytic_ChanceSubkey

        preparedData = dict()

        for dataKey in lenChainNamesData:
            preparedData.update(self.prepareChainsAnalytic(dataKey))
            newData = preparedData[dataKey]
            oldData = lenChainNamesData[dataKey]

            maxCountInName = dataKey.split("_")[1]

            newData[maxCountKey] = int(maxCountInName)
            newData[namesCount] = oldData.pop(countKey)
            newData[chanceKey] = oldData.pop(chanceKey)

        return preparedData

    def prepareChainsAnalytic(self, newKey: str) -> typing.Dict[str, dict]:
        '''
        Returns prepared template of chains analytic (#TEMPLATE_CHAINS_ANALYTIC) 
        for the certain key (#newKey).
        '''
        _tmpDump = cPickle.dumps(TEMPLATE_CHAINS_ANALYTIC, -1)
        localAnalytic = cPickle.loads(_tmpDump)

        self.renameDictKey(localAnalytic, newKey, "tmp_Length")
        return dict(localAnalytic)

    def prepareDataByChainsAnalyticTemplate(self, analyticSubkey: str) -> bool:
        '''
        Prepares and saves data of the lenght of chain and their repets count in names.
        '''
        #When the common data is finally filled
        #(on the last group key), we convert him too
        groupKeys = [self.groupKey]
        if self.islastgropkey():
            groupKeys.append(self.GroupSubKey_Common)

        for tmp_groupKey in groupKeys:
            if tmp_groupKey == self.GroupSubKey_Common:
                self.setCommonGroupKey()

            lenChainNamesData = self.getChainCountDataByLocalAnalytic(
                analyticSubkey)
            preparedData = self.transposeDataByChainsAnalyticTemplate(
                lenChainNamesData)

            doneFlag = self.setLocalChainsAnalyticData(analyticSubkey,
                                                   preparedData)
            self.unsetCommonGroupKey()
                                                   
            if not doneFlag:
                return False

        return True

    def calcChainMaxCountInName(self, name: str) -> typing.Dict[str, dict]:
        '''
        Calculates the max counts of times the chain a certain length 
        (n.p. of 2 letters; chains may not be the same, but the number of 
        letters is the same) occurs in the same name and how many such 
        names (i.e. n.p. of 2 letters there are as many, of 3 - as many).
        '''
        lowerName = name.lower()
        countKey = self.chainsAnalytic_MaxCountInNameSubkey
        chainNames = self.getChainsDataByLocalAnalytic()
        chainNames = self.sortChainsByLength(chainNames)
        lenChainNamesData = dict()

        for chainName in chainNames.keys():

            if not lowerName and not chainName in lowerName:
                continue

            lenChainName = len(str(chainName))

            splitedName = lowerName.split(chainName)
            repeatsCount = len(splitedName) - 1
            lowerName = "".join(splitedName)

            if repeatsCount == 0:
                continue

            if lenChainName not in lenChainNamesData or\
                        countKey not in lenChainNamesData[lenChainName]:
                lenChainNamesData[lenChainName] = dict({countKey: 0})

            lenChainNamesData[lenChainName][countKey] += repeatsCount

        return dict(lenChainNamesData)

    def calcChainFrequency(self) -> bool:
        '''
        Calculates common chains count in all names and write this 
        data in temporary AnalyticDB. (Shows how often chains occur.)

        (n.a. 2 different chains of 2 letters long occur in the same 
        name, each for 1 time, so we write down the total probability 
        of meeting a chain of 2 letters. So what if the chains themselves 
        are different and, moreover, are found in the same name.
        Later, when generating, if the number of names is less than 
        the number of such chains, then the probability will be more 
        than 100%, which means there is more than one such chains in 
        one name)
        '''
        countKey = self.ratingAnalytic_CountKey

        chainNames = self.getChainsDataByLocalAnalytic()
        chainNames = self.sortChainsByLength(chainNames)
        lenChainNamesData = self.getNullifyedChainCountDataByLocalAnalytic(
            self.xChains_ChainFrequencySubkey)

        for chainName in chainNames.keys():
            lenChainName = len(str(chainName))
            repeatsCount = chainNames[chainName][countKey]

            if lenChainName not in lenChainNamesData:
                lenChainNamesData[lenChainName] = dict()

            lenChainNamesData[lenChainName][countKey] += repeatsCount

        if not self.setLocalChainsAnalyticData(
                self.xChains_ChainFrequencySubkey, lenChainNamesData):
            return False

        return True

    def callcRatingOfChainsBySubkey(self, analyticSubkey: str) -> bool:
        '''
        Calculates local and common chances for the analytic subkey and write this 
        data in temporary AnalyticDB.
        '''
        countKey = self.ratingAnalytic_CountKey
        chanceKey = self.ratingAnalytic_ChanceKey

        ChainNamesData = self.getChainCountDataByLocalAnalytic(analyticSubkey)

        for dataKey in ChainNamesData.keys():
            count = ChainNamesData[dataKey][countKey]
            chance = self.calcAllChances(count)
            ChainNamesData[dataKey][chanceKey] = chance

        if not self.setLocalChainsAnalyticData(analyticSubkey, ChainNamesData):
            return False
        return True

    def calcRatingForAllChainsSubkeysByLocalAnalytic(
            self) -> typing.Tuple[bool, str]:
        '''
        Calculates chances for the chains (vowels or consonant) by local analytic.
        '''
        answer = "Can't calculate chance of chains by key - "

        if not self.callcRatingOfChainsBySubkey(self.xChains_ChainsSubkey):
            return False, str(answer + self.xChains_ChainsSubkey)

        if not self.callcRatingOfChainsBySubkey(
                self.xChains_ChainFrequencySubkey):
            return False, str(answer + self.xChains_ChainFrequencySubkey)

        return True, None

    def calcChainsDataForAllSubkeysByLocalAnalytic(
            self) -> typing.Tuple[bool, str]:
        '''
        Calculates all chains data for all subkeys by Local AnalyticKey in 
        temporary Names AnalyticDB.
        '''

        if not self.calcChainFrequency():
            answer = "Can't calculate chain frequency."
            return False, answer

        res, answer = self.calcRatingForAllChainsSubkeysByLocalAnalytic()
        if not res:
            return res, answer

        if not self.makeCommonRatingData(self.xChains_ChainFrequencySubkey):
            answer = "Can't calculate chain frequency common data."
            return False, answer

        if not self.prepareDataByChainsAnalyticTemplate(
                self.xChains_LengthCountNamesSubkey):
            answer = "Can't prepare data of the lenght of chain" \
                     + " and their repets count in names."
            return False, answer

        return True, None

    def createChainsDataForAllSubkeysByLocalAnalytic(
            self) -> typing.Tuple[bool, str]:
        '''
        Creates and format chains data by Local AnalyticKey in 
        temporary Names AnalyticDB.
        '''
        answer = "Can't create analytic data for key - "

        if not self.makeLocalAnalyticData(self.getChain,
                                          subKey=self.xChains_ChainsSubkey):
            return False, str(answer + self.xChains_ChainsSubkey)

        if not self.makeLocalAnalyticData(
                self.getChainMaxCountKey,
                subKey=self.xChains_LengthCountNamesSubkey):
            return False, str(answer + self.xChains_LengthCountNamesSubkey)

        return True, None

    def makeVowelsChainsAllData(self) -> str:
        '''
        Makes two  data variables. First - with vowel letters amount in 
        chain and their repeats amount. Second - with themselve vowel 
        chains and their amount.
        '''
        self.localAnalyticKey = self.vowelsChainsKey
        self.alphabet = VOWELS_LETTERS

        res, answer = self.createChainsDataForAllSubkeysByLocalAnalytic()
        if not res:
            return "makeVowelsChainsAllData: Error: " + answer

        res, answer = self.calcChainsDataForAllSubkeysByLocalAnalytic()
        if not res:
            return "makeVowelsChainsAllData: Error: " + answer

        return "makeVowelsChainsAllData: Done"

    def makeConsonantsChainsAllData(self) -> str:
        '''
        Makes two data variables. First - with consonant letters amount in 
        chain and their repeats amount. Second - with themselve consonant 
        chains and their amount.
        '''
        self.localAnalyticKey = self.consonantsChainsKey
        self.alphabet = CONSONANTS_LETTERS

        res, answer = self.createChainsDataForAllSubkeysByLocalAnalytic()
        if not res:
            return "makeConsonantsChainsAllData: Error: " + answer

        res, answer = self.calcChainsDataForAllSubkeysByLocalAnalytic()
        if not res:
            return "makeConsonantsChainsAllData: Error: " + answer

        return "makeConsonantsChainsAllData: Done"


class AnalyticCombinations(AnalyticChains):
    def __init__(self,
                 analysisObj: object,
                 testFile: Union[str, PathType] = None):
        super().__init__(analysisObj, testFile)

        self.copyObjectData(analysisObj)

        #Keys used
        self.chainsCombinationKey = "Chains_Combinations"
        self.ChainsCombinationCounts = list([3, 2])

    def getListChainsData(self, name: str) -> typing.Dict[str, list]:
        '''
        Returns chains data list, which first list includes the first 
        letter of the name.
        '''

        firstLetter = str(name.lower())[0]
        listsData = dict({
            'first': [],
            'second': [],
            'first_len': 0,
            'second_len': 0
        })

        if firstLetter in VOWELS_LETTERS:
            self.alphabet = VOWELS_LETTERS
            listsData['first'] = self.makeChainList(name)
            self.alphabet = CONSONANTS_LETTERS

        else:
            self.alphabet = CONSONANTS_LETTERS
            listsData['first'] = self.makeChainList(name)
            self.alphabet = VOWELS_LETTERS

        listsData['second'] = self.makeChainList(name)

        listsData['first_len'] = len(listsData['first'])
        listsData['second_len'] = len(listsData['second'])

        return dict(listsData)

    def makeAllChainList(self, name: str) -> typing.List[str]:
        ''' 
        Returns a list with all finded chains in the name by order.
        '''
        chainList = []
        listsData = self.getListChainsData(name)

        changesCount = 0
        maxChangesCount = max(listsData['first_len'], listsData['second_len'])

        while changesCount < maxChangesCount:

            if changesCount < listsData['first_len']:
                chainList.append(listsData['first'][changesCount])

            if changesCount < listsData['second_len']:
                chainList.append(listsData['second'][changesCount])

            changesCount += 1

        return chainList

    def makeChainsCombinationsInOrderData(self):
        '''
        Makes data with combinations of two adjacent letters chains, 
        includings one letter chains, and their repeats amount.
        '''
        self.localAnalyticKey = self.chainsCombinationKey

        def tmp_getNameEndingsData(name: str) -> str:
            '''
            '''
            chainList = self.makeAllChainList(name)
            chainsCount = len(chainList)
            ChainsCombinationCounts = self.ChainsCombinationCounts

            for ChainsCombinationCount in ChainsCombinationCounts:

                if ChainsCombinationCount > chainsCount:
                    continue

                changesCount = 0
                while changesCount < (chainsCount - ChainsCombinationCount +
                                      1):

                    usedChains = list()
                    for i in range(ChainsCombinationCount):
                        usedChains.append(chainList[changesCount + i])

                    chainCombination = ''.join(list(usedChains))

                    changesCount += 1
                    yield chainCombination

        if not self.makeLocalAnalyticData(tmp_getNameEndingsData):
            return "makeChainsCombinationsInOrderData: Error: Can't make data"

        return "makeChainsCombinationsInOrderData: Done"


class Analysis(AnalysysService):
    def __init__(self, testFile: Union[str, PathType] = None):
        super().__init__(testFile)

    def makeFunctionsList(self) -> typing.List[typing.Callable]:
        '''
        Makes runable functions list for the filling the temporary variable analytical data.
        '''
        functionsList = list([
            AnalyticLetters(self).makeNameLettersCountData,
            AnalyticLetters(self).makeVowelsCountData,
            AnalyticLetters(self).makeConsonantsCountData,
            AnalyticLetters(self).makeFirstLetterCountData,
            AnalyticLetters(self).makeAllLettersData,
            AnalyticLetters(self).makeNameEndingsData,
            AnalyticChains(self).makeVowelsChainsAllData,
            AnalyticChains(self).makeConsonantsChainsAllData,
            AnalyticCombinations(self).makeChainsCombinationsInOrderData,
        ])

        return functionsList

    def formatRespond(self) -> str:
        '''Formats respond by group key.'''
        respond = "*AnalyticDB* (Group Key: " + self.groupKey
        if self.groupKey == self.GroupKey_Male:
            respond += ") \t\t| "
        else:
            respond += ") \t| "

        return respond

    def initLocalAnalyticDataByGroupKey(self) -> str:
        '''
        Сreates initial data for a temporary analytic data variable by the group key.
        '''
        respond = self.formatRespond()
        respond += self.calcMaxNamesCount()

        return respond

    def makeLocalAnalyticDataByGroupKey(self) -> typing.List[str]:
        '''
        Runs the list of functions that fill the temporary variable analytical data by the group key.
        '''
        responds = list()
        functionsList = self.makeFunctionsList()

        for function in functionsList:
            respond = self.formatRespond()
            respond += function()
            responds.append(respond)

        return responds

    def initLocalAnalyticDB(self, groupKeys: list) -> typing.List[str]:
        '''
        Initializes the analytic data by the current race for the each group key.
        '''
        responds = list()

        for groupKey in groupKeys:
            self.groupKey = groupKey
            responds.append(self.initLocalAnalyticDataByGroupKey())

        return responds

    def makeLocalAnalyticDB(self, groupKeys: list) -> typing.List[str]:
        '''
        Creates the analytic data by the current race for the each group key.
        '''
        responds = list()

        for groupKey in groupKeys:
            self.groupKey = groupKey
            responds.extend(self.makeLocalAnalyticDataByGroupKey())

        return responds

    def formatLocalAnalyticDB(self, groupKeys: list) -> typing.List[str]:
        '''
        Creates the analytic database by the current race (#self.raceNameKey).
        '''
        responds = list()

        responds.extend(self.initLocalAnalyticDB(groupKeys))
        responds.extend(self.makeLocalAnalyticDB(groupKeys))

        return responds

    def extractingNamesByGroupKey(
            self, race: typing.Dict[str, dict]) -> typing.Dict[str, dict]:
        '''
        Extracts a lists of names and saves in temporary database by the gender/surname, 
        and remembers the group key for the all lists.\n
        Returns #groupKeys and #tmp_NamesDB.
        '''

        genders = {"Genders": [self.GroupKey_Male, self.GroupKey_Female]}
        surNamesKey = self.GroupKey_Surnames

        genderKey = self.getFirstUnknownDictKeyName(genders)
        for genderName in genders[genderKey]:
            self.tmp_NamesDB[genderName] = race[
                self.raceNameKey][genderKey][genderName]["Names"]

        self.tmp_NamesDB[surNamesKey] = race[self.raceNameKey][surNamesKey]

        return True

    def fillGlobNamesAnalyticVar(self) -> bool:
        '''
        Fills a global naming analytic database variable with data from a prepared temporary 
        variable holding a list of names for the current race analytic.
        '''

        try:
            analyticKey = self.getFirstUnknownDictKeyName(
                self.globNamesAnalytic)  #Value = 'Analytics'
            self.globNamesAnalytic[analyticKey][
                self.raceNameKey] = self.tmp_NamesAnalytic[self.raceNameKey]
        except:
            return False

        return True

    def makeAnalyticData(self) -> typing.Dict[str, list]:
        '''
        Starts to making names analytic data. Returns list of responds of local making functions.
        '''
        responds = dict()

        for race in self.baseOfNames["Races"]:
            groupKeys = GROUP_KEYS
            self.raceNameKey = self.getFirstUnknownDictKeyName(race)

            self.initNamesAnalytics()
            self.renameDictKey(self.tmp_NamesAnalytic, self.raceNameKey,
                               'tmp_Race')

            if not self.extractingNamesByGroupKey(race):
                return None

            responds[self.raceNameKey] = self.formatLocalAnalyticDB(groupKeys)

            if not self.fillGlobNamesAnalyticVar():
                return None

        return responds

    @redirectOutput
    def printResponds(self, responds: typing.Dict[str, list]) -> bool:
        '''
        Prints the responds list for the each race.
        '''

        if not responds or len(responds.keys()) == 0:
            return False

        for raceNameKey in responds:
            print("\n*AnalyticDB* Race: ", raceNameKey)

            for respond in responds[raceNameKey]:
                print(respond)

        return True

    def makeAnalyticDB(self, testDBFile: Union[str, PathType] = None) -> str:
        '''
        Makes analytic database and write in analytic database file. Returns status.
        '''
        DBFile = ANALYTIC_DB_FILE if not testDBFile else testDBFile

        if not self.baseOfNames or len(self.baseOfNames.keys()) == 0:
            return "\nAnalyticDB: Canceled; Answer: 'Empty initialize database'"

        responds = dict()
        responds = self.makeAnalyticData()
        if not self.printResponds(responds):
            return "\nAnalyticDB: Fault; Answer: 'Error in the process of making local analytic data'"

        flag = FileWork.overwriteDataFile(self.globNamesAnalytic, DBFile)
        if not flag:
            return "\nAnalyticDB: Fault; Answer: 'Data not writed in database'"

        return "\nAnalyticDB: Created"


###FINISH FunctionalBlock


###START MainBlock
def main() -> str:
    analysis: typing.instance = Analysis()
    res: str = analysis.makeAnalyticDB()

    #print(res)
    return res


###FINISH Mainblock
