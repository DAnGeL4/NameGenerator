###START ImportBlock
##systemImport
import json
import typing as typ
import mongoengine as medb

from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.database import Database

##customImport
from configs.CFGNames import ME_SETTINGS
from configs.CFGNames import CHECKSUM_DB_GLOBAL_FLAG

from database.medbNameSchemas import Race, Female, Male, Surname

from database.medbAnalyticSchemas import GlobalCounts, NameLettersCount
from database.medbAnalyticSchemas import VowelsCount, ConsonantsCount
from database.medbAnalyticSchemas import FirstLetters, Letters
from database.medbAnalyticSchemas import ChainsCombinations, NameEndings
from database.medbAnalyticSchemas import VowelsChains, ConsonantsChains

from database.medbCheckSumSchemas import GlobalFlags, ChecksumFiles
###FINISH ImportBlock

###START GlobalConstantBlock
MEField = typ.NewType('MongoEngineField', medb.Document)
MECollection = typ.NewType('MongoEngineCollection', medb.Document)
MEDocument = typ.NewType('MongoEngineDocument', MECollection)

###FINISH GlobalConstantBlock

###START DecoratorBlock
###FINISH DecoratorBlock


###START FunctionalBlock
class MongoDBTools:
    '''
    A class containing tools for working with MongoDB using mongoEngine.
    '''
    @staticmethod
    def getMDBObject(mdb: str) -> Database:
        '''
        Returns mongodb object.
        '''
        if not mdb:
            return None, "ERR: mdb is not defined"

        mdbNAliases = ME_SETTINGS.MDB_n_Aliases
        mdbAlias = mdbNAliases[mdb]['alias']

        if not mdbAlias:
            return None, "ERR: Have not alias for mdb."

        mdbObject = medb.get_db(mdbAlias)

        if not mdbObject:
            return None, "ERR: Have not database by alias."

        return mdbObject, None

    @staticmethod
    def getReferenceID(collectionField: MEField,
                       data: typ.Dict[str, dict]) -> ObjectId:
        '''
        Gets id for reference field of document.
        '''
        field = collectionField.db_field
        referenceCollection = collectionField.document_type_obj
        referenceDocument = referenceCollection.objects.get(
            __raw__={field: data[field]})
        if referenceDocument:
            return referenceDocument.id
        return None

    @staticmethod
    def getReferenceFields() -> typ.Tuple[MEField]:
        '''
        Returns tuple of mongoengine reference fields.
        '''
        referenceFields = tuple((medb.GenericReferenceField,
                                 medb.LazyReferenceField, medb.ReferenceField))
        return referenceFields

    @staticmethod
    def getFieldsContainersCollections() -> typ.Tuple[MEField]:
        '''
        Returns tuple of mongoengine fields of collections containers.
        '''
        fieldsContainersCollections = tuple(
            (medb.DynamicField, medb.EmbeddedDocumentField,
             medb.GenericEmbeddedDocumentField))
        return fieldsContainersCollections

    @staticmethod
    def getUniqueRAWData(collection: MECollection,
                         data: typ.Dict[str, dict]) -> typ.Dict[str, dict]:
        '''
        Gets unique fields and makes raw data from them.
        '''
        rawData = dict()
        uniqueFieldsData = collection._unique_with_indexes()
        if not uniqueFieldsData:
            return None

        uniqueFieldsData = uniqueFieldsData[0]

        uniqueFields = uniqueFieldsData['fields']
        if uniqueFields:

            for fieldIndex in uniqueFields:
                field = fieldIndex[0]

                if field in data:
                    rawData.update({field: data[field]})

        return rawData

    @classmethod
    def eraseME_DB(cls, mdb: str = None) -> str:
        '''
        Drops and recreates empty all collections from the target database.
        '''
        mdbObject, answ = cls.getMDBObject(mdb)
        if not mdbObject:
            return answ

        listCollections = mdbObject.list_collection_names()

        for collectionName in listCollections:
            mdbObject.drop_collection(collectionName)
            mdbObject.create_collection(collectionName)

        return "INF: Target Mongo db erased. Recreated empty."

    @classmethod
    def insertField(cls, document: MEDocument, collection: MECollection,
                    field: str, data: typ.Dict[str, dict]) -> MEDocument:
        '''
        Checks the field and data, and inserts into the document.
        '''
        referenceFields = cls.getReferenceFields()
        fieldsContainersCollections = cls.getFieldsContainersCollections()
        collectionField = getattr(collection, field, None)

        if isinstance(collectionField, referenceFields):
            setattr(document, field, cls.getReferenceID(collectionField, data))

        elif isinstance(collectionField, fieldsContainersCollections):
            if type(data[field]) is dict:
                document = cls.setDocument(document[field], data[field])

        else:
            setattr(document, field, data[field])

        return document

    @classmethod
    def setDocument(cls, collection: MECollection,
                    data: typ.Dict[str, dict]) -> MEDocument:
        '''
        Prepraires and inserts data into the document.
        '''
        document = None
        if collection._initialised is True:
            document = collection
        else:
            document = collection()

        for field in data.keys():

            if hasattr(collection, field):
                document = cls.insertField(document, collection, field, data)

        return document

    @classmethod
    def insertDocument(cls, collection: MECollection,
                       data: typ.Dict[str, dict]) -> typ.Union[str, None]:
        '''
        Prepraires and saves document.
        '''
        documents = cls.checkDocExist(collection, data)
        if documents:
            return "INF: Document already exist. Insert canceled"

        document = cls.setDocument(collection, data)
        answer = None
        try:
            document.save()

        except medb.NotUniqueError as err:
            answer = getattr(err, 'message', str(err))

        return answer

    @classmethod
    def updateDocument(cls, documents: typ.List[MEDocument],
                       data: typ.Dict[str, dict]) -> typ.List[str]:
        '''
        Prepraires and updates document.
        '''
        answers = list()
        for document in documents:
            document = cls.setDocument(document, data)

            answer = None
            try:
                document.save()

            except medb.NotUniqueError as err:
                answer = getattr(err, 'message', str(err))
            answers.append(answer)

        return answers

    @classmethod
    def checkDocExist(
            cls, collection: MECollection,
            data: typ.Dict[str, dict]
            ) -> typ.Union[typ.List[MEDocument], None]:
        '''
        Checks if documents already exists in db.
        '''
        uniqueRawData = cls.getUniqueRAWData(collection, data)

        rawQuery = uniqueRawData if uniqueRawData else data
        objs = collection.objects(__raw__=rawQuery).all()

        if objs:
            return objs
        return None

    @classmethod
    def updateOrInsertDocument(cls, collection: MECollection,
                               data: typ.Dict[str, dict]) -> str:
        '''
        Updates the document if it exists, 
        otherwise prepares and inserts a new one.
        '''
        answer = ''

        documents = cls.checkDocExist(collection, data)
        if not documents:
            answer = cls.insertDocument(collection, data)
        else:
            answer = cls.updateDocument(documents, data)

        return str(answer)

    @classmethod
    def writeDocuments(cls, collection: MECollection,
                       listOfData: typ.List[dict],
                       operation: str) -> typ.Union[list, None]:
        '''
        Writes document data for the entire collection.
        '''
        answers = list()
        operations = {
            'insert_only': cls.insertDocument,
            'update_or_insert': cls.updateOrInsertDocument,
            'update_only': cls.insertDocument
        }  #need to do

        if operation not in operations:
            answers.append('ERR: Unknown operation.')
            return answers

        for data in listOfData:
            answer = operations[operation](collection, data)

            if answer:
                answers.append(answer)

        if not answers:
            answers = None
        return answers

    @classmethod
    def writeDatabase(cls, collectionsData: typ.Dict[str, dict]
                                        ) -> typ.Union[list, None]:
        '''
        Writes prepared data for all collections in the database.
        '''
        for collectionName in collectionsData.keys():
            collection = collectionsData[collectionName]['collection']
            listOfData = collectionsData[collectionName]['data']
            operation = collectionsData[collectionName]['operation']
            answers = cls.writeDocuments(collection, listOfData, operation)

        return answers

    @classmethod
    def printCollection(cls, collection: MECollection) -> typ.NoReturn:
        '''
        Custom print on demand for collection fields.
        '''
        print("\n #MEDATA_module.1 {0} len: {1}".format(
            collection._class_name, len(collection.objects)))
        for obj in collection.objects:
            printString = ""  #\n  ##MEDATA_module.1.1 \n"

            for field in obj._fields:
                printString += "   *" + str(field) + ": " + str(
                    obj[field]) + "\n"

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

    def getConnectString(self, mdb: str) -> str:
        '''
        Makes connection string for mongodb.
        '''
        connectString = "mongodb+srv://" + self.mdbUser + ":" + self.mdbPass + \
                        "@" + self.mdbCluster + ".9wwxd.mongodb.net/" + \
                        mdb + "?retryWrites=true&w=majority"

        return connectString

    def getConnect(self, mdb: str, mdb_alias: str) -> MongoClient:
        '''
        Connects to database and sets the alias.
        '''
        connectString = self.getConnectString(mdb)
        client = medb.connect(host=connectString, alias=mdb_alias)
        return client

    def registerDataBases(self) -> typ.Dict[str, MongoClient]:
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

    def prepareNamesData(self, race: str, data: list) -> typ.Dict[str, dict]:
        '''
        Adapts the names database to the mongoengine schema.
        '''
        collectionData = list({})
        for name in data:
            collectionData.append({'name': str(name), 'race': str(race)})

        return collectionData

    def readChecksumDB_ME(self) -> typ.Dict[str, dict]:
        '''
        Reads and adapts the checksum database to the dictionary format.
        '''
        ChecksumDB = dict()

        flagData = GlobalFlags.objects.first()
        if flagData:
            flagData = flagData.to_json()
            flagData = json.loads(flagData)
            _ = flagData.pop('_id')
            ChecksumDB.update(flagData)

        allData = ChecksumFiles.objects.all()
        if allData:
            allData = allData.to_json()
            allData = json.loads(allData)

            for filedata in allData:
                ChecksumDB.update({filedata["file"]: filedata["checksum"]})

        return ChecksumDB

    def writeChecksumDB_ME(self, checksumDB: typ.Dict[str, dict]
                                                    ) -> typ.List[str]:
        '''
        Adapts the checksum database to the database format 
        and writes it out.
        '''
        flagData = dict(
            {CHECKSUM_DB_GLOBAL_FLAG: checksumDB.pop(CHECKSUM_DB_GLOBAL_FLAG)})
        globFlagDB_ME = list([flagData])

        checksumDB_ME = list()
        for fileName in checksumDB.keys():
            data = dict({'file': fileName, 'checksum': checksumDB[fileName]})
            checksumDB_ME.append(data)

        collectionsData = dict({
            'GlobalFlags': {
                'collection': GlobalFlags,
                'data': globFlagDB_ME,
                'operation': 'update_or_insert'
            },
            'ChecksumFiles': {
                'collection': ChecksumFiles,
                'data': checksumDB_ME,
                'operation': 'update_or_insert'
            },
        })

        answers = MongoDBTools.writeDatabase(collectionsData)

        if not answers:
            answers = list(["Checksun db writed in mongoDB."])
        return answers

    def insertNames(self, namesDict: typ.Dict[str, dict]) -> typ.List[str]:
        '''
        Adapts the names database to the database format 
        and writes it out.
        '''
        answers = list([])
        racesData = list({})
        malesData = list({})
        femalesData = list({})
        surnamesData = list({})

        for race in namesDict['Races']:
            raceName = str(next(iter(race)))
            maleNames = race[raceName]['Genders']['Male']['Names']
            femaleNames = race[raceName]['Genders']['Female']['Names']
            surnames = race[raceName]['Surnames']

            racesData.append({'race': raceName})
            malesData = self.prepareNamesData(raceName, maleNames)
            femalesData = self.prepareNamesData(raceName, femaleNames)
            surnamesData = self.prepareNamesData(raceName, surnames)

            collectionsData = dict({
                'Race': {
                    'collection': Race,
                    'data': racesData,
                    'operation': 'insert_only'
                },
                'Male': {
                    'collection': Male,
                    'data': malesData,
                    'operation': 'insert_only'
                },
                'Female': {
                    'collection': Female,
                    'data': femalesData,
                    'operation': 'insert_only'
                },
                'Surname': {
                    'collection': Surname,
                    'data': surnamesData,
                    'operation': 'insert_only'
                },
            })

            answer = MongoDBTools.writeDatabase(collectionsData)
            if answer:
                answers.extend(answer)

        if not answers:
            answers = list(["Names inserted in mongoDB."])
        return answers

    def printDatabases(self, modelsByAliases: typ.Dict[str, list]
                                                    ) -> typ.NoReturn:
        '''
        Custom data printing for database.
        '''
        for alias in modelsByAliases.keys():
            print("\nMEDATA.x DB %s" % alias)

            models = modelsByAliases[alias]
            for model in models:
                MongoDBTools.printCollection(model)

    def showDBData(self) -> typ.NoReturn:
        '''
        Shows data for all databases by aliases.
        '''
        glob_db = self.mdbNAliases
        modelsByAliases = dict({
            glob_db['mdbName']['alias']:
            list([Race, Male, Female, Surname]),
            glob_db['mdbAnalytic']['alias']:
            list([
                GlobalCounts, NameLettersCount, VowelsCount, ConsonantsCount,
                FirstLetters, Letters, ChainsCombinations, NameEndings,
                VowelsChains, ConsonantsChains
            ]),
            glob_db['mdbCheckSum']['alias']:
            list([GlobalFlags, ChecksumFiles]),
        })

        self.printDatabases(modelsByAliases)


###FINISH FunctionalBlock


###START MainBlock
def main() -> typ.NoReturn:
    '''
    Entry point for working with databases.
    '''
    tools = ME_DBService()

    #tools.showDBData()


###FINISH Mainblock
