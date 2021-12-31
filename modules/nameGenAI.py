#--------------------------------------------------------#
#|  For Google colaboratory                             |#
#|  Not work on Replit                                  |#
#|   (used too old version of tensorflow for python)    |#
#--------------------------------------------------------#

###START ImportBlock
##systemImport
import numpy
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint

##customImport

###FINISH ImportBlock

###START GlobalConstantBlock
###FINISH GlobalConstantBlock

###START DecoratorBlock
###FINISH DecoratorBlock

###START FunctionalBlock
class NameGenAI():

    dbNames = [
            'DBNames/DBNames_Elf_Male',
            'DBNames/DBNames_Elf_Female',
            'DBNames/DBNames_Elf_Surnames',]
    checkpointFile = "DBNames/saved_models/" + \
                     "weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
    
    model = None

    sequenceLength = 0
    inData = list()
    outData = list()    
    usedChars = list()

    def __init__(self, model=None, sequenceLength=100):
        '''
        '''
        nltk.download('stopwords')

        self.sequenceLength = sequenceLength

        if model:
            self.model = model
    
    def tokenizeWords(self, input):
        '''
        '''
        input = input.lower()

        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(input)

        
        filtered = filter(lambda token: 
                          token not in stopwords.words('english'), 
                          tokens)
        
        return " ".join(filtered)

    def getProcessedInputs(self):
        '''
        '''
        data = open(self.dbNames[0]).read()
        processedInputs = self.tokenizeWords(data)
    
        return processedInputs

    def initializeModel(self, preparedInData, preparedOutData):
        '''
        '''
        self.model = Sequential()
        self.model.add(LSTM(256, input_shape=(preparedInData.shape[1], 
                                              preparedInData.shape[2]), 
                            return_sequences=True))
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(256, return_sequences=True))
        self.model.add(Dropout(0.2))
        self.model.add(LSTM(128))
        self.model.add(Dropout(0.2))
        self.model.add(Dense(preparedOutData.shape[1], activation='softmax'))

    def prepareModel(self):
        '''
        '''
        print("* Preparing model...")
        processedInputs = self.getProcessedInputs()
        self.usedChars = sorted(list(set(processedInputs)))

        _ = self.preparePatterns(processedInputs)
        preparedInData = self.prepareInputData()
        preparedOutData = self.prepareOutputData()

        _ = self.initializeModel(preparedInData, preparedOutData)

        print("* ...done.")
        return preparedInData, preparedOutData

    def compileModel(self):
        '''
        '''
        print("* Compiling model...")
        self.model.compile(loss='categorical_crossentropy', optimizer='adam')
        print("* ...done.")

    def preparePatterns(self, processedInputs):
        '''
        '''
        lenInputChars = len(processedInputs)
        #lenVocab = len(self.usedChars)
        charsToNum = dict((char, iter) for iter, char in enumerate(self.usedChars))

        #print("Total number of characters:", lenInputChars)
        #print("Total vocab:", lenVocab)

        self.inData = list()
        self.outData = list()
        for i in range(0, lenInputChars - self.sequenceLength, 1):
            in_seq = processedInputs[i:i + self.sequenceLength]
            out_seq = processedInputs[i + self.sequenceLength]

            self.inData.append([charsToNum[char] for char in in_seq])
            self.outData.append(charsToNum[out_seq])

        #patternsCount = len(self.inData)
        #print("Total Patterns:", patternsCount)

    def prepareInputData(self, pattern=None):
        '''
        '''
        patternsCount = len(self.inData)
        lenVocab = len(self.usedChars)

        if pattern:
            preparedInData = numpy.reshape(pattern, 
                                           (1, len(pattern), 1))
            preparedInData = preparedInData / float(lenVocab)

        else:
            preparedInData = numpy.reshape(self.inData, 
                                           (patternsCount, self.sequenceLength, 1))
            preparedInData = preparedInData / float(lenVocab)

        return preparedInData

        
        preparedInData = numpy.reshape(pattern, (1, len(pattern), 1))
        preparedInData = preparedInData / float(lenVocab)
    
    def prepareOutputData(self):
        '''
        '''
        return np_utils.to_categorical(self.outData)

    def getStartPattern(self):
        '''
        '''
        start = numpy.random.randint(0, len(self.inData) - 1)
        startPattern = self.inData[start]

        return startPattern

    def generateChars(self, pattern, length, numsToChar):
        '''
        '''
        print("* Start generation chars...")
        resultStr = ''
        for i in range(length):
            preparedInData = self.prepareInputData(pattern)

            prediction = self.model.predict(preparedInData, verbose=0)
            index = numpy.argmax(prediction)
            result = numsToChar[index]

            #if result == ' ': break
            resultStr += str(result)

            pattern.append(index)
            pattern = pattern[1:len(pattern)]
        
        print("* ...done.")
        return resultStr

    def train(self, epochsCount=300):
        '''
        
        '''
        print("Start training...\n")
        preparedInData, preparedOutData = self.prepareModel()
        _ = self.compileModel()

        checkpoint = ModelCheckpoint(self.checkpointFile, 
                                     monitor='loss', 
                                     verbose=1, 
                                     save_best_only=True, 
                                     mode='min')
        callbackList = list([checkpoint])

        print("* Start fiting...")
        self.model.fit(preparedInData, 
                       preparedOutData, 
                       epochs=epochsCount, 
                       batch_size=256, 
                       callbacks=callbackList)
        print("* ...done.")
        print("\n...Finish training.\n")

    def generate(self, fileName=None, length=1000):
        '''
        '''
        print("Start generating...\n")

        if not self.model:
            _ = self.prepareModel()
            _ = self.compileModel()
            
            if not fileName:
                fileName = self.checkpointFile
            else:
                fileName = fileName

            print("* Load weights.")
            self.model.load_weights(fileName)
            print("* ...done.")
            _ = self.compileModel()

        numsToChar = dict((iter, char) for iter, char in enumerate(self.usedChars))
        pattern = self.getStartPattern()

        #randSeed = ''.join([numsToChar[value] for value in pattern])
        #print('Random Seed:\n "%s"' % randSeed)

        resultStr = self.generateChars(pattern, length, numsToChar)

        print("\n...Finish generation.\n")

        return resultStr
                                                                               #| 80 
###FINISH FunctionalBlock

###START MainBlock
def main():
    nameGenAI = NameGenAI()#sequenceLength=20)
    respond = '\nName Generator AI: '
    #_ = nameGenAI.train(epochsCount=300)
    nameGenAI.model = None

    filePath='DBNames/saved_models/'
    fileName = 'weights-improvement-255-0.0397.hdf5'
    fullFileName = filePath + fileName

    names = list()
    generationCount = 10
    for count in range(generationCount):
        print("\n$ Count of generation: %s.\n" % (count + 1))
        
        genNames = nameGenAI.generate(fileName=fullFileName)
        editedNames = genNames.split(' ')
        _ = editedNames.pop(0)
        _ = editedNames.pop(-1)
        
        names.extend(editedNames)

    print("################")
    print("Generated names: \n%s" % names)
    
    respond += "\nGenerated names: \n" + names
    return respond
###FINISH Mainblock