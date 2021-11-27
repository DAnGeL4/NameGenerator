###START ImportBlock
##systemImport
import os
import typing
#import pymongo as pymdb
import mongoengine as medb

##customImport
from configs.CFGNames import ME_SETTINGS

from database.medbNameSchemas import Race, Female, Male, Surname

from database.medbAnalyticSchemas import GlobalCounts, NameLettersCount
from database.medbAnalyticSchemas import VowelsCount, ConsonantsCount
from database.medbAnalyticSchemas import FirstLetters, Letters
from database.medbAnalyticSchemas import ChainsCombinations, NameEndings
from database.medbAnalyticSchemas import VowelsChains, ConsonantsChains

from database.medbCheckSumSchemas import GlobalFlags, ChecksumFiles
###FINISH ImportBlock

###START GlobalConstantBlock
###FINISH GlobalConstantBlock

###START DecoratorBlock
###FINISH DecoratorBlock

###START FunctionalBlock

class MongoDBWork:
    '''
    A class containing tools for working with MongoDB using mongoEngine.
    '''
    @classmethod
    def eraseNamesME_DB(cls):
        '''
        
        '''
        mdbNAliases = ME_SETTINGS.MDB_n_Aliases
        mdbNameAlias = mdbNAliases['mdbName']['alias']

        mdbName = medb.get_db(mdbNameAlias)
        listCollections = mdbName.list_collection_names()
        
        for collectionName in listCollections:
            mdbName.drop_collection(collectionName)
            mdbName.create_collection(collectionName)

    @classmethod
    def getReferenceID(cls, collectionField, data):
        '''
        
        '''
        field = collectionField.db_field
        referenceCollection = collectionField.document_type_obj
        referenceDocument = referenceCollection.objects.get(
                                    __raw__={field: data[field]})
        return referenceDocument.id

    @classmethod
    def insertData(cls, collection, data) -> bool:
        '''

        '''
        document = collection()
        referenceFields = tuple( (medb.GenericReferenceField, 
                                medb.LazyReferenceField, 
                                medb.ReferenceField) )
        fieldContainedCollections = tuple( (medb.DynamicField,
                                    medb.EmbeddedDocumentField,
                                    medb.GenericEmbeddedDocumentField) )
                                    
        for field in data.keys():

            if hasattr(collection, field):
                collectionField = getattr(collection, field, None)
                
                if isinstance(collectionField, referenceFields): 
                    document[field] = cls.getReferenceID(collectionField, data)
                    continue

                elif isinstance(collectionField, fieldContainedCollections):

                    if type(data[field]) is dict:
                        cls.insertData(collection[field], data[field])
                    continue
                    
                else:
                    document[field] = data[field]
                
        return document

    @classmethod
    def insertDocument(cls, collection, data):
        '''
        
        '''        
        document = cls.insertData(collection, data)

        answer = None
        try:
            document.save()
            
        except medb.NotUniqueError as err:
            answer = err

        return answer

    @classmethod
    def insertDocuments(cls, collection, listOfData):
        '''
        
        '''
        answers = list()
        for data in listOfData:
            answer = cls.insertDocument(collection, data)

            if answer:
                answers.append(answer)
        
        if not answers:
            answers = None
        return answers

    @classmethod
    def insertDatabase(cls, collectionsData):
        '''
        
        '''
        for collectionName in collectionsData.keys():
            collection = collectionsData[collectionName]['collection']
            listOfData = collectionsData[collectionName]['data']
            answers = cls.insertDocuments(collection, listOfData)

        return answers

    @classmethod
    def printCollection(cls, collection) -> list:
        '''
        Custom print on demand for collection fields.
        '''
        print("\n #MEDATA_module.1 {0} len: {1}".format(collection._class_name, 
                                                len(collection.objects)))
        for obj in collection.objects:
            printString = ""#\n  ##MEDATA_module.1.1 \n"

            for field in obj._fields:
                printString += "   *" + str(field) + ": " + str(obj[field]) + "\n"

            print(printString)
        
        return None


class ME_DBService():
    '''
    Contains tools for working with mongoengine and mongodb.
    '''
    mdbUser = ME_SETTINGS.mdbUser
    mdbPass = ME_SETTINGS.mdbPass
    mdbCluster = ME_SETTINGS.mdbCluster
    mdbNAliases = ME_SETTINGS.MDB_n_Aliases

    def getConnectString(self, mdb):
        '''
        Makes connection string for mongodb.
        '''
        connectString = "mongodb+srv://" + self.mdbUser + ":" + self.mdbPass + \
                        "@" + self.mdbCluster + ".9wwxd.mongodb.net/" + \
                        mdb + "?retryWrites=true&w=majority"

        return connectString

    def getConnect(self, mdb, mdb_alias):
        '''
        Connects to database and sets the alias.
        '''
        connectString = self.getConnectString(mdb)
        client = medb.connect(host=connectString, alias=mdb_alias)
        return client

    def registerDataBases(self):
        '''
        Connects to all databases by dictionary.
        '''
        clients = dict({})
        for database in self.mdbNAliases:
            db = self.mdbNAliases[database]['db_name']
            alias = self.mdbNAliases[database]['alias']
            client = self.getConnect(db, alias)
            clients.update({alias: client})

        return clients

    
    def prepareNamesData(self, race: str, data: list) -> dict:
        '''
        
        '''
        collectionData = list({})
        for name in data:
            collectionData.append({
                'name': str(name),
                'race': str(race)})
        
        return collectionData

    def insertNames(self, namesDict):
        '''
        
        '''
        answers = list([])
        racesData = list({})
        malesData = list({})
        femalesData = list({})
        surnamesData = list({})

        for race in namesDict['Races']:
            raceName = str(next(iter(race)))
            maleNames =  race[raceName]['Genders']['Male']['Names']
            femaleNames =  race[raceName]['Genders']['Female']['Names']
            surnames = race[raceName]['Surnames']

            racesData.append({'race': raceName})
            malesData = self.prepareNamesData(raceName, maleNames)
            femalesData = self.prepareNamesData(raceName, femaleNames)
            surnamesData = self.prepareNamesData(raceName, surnames)

            collectionsData = dict({
                'Race': {
                    'collection': Race,
                    'data': racesData},
                'Male':{
                    'collection': Male,
                    'data': malesData}, 
                'Female':{
                    'collection': Female,
                    'data': femalesData}, 
                'Surname':{
                    'collection': Surname,
                    'data': surnamesData},
                    })

            answer = MongoDBWork.insertDatabase(collectionsData)
            if answer:
                answers.append(answer)

        if not answers:
            answers = "Names inserted in mongoDB."
        return answers

    def printDatabases(self, modelsByAliases):
        '''
        Custom data printing for database.
        '''
        for alias in modelsByAliases.keys():
            print("\nMEDATA.x DB %s" % alias)

            models = modelsByAliases[alias]
            for model in models:
                MongoDBWork.printCollection(model)

    def showDBData(self) -> typing.NoReturn:
        '''
        Shows data for all databases by aliases.
        '''
        glob_db = self.mdbNAliases
        modelsByAliases = dict({
                        glob_db['mdbName']['alias']: list([
                            Race, Male, Female, Surname]),
                        glob_db['mdbAnalytic']['alias']: list([
                            GlobalCounts, NameLettersCount, VowelsCount, 
                            ConsonantsCount, FirstLetters, Letters,
                            ChainsCombinations, NameEndings, 
                            VowelsChains, ConsonantsChains]),
                        glob_db['mdbCheckSum']['alias']: list([
                            GlobalFlags, ChecksumFiles]),
                        })

        self.printDatabases(modelsByAliases)
        return
###FINISH FunctionalBlock

###START MainBlock
def main():
    '''
    Entry point for working with databases.
    '''
    tools = ME_DBService()
    #_ = tools.registerDataBases()
    
    #tools.showDBData()
###FINISH Mainblock