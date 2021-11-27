###START ImportBlock
##systemImport
import random
import string

##customImport
from configs.CFGNames import VOWELS_LETTERS, VOWELS_MAX_COUNT
from configs.CFGNames import CONSONANTS_MAX_COUNT, ALPHABET
###FINISH ImportBlock

###START GlobalConstantBlock
###FINISH GlobalConstantBlock

###START DecoratorBlock
###FINISH DecoratorBlock

###START FunctionalBlock
def randomNameSize(startRange=5, endRange=7):
    '''
    Возвращает случайное целое число #nameSize в диапазоне от #startRange до #endRange.
    '''

    nameSize = random.randint(startRange, endRange)
    return nameSize


def randomLetter():
    '''
    Возвращает случайную букву нижнего регистра #letter из алфавита ALPHABET.
    '''

    letter = random.choice(ALPHABET)
    return letter


def createCharacterName():
    '''
    Функция "топорной" случайной генерации имени по правилам: не более 2 гласных и 2 согласных подряд.
    '''
    
    nameSize = randomNameSize()
    tmpName = ""
    characterName = ""

    vowelsCount = 0
    consonantsCount = 0
    for letNumber in range(nameSize):
        flag = True         #flag устанавливается в false когда найдена
                            ##буква соответствующая правилам

        while flag:
            tmp_randomLetter = randomLetter()

            #Правило 2 гласных
            if tmp_randomLetter in VOWELS_LETTERS:
                vowelsCount += 1
                consonantsCount = 0
                if vowelsCount >= VOWELS_MAX_COUNT:
                    continue

            #Правило 2 согласных
            else:
                vowelsCount = 0
                consonantsCount += 1
                if consonantsCount >= CONSONANTS_MAX_COUNT:
                    continue

            tmpName += tmp_randomLetter
            flag = False

    characterName = tmpName.capitalize()
    return characterName
###FINISH FunctionalBlock

###START MainBlock
def main():
    respond = '\nName Generator: '
    respond += createCharacterName()
    return respond
###FINISH Mainblock