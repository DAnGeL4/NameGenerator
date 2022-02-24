###START ImportBlock
##systemImport
import sys
import random
import functools
import typing as typ
from contextlib import redirect_stdout

##customImport
from configs.CFGNames import VOWELS_LETTERS, CONSONANTS_LETTERS
from configs.CFGNames import VOWELS_MAX_COUNT, CONSONANTS_MAX_COUNT
from configs.CFGNames import ALPHABET
from configs.CFGNames import LOCAL_GENERATOR_LOG_FILE
from configs.CFGNames import USING_FILE_STORING_FLAG

from database.medbAnalyticSchemas import NameLettersCount, NameEndings
from database.medbAnalyticSchemas import FirstLetters, Letters
from database.medbAnalyticSchemas import VowelsChains, ConsonantsChains
from database.medbAnalyticSchemas import ChainsCombinations

from modules.dbTools import ME_DBService, MECollection
from modules.nameAnalysis import AnalysysService, AnalyticLetters
from modules.nameAnalysis import AnalyticChains, AnalyticCombinations

###FINISH ImportBlock

###START GlobalConstantBlock
###FINISH GlobalConstantBlock


###START DecoratorBlock
def redirectOutput(redirectedFunction: typ.Callable) -> typ.Callable:
    '''
    Redirects output to log file for #redirectedFunction. 
    After returns stdout back.
    '''
    @functools.wraps(redirectedFunction)
    def wrapper(*args, **kwargs):
        logFilePath = LOCAL_GENERATOR_LOG_FILE

        with open(logFilePath, 'w') as f, redirect_stdout(f):
            print("---NAMEGENERATOR-STARTED---\n")
            res = redirectedFunction(*args, **kwargs)
            print("\n---NAMEGENERATOR-FINISHED---")

        return res

    return wrapper


###FINISH DecoratorBlock


###START FunctionalBlock
class ManualNameGen_Stub():
    '''
    A stub for a simple name generator.
    '''

    def __init__(self, seed: int=None):
        '''
        Initial function.
        Seed used for tests.
        '''
        if seed is not None:
            random.seed(seed)
    
    def randomNameSize(self, startRange=5, endRange=7):
        '''
        Returns a random integer #nameSize ranging 
        from #startRange to #endRange.
        '''
        nameSize = random.randint(startRange, endRange)
        return nameSize

    def randomLetter(self):
        '''
        Returns a random lowercase letter #letter 
        from the ALPHABET alphabet.
        '''
        letter = random.choice(ALPHABET)
        return letter

    def createCharacterName(self):
        '''
        The function of 'clumsy' random generation of a name 
        according to the rules: no more than 2 vowels 
        and 2 consonants in a row.
        '''
        nameSize = self.randomNameSize()
        tmpName = ""
        characterName = ""

        vowelsCount = 0
        consonantsCount = 0
        for letNumber in range(nameSize):
            flag = True  #flag is set to false when a
            ##letter matching the rules is found

            while flag:
                tmp_randomLetter = self.randomLetter()

                #Rule of 2 vowels
                if tmp_randomLetter in VOWELS_LETTERS:
                    vowelsCount += 1
                    consonantsCount = 0
                    if vowelsCount >= VOWELS_MAX_COUNT:
                        continue

                #Rule of 2 consonants
                else:
                    vowelsCount = 0
                    consonantsCount += 1
                    if consonantsCount >= CONSONANTS_MAX_COUNT:
                        continue

                tmpName += tmp_randomLetter
                flag = False

        characterName = tmpName.capitalize()
        return characterName


class ManualNameGen():
    '''
    Contains tools for generating names.
    '''

    race = None
    genderGroup = None
    nameLettersCount = NameLettersCount
    nameEndings = NameEndings
    firstLetters = FirstLetters
    letters = Letters
    vowelsChains = VowelsChains
    consonantsChains = ConsonantsChains
    chainsCombinations = ChainsCombinations

    lastLetter = None
    chainTypes = dict({'v': 'vowel', 'c': 'consonant'})

    #Chances params
    globalRandomChance = 1.0

    freeChance = 3.0
    chanceLetterNames = 9.0
    chanceLetterChains = 18.0
    chanceLetterFirst = 70.0

    chanceFreeCombination = 25.0
    chanceCombinationLetter = 75.0

    def __init__(self, seed: int=None):
        '''
        Initial function.
        Seed used for tests.
        '''
        if seed is not None:
            random.seed(seed)

    def modifyChance(self, currChance: float) -> float:
        '''
        Modifies the chance to a free global random chance.
        '''
        allProbability = 100
        modifier = allProbability - self.globalRandomChance
        currChance = (currChance * modifier) / allProbability
        return currChance

    def getFreeRandomChance(self, prewChance: float) -> typ.Dict[str, typ.Any]:
        '''
        Returns range rule for a free global random chance.
        '''
        endRange = prewChance + self.globalRandomChance
        freeRandomChance = {
            'range': tuple((prewChance, endRange)),
            'key': None
        }
        return freeRandomChance

    def prepareEmbeddedData(
            self, embedded: str,
            localAnalyticData: typ.List[dict]) -> typ.List[dict]:
        '''
        Extracts data from embedded field.
        '''
        tmp_data = list()
        for data in localAnalyticData:
            tmp_data.extend(data[embedded])
        return tmp_data

    def setRangeByChances(self, localAnalyticData: typ.List[dict],
                          modify: bool) -> typ.List[dict]:
        '''
        Specifies key ranges by key chances for analytic data.
        '''
        randomChances = list()
        prewChance = 0
        for data in localAnalyticData:
            currChance = data['chance']
            if modify:
                currChance = self.modifyChance(currChance)

            startRange = prewChance
            endRange = startRange + currChance

            randomChances.append({
                'range': tuple((startRange, endRange)),
                'key': data['key']
            })
            prewChance = endRange

        if modify:
            freeRandomChance = self.getFreeRandomChance(prewChance)
            randomChances.append(freeRandomChance)

        return randomChances

    def getDBAnalyticData(self,
                          collection: MECollection,
                          embedded: str = None) -> typ.List[dict]:
        '''
        Returns analytic data from the database by race and gender group keys.
        '''
        localAnalyticData: list = ME_DBService.getLocalAnalyticDataByKeys(
            collection, self.race, self.genderGroup)

        if embedded is not None:
            localAnalyticData = self.prepareEmbeddedData(
                embedded, localAnalyticData)
        return localAnalyticData

    def getRandomByAnalytic(self,
                            collection: MECollection,
                            embedded: str = None,
                            modify: bool = True) -> typ.List[dict]:
        '''
        Returns prepared analytic data from database.
        '''
        localAnalyticData = self.getDBAnalyticData(collection, embedded)

        randomChances = self.setRangeByChances(localAnalyticData, modify)
        return randomChances

    def getRandomChance(self,
                        maxRange: float = 100.0,
                        startRange: float = 0.0) -> float:
        '''
        Returns a random floating point chance within the given range.
        '''
        randomChance = random.uniform(startRange, maxRange)
        return randomChance

    def inRange(self, chance: float, start: float, finish: float) -> bool:
        '''
        Returns true if the chance is in the target range.
        '''
        if start <= chance and chance <= finish:
            return True
        return False

    def getMinMaxSize(self,
                      collection: MECollection,
                      embedded: str = None,
                      modify: bool = True,
                      randomRules: typ.List[dict] = None) -> typ.Tuple[float]:
        '''
        Returns the minimum and maximum key, or key length, 
        with the possibility of random probability.
        '''
        if randomRules is None:
            randomRules = self.getRandomByAnalytic(collection,
                                                   embedded=embedded,
                                                   modify=modify)
        if not randomRules:
            return (0, 0)

        minSize = sys.maxsize
        maxSize = -sys.maxsize - 1
        for data in randomRules:
            if not data['key']:
                continue

            elif type(data['key']) is str:
                minSize = min(minSize, len(data['key']))
                maxSize = max(maxSize, len(data['key']))

            else:
                minSize = min(minSize, data['key'])
                maxSize = max(maxSize, data['key'])

        maxRange = self.getMaxRange(randomRules)
        randomChance = self.getRandomChance(maxRange)
        modifyedMaxChance = self.modifyChance(100)
        if not self.inRange(randomChance, 0.0, modifyedMaxChance):
            maxSize = maxSize * minSize

        return tuple((minSize, maxSize))

    def getMaxRange(self, randomRules: typ.List[dict]) -> float:
        '''
        Returns the max possible range in rules.
        '''
        maxRange = None
        for rule in randomRules:
            _, locRange = rule['range']

            if not maxRange:
                maxRange = locRange
                continue
            maxRange = max(locRange, maxRange)

        return maxRange

    def getRandomKey(
            self,
            collection: MECollection,
            embedded: str = None,
            randomRules: typ.Dict[str, dict] = None) -> typ.Union[int, str]:
        '''
        Gets a random key according to the rules of randomness.
        '''
        if not randomRules:
            randomRules = self.getRandomByAnalytic(collection,
                                                   embedded=embedded)
        maxRange = self.getMaxRange(randomRules)
        randomChance = self.getRandomChance(maxRange)

        randomKey = None
        for rule in randomRules:
            if self.inRange(randomChance, *rule['range']):
                randomKey = rule['key']
                break

        return randomKey

    def getAlphabetByChainType(self, chainType: str) -> str:
        '''
        Returns a string of letters (vowels, consonants, or all) by chain type.
        '''
        abc = ALPHABET
        if chainType == self.chainTypes['v']:
            abc = VOWELS_LETTERS
        elif chainType == self.chainTypes['c']:
            abc = CONSONANTS_LETTERS
        return abc

    def getRandomLetter(self, chainType: str = None) -> str:
        '''
        Returns a random letter from the alphabet by chain type.
        '''
        abc = self.getAlphabetByChainType(chainType)
        letter = random.choice(abc)
        return letter

    def getNameSize(self) -> int:
        '''
        Returns a random name length according to analytics 
        with the probability of another random name length.
        '''
        self.globalRandomChance = 1.0
        nameSize = self.getRandomKey(self.nameLettersCount)
        if not nameSize:
            minSize, maxSize = self.getMinMaxSize(self.nameLettersCount)
            if minSize > maxSize:
                minSize = 0
                maxSize = 30
                
            nameSize = random.randint(minSize, maxSize)

        return nameSize

    def getEndSizeChances(self,
                          nameEndings: typ.List[dict]) -> typ.Dict[int, float]:
        '''
        Returns the chances of the length of the endings.
        '''
        endingChances = dict()
        for ending in nameEndings:
            key = len(ending['key'])
            chance = ending['chance']
            if key in endingChances:
                chance += endingChances[key]

            endingChances.update({key: chance})

        return endingChances

    def convertDictToListRules(self,
                               endingChances: typ.Dict[str, dict],
                               preparing: bool = True) -> typ.List[dict]:
        '''
        Converts a rules dictionary to a list of dictionaries.
        '''
        endingRules = list()
        for key, chance in endingChances.items():
            endingRules.append({'key': key, 'chance': chance})
        if preparing:
            endingRules = self.setRangeByChances(endingRules, False)
        return endingRules

    def getNameEndSize(self) -> int:
        '''
        Returns the length of the end of the name by the analytic.
        '''
        self.globalRandomChance = 1.0

        nameEndings = self.getDBAnalyticData(self.nameEndings)
        endingChances = self.getEndSizeChances(nameEndings)
        endingRules = self.convertDictToListRules(endingChances)
        nameEndSize = self.getRandomKey(None, randomRules=endingRules)
        
        if nameEndSize is None:
            nameEndSize = random.randint(0, 21)

        return nameEndSize

    def getNameFirstLetter(self) -> str:
        '''
        Gets a random first letter from the analytic 
        with a probability of any letter.
        '''
        self.globalRandomChance = 10.0
        letter = self.getRandomKey(self.firstLetters)
        if not letter:
            letter = self.getRandomLetter()
            letter = letter.capitalize()

        return letter

    def getLetterType(self, letter: str) -> str:
        '''
        Returns type (vowel or consonant) for target letter.
        '''
        typeChain = self.chainTypes['c']
        if letter in VOWELS_LETTERS:
            typeChain = self.chainTypes['v']
        return typeChain

    def getNextLetterType(self, currentType: str) -> str:
        '''
        Returns the next letter type (vowel or consonant) given the current type.
        '''
        nextType = self.chainTypes['v']
        if currentType == self.chainTypes['v']:
            nextType = self.chainTypes['c']
        return nextType

    def getCollectionByType(
            self,
            chainType: str,
            embeddedType: str = 'chains') -> typ.Union[MECollection, str]:
        '''
        Returns a Mongoengine collection by chain type and embedded type.
        '''
        assert chainType in self.chainTypes.values(),\
                "ERR: Unknown chain type."
                
        collectionsByTypes = dict({
            self.chainTypes['v']: {
                'type': self.vowelsChains,
                'embedded': embeddedType
            },
            self.chainTypes['c']: {
                'type': self.consonantsChains,
                'embedded': embeddedType
            }
        })

        collection = collectionsByTypes[chainType]['type']
        embedded = collectionsByTypes[chainType]['embedded']
        return collection, embedded

    def makeFrequencyData(self) -> typ.Dict[str, list]:
        '''
        Returns the chain frequency, ordered by chain type.
        '''
        frequencyData = dict()
        types = list([self.chainTypes['v'], self.chainTypes['c']])

        for chainType in types:
            collection, embedded = self.getCollectionByType(
                chainType, embeddedType='chainFrequency')
            chainsFrequency = self.getDBAnalyticData(collection,
                                                     embedded=embedded)
            frequencyData.update({chainType: chainsFrequency})

        return frequencyData

    def makeRangesByTypes(
            self, frequencyData: typ.Dict[str, list]) -> typ.Dict[str, tuple]:
        '''
        Returns the chain ranges, ordered by chain type.
        '''
        rangeByTypes = dict()
        types = list([self.chainTypes['v'], self.chainTypes['c']])

        for chainType in types:
            frequencyRules = self.setRangeByChances(frequencyData[chainType],
                                                    False)
            chainRange = self.getMinMaxSize(None, randomRules=frequencyRules)
            rangeByTypes.update({chainType: chainRange})

        return rangeByTypes

    def prepareFrequencyData(self, minMaxRange: tuple,
                             frequencyData: typ.List[dict]) -> typ.List[dict]:
        '''
        Leaves only those rules whose keys match the range.
        '''
        minSize, maxSize = minMaxRange

        preparedData = list()
        for rule in frequencyData:
            if self.inRange(rule['key'], minSize, maxSize):
                preparedData.append(rule)

        return preparedData

    def getChainSize(self, croppedSize: int, minMaxRange: tuple,
                     frequencyData: typ.List[dict]) -> int:
        '''
        Returns a random chain size by analytics.
        '''
        minSize, maxSize = minMaxRange

        if maxSize > croppedSize:
            maxSize = croppedSize

        if minSize >= croppedSize:
            chainSize = croppedSize
        else:
            minMaxRange = tuple((minSize, maxSize))
            preparedData = self.prepareFrequencyData(minMaxRange,
                                                     frequencyData)
            frequencyRules = self.setRangeByChances(preparedData, False)
            chainSize = self.getRandomKey(None, randomRules=frequencyRules)

        return chainSize

    def makeChainsOrder(self, croppedSize: int) -> typ.List[int]:
        '''
        Returns the order of chains by type and length.
        '''
        if not croppedSize: 
            return []
            
        chainType = self.getLetterType(self.lastLetter)
        frequencyData = self.makeFrequencyData()
        rangeByTypes = self.makeRangesByTypes(frequencyData)

        chainsOrder = list()
        while True:
            chainSize = self.getChainSize(croppedSize, 
                                          rangeByTypes[chainType],
                                          frequencyData[chainType])
            chainsOrder.append(chainSize)

            croppedSize = croppedSize - chainSize
            if croppedSize == 0:
                break
            assert croppedSize >= 0, "ERR: Out of range cropped size." #>0

            chainType = self.getNextLetterType(chainType)

        return chainsOrder

    def getChainsData(self, chainType: str) -> typ.List[dict]:
        '''
        Returns chains data from database by chain type.
        '''
        collection, embedded = self.getCollectionByType(chainType)
        chainData = self.getDBAnalyticData(collection, embedded=embedded)
        return chainData

    def getChainsList(self,
                      chainType: str,
                      chainRules: typ.List[dict] = None) -> typ.List[str]:
        '''
        Returns a list of chains from chain rules.
        '''
        if chainRules is None:
            chainRules = self.getChainsData(chainType)

        chainsData = list()
        for chain in chainRules:
            chainsData.append(chain['key'])
        return chainsData

    def prepareLettersAnalytic(self, chainList: typ.List[str]) -> object:
        '''
        Prepares initial data for an analytic object.
        '''
        NamesAnalyticData = {
            'tmp_Race': {
                'Max_Names_Count': len(chainList),
                'First_Letters': {
                    'Vowels_Count': 0,
                    'Consonants_Count': 0,
                },
                "Letters": dict({})
            }
        }

        analysisObj = AnalysysService(baseOfNames=dict())
        analysisObj = AnalyticLetters(analysisObj, baseOfNames=dict())
        analysisObj.tmp_NamesAnalytic = NamesAnalyticData
        analysisObj.tmp_NamesDB['Common'] = chainList
        analysisObj.raceNameKey = 'tmp_Race'
        analysisObj.groupKey = 'Common'

        return analysisObj

    def getCombinationsAnalyticObject(self) -> object:
        '''
        Returns an initialized combination analytics object.
        '''
        analysisObj = AnalysysService(baseOfNames=dict())
        analysisObj = AnalyticCombinations(analysisObj, baseOfNames=dict())

        return analysisObj

    def getChainsAnalyticObject(self) -> object:
        '''
        Returns an initialized chains analytics object.
        '''
        analysisObj = AnalysysService(baseOfNames=dict())
        analysisObj = AnalyticChains(analysisObj, baseOfNames=dict())

        return analysisObj

    def makeAllChainLettersData(self,
                                chainList: typ.List[str]) -> typ.List[dict]:
        '''
        Makes rules by the chances of all letters in chains from the data.
        '''
        analysisObj = self.prepareLettersAnalytic(chainList)
        _ = analysisObj.makeAllLettersData()
        analytic = analysisObj.tmp_NamesAnalytic['tmp_Race']

        lettersAnalytic = ME_DBService.fillAnalyticCountCollection(
            'tmp_Race', analytic, 'Letters')

        randomChances = self.setRangeByChances(lettersAnalytic, False)
        return randomChances

    def makeAllNamesLetters(self, chainType: str) -> typ.List[dict]:
        '''
        Makes rules by the chances of all letters 
        in the database of names for given type.
        '''
        localAnalyticData: list = ME_DBService.getLocalAnalyticDataByKeys(
            self.letters, self.race, self.genderGroup)

        sortedData = list()
        alphabet = self.getAlphabetByChainType(chainType)
        for data in localAnalyticData:
            if data['key'] in alphabet:
                sortedData.append(data)

        lettersRules = self.setRangeByChances(sortedData, modify=False)
        return lettersRules

    def getGivenLengthChains(self, chainsData: typ.List[dict],
                             lenChain: int) -> typ.List[dict]:
        '''
        Returns a list of chains of the given length.
        '''
        assert lenChain is not None, "ERR: lenChain must be initialized."
        assert lenChain >= 0, "ERR: lenChain must be positive."
                                 
        preparedData = list()
        for chain in chainsData:
            if len(chain['key']) == lenChain:
                preparedData.append(chain)

        return preparedData

    def prepareFirstChainLetters(self,
                                 chainsData: typ.List[dict]) -> typ.List[dict]:
        '''
        Gets the first letters in chains from rules.
        '''
        preparedData = list(chainsData)
        for chain in preparedData:
            key = chain['key'][0]
            chain['key'] = key

        return preparedData

    def cutChains(self, chainsData: typ.List[dict],
                  prewLetter: str) -> typ.List[dict]:
        '''
        Selects chains starting with the received letter 
        and discards this letter from each chain.
        '''
        assert prewLetter is not None, "ERR: letter cannot be None."
                      
        preparedData = list()
        for chain in chainsData:
            key = chain['key']
            letter = key[0]
            if prewLetter == letter:
                chain['key'] = key[1:]
                if not chain['key']:
                    continue
                preparedData.append(chain)

        return preparedData

    def prepareLettersRules(
            self, rulesData: typ.Dict[str, list]) -> typ.List[dict]:
        '''
        Prepares rules by type for:
        probable next letter in the chain;
        any of the possible letters in the chain;
        any of the possible letters in the name;
        any random letter.
        '''
        assert all(key in rulesData for key in ['fcl', 'acl', 'anl']),\
                "ERR: There is no one of the keys."
                
        chanceLetterFirst = self.chanceLetterFirst
        if not rulesData['fcl']:
            chanceLetterFirst = 0.0

        dataList = list()
        dataList.append((chanceLetterFirst, rulesData['fcl']))
        dataList.append((self.chanceLetterChains, rulesData['acl']))
        dataList.append((self.chanceLetterNames, rulesData['anl']))
        dataList.append((self.freeChance, None))

        return dataList

    def makeLetterRules(self, chainType: str,
                        dataList: typ.List[tuple]) -> typ.List[dict]:
        '''
        Makes rules for several letter variants, 
        chosen randomly according to their rules.
        '''
        startChance = 0
        randomRules = list()
        for data in dataList:
            chance = data[0]

            if not data[1]:
                key = self.getRandomLetter(chainType)
            else:
                key = self.getRandomKey(None, randomRules=data[1])

            endChance = startChance + chance
            randomRules.append({
                'range': tuple((startChance, endChance)),
                'key': key
            })

            startChance = endChance

        return randomRules

    def getLettersRules(self, chainType: str,
                        rulesData: typ.Dict[str, list]) -> typ.List[dict]:
        '''
        Prepares and makes rules for several variants of letters.
        '''
        dataList = self.prepareLettersRules(rulesData)
        randomRules = self.makeLetterRules(chainType, dataList)

        return randomRules

    def cutChance(self, currLetter: str,
                  letterRules: typ.List[dict]) -> typ.List[dict]:
        '''
        Reduces the chance of dropping an already 
        dropped letter and recalculates the ranges.
        '''
        coefficient = 0.01
        prewRange = None

        for rule in letterRules:
            startRange, endRange = rule['range']
            commonRange = endRange - startRange

            if not prewRange:
                prewRange = startRange

            if rule['key'] == currLetter:
                if commonRange > 100:
                    commonRange -= 100
                else:
                    commonRange *= coefficient

            endRange = prewRange + commonRange
            rule['range'] = tuple((prewRange, endRange))
            prewRange = endRange

        return letterRules

    def createChain(self, lenChain: int, chainType: str,
                    chainsRules: typ.List[dict]) -> str:
        '''
        Creates a chain of the given type according to the rules used.
        Used rules:
        the first letter of the possible next chain;
        chances of all letters in chains of a given type;
        the chances of all letters in the database of names for given type;
        free random chance for any letter of the given type.
        '''
        self.globalRandomChance = 0.0
        generalChain = ''

        if not chainsRules:
            chainsRules = self.getChainsData(chainType)
        chainsList = self.getChainsList(chainType, chainsRules)

        allChainLetters = self.makeAllChainLettersData(chainsList)
        allNamesLetters = self.makeAllNamesLetters(chainType)

        chainsRules = self.getGivenLengthChains(chainsRules, lenChain)
        if self.lastLetter:
            lenChain -= 1
            chainsRules = self.cutChains(chainsRules, self.lastLetter)

            generalChain += self.lastLetter
            self.lastLetter = None

        count = 0
        while count < lenChain:
            firstLettersRules = self.prepareFirstChainLetters(chainsRules)
            firstChainLetters = self.setRangeByChances(firstLettersRules,
                                                       False)

            preRulesData = dict()
            preRulesData.update({'fcl': firstChainLetters})
            preRulesData.update({'acl': allChainLetters})
            preRulesData.update({'anl': allNamesLetters})

            randomRules = self.getLettersRules(chainType, preRulesData)
            letter = self.getRandomKey(None, randomRules=randomRules)
            generalChain += letter

            chainsRules = self.cutChains(chainsRules, letter)
            allChainLetters = self.cutChance(letter, allChainLetters)
            allNamesLetters = self.cutChance(letter, allNamesLetters)
            count += 1

        return generalChain

    def findValidCombinations(
            self, lastChain: str, analysisObj: object,
            combinationsData: typ.List[dict]) -> typ.List[dict]:
        '''
        Finds valid combinations for the previous chain 
        and discards the previous chain from the combinations.
        Returns prepared combinations data.
        '''
        preparedData = list()

        for data in combinationsData:
            if lastChain not in data['key']:
                continue

            chains = analysisObj.getListChainsData(data['key'])

            if chains['first'][0] != lastChain:
                continue

            lastChainLen = len(lastChain)
            data['key'] = data['key'][lastChainLen:]
            if not data['key']:
                continue

            preparedData.append(data)

        return preparedData

    def createCombinationChances(
            self, analysisObj: object,
            combinationsData: typ.List[dict]) -> typ.List[dict]:
        '''
        Creates the chances data for the next letter in chains combinations.
        '''
        letterChances = dict()

        for data in combinationsData:
            chains = analysisObj.getListChainsData(data['key'])
            nextChain = chains['first'][0]
            nextLetter = nextChain[0]

            chance = data['chance']
            if nextLetter in letterChances.keys():
                chance += letterChances[nextLetter]

            letterChances.update({nextLetter: chance})

        combinationRules = self.convertDictToListRules(letterChances)
        return combinationRules

    def setCombinationLetter(self, lastChain: str, analysisObj: object,
                             combinationsData: typ.List[dict]) -> typ.NoReturn:
        '''
        Finds possible combinations for the previous chain 
        and randomly selects the first letter from those chains.
        '''
        combinationsData = self.findValidCombinations(lastChain, analysisObj,
                                                      combinationsData)

        freeLetterRule = dict({'range': tuple((0, 1)), 'key': None})
        combinationRules = self.createCombinationChances(
            analysisObj, combinationsData)
        chanceCombinationLetter = self.chanceCombinationLetter
        if not combinationRules:
            chanceCombinationLetter = 0

        dataList = list()
        dataList.append((chanceCombinationLetter, combinationRules))
        dataList.append((self.chanceFreeCombination, list([freeLetterRule])))

        randomRules = self.makeLetterRules(None, dataList)
        letter = self.getRandomKey(None, randomRules=randomRules)

        self.lastLetter = letter
        return

    def createNamePart(self,
                       chainsOrder: typ.List[int],
                       chainRules: typ.List[dict] = None,
                       end: bool = False) -> str:
        '''
        Creates the part of name by the analytic.
        Used analytics: chains combinations, chains,
        first letters, letters e.t.c.
        '''
        orderedChains = list()
        chainType = self.getLetterType(self.lastLetter)
        if end:
            self.lastLetter = None
            chainType = self.getNextLetterType(chainType)

        combinationsData = self.getDBAnalyticData(self.chainsCombinations)
        analysisObj = self.getCombinationsAnalyticObject()

        chain = None
        for lenChain in chainsOrder:
            if chain:
                _ = self.setCombinationLetter(chain, analysisObj,
                                              combinationsData)

            rules = None if not chainRules else chainRules[chainType]
            chain = self.createChain(lenChain, chainType, rules)
            chainType = self.getNextLetterType(chainType)
            orderedChains.append(chain)

        namePart = ''.join(orderedChains)
        return namePart

    def makeEndingChainsRules(self) -> typ.Dict[str, list]:
        '''
        Makes rules for name endings from the 
        database analytics for name endings.
        '''
        rulesByTypes = dict()
        endingsData = self.getDBAnalyticData(self.nameEndings)
        analysisObj = self.getChainsAnalyticObject()

        types = list([self.chainTypes['v'], self.chainTypes['c']])
        for chainType in types:
            endingChains = dict()

            for ending in endingsData:
                analysisObj.alphabet = self.getAlphabetByChainType(chainType)
                chainList = analysisObj.makeChainList(ending['key'])

                for chain in chainList:
                    chance = ending['chance']
                    if chain in endingChains.keys():
                        chance += endingChains[chain]

                    endingChains.update({chain: chance})

            endingRules = self.convertDictToListRules(endingChains,
                                                      preparing=False)
            rulesByTypes.update({chainType: endingRules})

        return rulesByTypes

    def printLogLine(self, msg: str, param: typ.Any, lvl: int) -> typ.NoReturn:
        '''
        Prints message to log file.
        '''
        filler = "*" * lvl
        ident = "" if lvl == 0 else " "
        completion = "..." if lvl == 0 else ": "

        logStr = "" + filler + ident
        logStr += msg + completion + str(param)

        print(logStr)
        return

    def createCharacterName(self, race: str, genderGroup: str) -> str:
        '''
        Creates character name by analytic.
        Gets from analytic:
        size of name, size of ending name,
        first letter, chains data, letters data,
        combination of chains data.
        '''
        self.race = race
        self.genderGroup = genderGroup
        self.lastLetter = str(self.getNameFirstLetter()).lower()

        nameSize = self.getNameSize()
        nameEndSize = self.getNameEndSize()
        if nameEndSize >= nameSize:
            nameSize = nameEndSize + 1

        self.printLogLine('New generate', '', 0)
        self.printLogLine('Race name', race, 1)
        self.printLogLine('Gender group', genderGroup, 1)
        self.printLogLine('Generation parameters', '', 1)
        self.printLogLine('Name size', nameSize, 2)
        self.printLogLine('Name end size', nameEndSize, 2)
        self.printLogLine('First letter', self.lastLetter, 2)

        croppedSize = nameSize - nameEndSize
        self.printLogLine('Cropped size', croppedSize, 2)
        chainsOrder = self.makeChainsOrder(croppedSize)

        self.printLogLine('Chains order', chainsOrder, 2)

        characterName = ''
        namePart = self.createNamePart(chainsOrder)
        characterName += namePart

        self.printLogLine('Character name part', characterName, 2)

        self.lastLetter = characterName[-1]
        chainsOrder = self.makeChainsOrder(nameEndSize)

        self.printLogLine('Chains order for ending', chainsOrder, 2)

        endingRules = self.makeEndingChainsRules()
        nameEnding = self.createNamePart(chainsOrder,
                                         chainRules=endingRules,
                                         end=True)

        self.printLogLine('Name ending part', nameEnding, 2)

        characterName += nameEnding
        characterName = characterName.capitalize()

        self.printLogLine('Full character name', characterName, 2)
        self.printLogLine('End generate', '', 0)
        self.printLogLine('', '', 0)

        return characterName


###FINISH FunctionalBlock


###START MainBlock
@redirectOutput
def main():
    respond = '\nName Generator: '
    
    if USING_FILE_STORING_FLAG:
        nameGen = ManualNameGen_Stub()
        respond += '\n* Stub name: '
        respond += nameGen.createCharacterName()
    else:
        nameGen = ManualNameGen()
        race = 'Elf'
        respond += '\n* Race: %s' % race

        loc_resp = '\n* New %s: '
        gender_groups = ['Male', 'Female', 'Surnames']
        for gender in gender_groups:
            respond += loc_resp % gender
            respond += nameGen.createCharacterName(race, gender)

    print(respond)
    return respond


###FINISH Mainblock
