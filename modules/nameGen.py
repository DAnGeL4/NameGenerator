###START ImportBlock
##systemImport
import random

##customImport
from configs.CFGNames import VOWELS_LETTERS, VOWELS_MAX_COUNT
from configs.CFGNames import CONSONANTS_MAX_COUNT, ALPHABET
###FINISH ImportBlock

###START GlobalConstantBlock
###FINISH GlobalConstantBlock

###START DecoratorBlock
###FINISH DecoratorBlock

###START FunctionalBlock
class ManualNameGen():
    '''
    '''

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
            flag = True         #flag is set to false when a 
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

###FINISH FunctionalBlock

###START MainBlock
def main():
    nameGen = ManualNameGen()
    respond = '\nName Generator: '
    respond += nameGen.createCharacterName()
    
    return respond
###FINISH Mainblock