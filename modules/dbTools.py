###START ImportBlock
##systemImport
import json
import typing as typ
import mongoengine as medb
import pickle

from bson.objectid import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.database import Database

##customImport
from configs.CFGNames import ME_SETTINGS
from configs.CFGNames import CHECKSUM_DB_GLOBAL_FLAG
from templates.templateAnalysis import TEMPLATE_GLOBAL_RACE
from templates.templateAnalysis import TEMPLATE_LOCAL_RACE

from database.medbNameSchemas import Race, Female, Male
from database.medbNameSchemas import Surnames, GenderGroups

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
    mdbUser = ME_SETTINGS.mdbUser
    mdbPass = ME_SETTINGS.mdbPass
    mdbCluster = ME_SETTINGS.mdbCluster
    mdbNAliases = ME_SETTINGS.MDB_n_Aliases

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
            medb.GenericEmbeddedDocumentField, medb.EmbeddedDocumentListField))
                
        return fieldsContainersCollections

    @classmethod
    def getUniqueIndexes(cls, collection: MECollection) -> typ.List[dict]:
        '''
        Gets the unique indexes of collection.
        '''
        uniqueFields = dict({'fields': list()})

        indexes = collection._meta.get('index_specs')
        for index in indexes:
            if 'unique' not in index or not index['unique']:
                continue
            elif ('_cls', 1) in index['fields']:
                _ = index['fields'].remove(('_cls', 1))
            elif ('_id', 1) in index['fields']:
                _ = index['fields'].remove(('_id', 1))
            
            if not all(field in uniqueFields['fields'] 
                       for field in index['fields']):
                uniqueFields['fields'].extend(index['fields'])

        if not uniqueFields['fields']:
            return None
        return list([uniqueFields])

    @classmethod
    def getUniqueRAWData(cls, collection: MECollection,
                         data: typ.Dict[str, dict]) -> typ.Dict[str, dict]:
        '''
        Gets unique fields and makes raw data from them.
        '''
        rawData = dict()

        uniqueFieldsData = collection._unique_with_indexes()
        if not uniqueFieldsData:
            uniqueFieldsData = cls.getUniqueIndexes(collection)
            if not uniqueFieldsData:
                return None

        uniqueFieldsData = uniqueFieldsData[0]

        uniqueFields = uniqueFieldsData['fields']
        if uniqueFields:

            for fieldIndex in uniqueFields:
                field = fieldIndex[0]

                if field in data:
                    value = data[field]
                    
                    referenceFields = cls.getReferenceFields()
                    collectionField = getattr(collection, field, None)
                    if isinstance(collectionField, referenceFields):
                        value = cls.getReferenceID(collectionField, data)

                    rawData.update({field: value})

        return rawData

    @classmethod
    def getConnectString(cls, mdb: str) -> str:
        '''
        Makes connection string for mongodb.
        '''
        connectString = "mongodb+srv://" + cls.mdbUser + ":" + cls.mdbPass + \
                        "@" + cls.mdbCluster + ".9wwxd.mongodb.net/" + \
                        mdb + "?retryWrites=true&w=majority"

        return connectString

    @classmethod
    def getConnect(cls, mdb: str, mdb_alias: str) -> MongoClient:
        '''
        Connects to database and sets the alias.
        '''
        connectString = cls.getConnectString(mdb)
        client = medb.connect(host=connectString, alias=mdb_alias)
        return client

    @classmethod
    def registerDataBases(cls) -> typ.Dict[str, MongoClient]:
        '''
        Connects to all databases by dictionary.
        '''
        clients = dict({})
        for database in cls.mdbNAliases:
            db = cls.mdbNAliases[database]['db_name']
            alias = cls.mdbNAliases[database]['alias']
            client = cls.getConnect(db, alias)
            clients.update({alias: client})

        return clients

    @classmethod
    def unregisterDataBases(cls) -> typ.NoReturn:
        '''
        Disconnects of all databases by dictionary.
        '''
        for database in cls.mdbNAliases:
            alias = cls.mdbNAliases[database]['alias']
            _ = medb.disconnect(alias)

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
    def insertEmbeddedField(cls, document: MEDocument, 
                    field: str, 
                    data: typ.Dict[str, dict]) -> MEDocument:
        '''
        Checks the embedded field and data, and inserts into the document.
        '''
        collection = document.__class__
        embeddedType = collection._fields.get(field)

        if type(data[field]) is dict:
            embeddedCollection = embeddedType.document_type
            subDocument = cls.setDocument(embeddedCollection, data[field])
            setattr(document, field, subDocument)

        elif type(data[field]) is list:     
            if not hasattr(collection, '_get_embedded_list_field_type'):
                return document

            embeddedCollection = collection._get_embedded_list_field_type(embeddedType.name)

            for keyData in data[field]:
                subDocument = cls.setDocument(embeddedCollection, keyData)
                
                if hasattr(document, 'add_unique'):
                    document.add_unique(field, subDocument)
        
        return document

    @classmethod
    def insertField(cls, document: MEDocument, field: str, 
                    data: typ.Dict[str, dict]) -> MEDocument:
        '''
        Checks the field and data, and inserts into the document.
        '''
        collection = document.__class__
        referenceFields = cls.getReferenceFields()
        fieldsContainersCollections = cls.getFieldsContainersCollections()
        collectionField = getattr(collection, field, None)

        if isinstance(collectionField, referenceFields):
            setattr(document, field, cls.getReferenceID(collectionField, data))

        elif isinstance(collectionField, fieldsContainersCollections):
            document = cls.insertEmbeddedField(document, field, data)

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
                document = cls.insertField(document, field, data)

        return document

    @classmethod
    def insertDocument(cls, collection: MECollection,
                       data: typ.Dict[str, dict]) -> typ.Union[str, None]:
        '''
        Prepaires and saves document.
        '''        
        document = cls.checkDocExist(collection, data)
        if document:
            return "INF: Document already exist. Insert canceled."

        document = cls.setDocument(collection, data)
        answer = None
        try:
            document.save()

        except medb.NotUniqueError as err:
            answer = getattr(err, 'message', str(err))

        return answer

    @classmethod
    def updateDocument(cls, document: typ.List[MEDocument],
                       data: typ.Dict[str, dict]) -> typ.List[str]:
        '''
        Prepaires and updates document.
        '''
        document = cls.setDocument(document, data)
        answer = None
        try:
            document.save()

        except medb.NotUniqueError as err:
            answer = getattr(err, 'message', str(err))

        return answer

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
        obj = collection.objects(__raw__=rawQuery).first()

        if obj:
            return obj
        return None

    @classmethod
    def updateOrInsertDocument(cls, collection: MECollection,
                               data: typ.Dict[str, dict]) -> str:
        '''
        Updates the document if it exists, 
        otherwise prepares and inserts a new one.
        '''
        answer = ''

        document = cls.checkDocExist(collection, data)
        if not document:
            answer = cls.insertDocument(collection, data)
        else:
            answer = cls.updateDocument(document, data)

        return answer

    @classmethod
    def updateDocumentIfExist(cls, collection: MECollection,
                               data: typ.Dict[str, dict]) -> str:
        '''
        Only updates the document if it exists.
        '''
        document = cls.checkDocExist(collection, data)
        if not document:
            return "WRN: Document not exist. Update canceled."

        answer = cls.updateDocument(document, data)
        return answer    

    @classmethod
    def writeDocuments(cls, collection: MECollection,
                       listOfData: typ.List[dict],
                       operation: str) -> typ.Union[list, None]:
        '''
        Writes document data for the entire collection.
        '''
        answers = list([])
        operations = {
            'insert_only': cls.insertDocument,
            'update_or_insert': cls.updateOrInsertDocument,
            'update_only': cls.updateDocumentIfExist
        }

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
        Writes prepared data for few collections in the database.
        '''
        allAnswers = list()
        for collectionName in collectionsData.keys():
            collection = collectionsData[collectionName]['collection']
            listOfData = collectionsData[collectionName]['data']
            operation = collectionsData[collectionName]['operation']
            answers = cls.writeDocuments(collection, listOfData, operation)
            
            if answers:
                allAnswers.extend(answers)

        return allAnswers


class ME_DBService():
    '''
    Contains tools for working with mongoengine and mongodb.
    '''
    mdbNAliases = ME_SETTINGS.MDB_n_Aliases
    genderGroups = dict({'Male': Male._class_name, 
                        'Female': Female._class_name, 
                        'Surnames': Surnames._class_name,
                        'Common': 'Common'})

    def getTemplate(self, template: typ.Any) -> typ.Any:
        '''
        Gets fast deepcopy of template.
        '''
        _tmpDump = pickle.dumps(template, -1)
        return pickle.loads(_tmpDump)

    def getNamesByRace(self, raceObject: MEDocument, 
                        collection: MECollection) -> typ.List[str]:
        '''
        Returns names list by target race.
        '''
        assert getattr(collection, 'name', None) is not None, \
                "The collection does not have a 'name' field."
        objs = collection.objects(race=raceObject).only('name').all()
        names = list([str(obj.name) for obj in objs])

        return names

    def getPreparedRaceData(self, raceObject: MEDocument) -> typ.Dict[str, dict]:
        '''
        Prepairs data by current race.
        '''
        raceField = getattr(raceObject, 'race', None)
        raceData = self.getTemplate(TEMPLATE_LOCAL_RACE)
        tmpKey = str(next(iter(raceData)))

        if not raceField or not tmpKey: 
            return None

        raceData[raceField] = raceData.pop(tmpKey)
        return raceData

    @classmethod
    def getIdByField(cls, collection: MECollection, 
                     field: str, value: str) -> ObjectId:
        '''
        Gets id by field from collection.
        '''
        collectionField = getattr(collection, field, None)
        if not collectionField:
            return None
            
        objId = MongoDBTools.getReferenceID(collectionField, 
                                            {field: value})
        return objId

    @classmethod
    def getLocalAnalyticDataByKeys(cls, collection: MECollection, race: str, 
                                   genderGroup: str) -> typ.List[dict]:
        '''
        Reads analytic data from collection by target keys.
        '''
        raceId = cls.getIdByField(collection, 'race', race)
        genderId = cls.getIdByField(collection, 'gender_group', genderGroup)

        if not raceId or not genderId:
            return list()

        filteredObjects = collection.objects(medb.Q(race=raceId) & 
                                            medb.Q(gender_group=genderId))

        filteredData = filteredObjects.to_json()
        filteredData = json.loads(filteredData)
        
        return filteredData

    def prepareToWriteNamesData(self, race: str, data: list) -> typ.Dict[str, dict]:
        '''
        Adapts the names database to the mongoengine schema.
        '''
        collectionData = list({})
        for name in data:
            collectionData.append({'name': str(name), 'race': str(race)})

        return collectionData

    def readNamesDBByRace(self, raceObject: MEDocument) -> typ.Dict[str, list]:
        '''
        Returns a base of names grouped by collection names.
        '''
        genderCollections = list([Male, Female, Surnames])

        namesByCollections = dict()
        for collection in genderCollections:
            names = self.getNamesByRace(raceObject, collection)
            namesByCollections.update({collection._class_name: names})

        return namesByCollections

    def setChecksumGlobalDB_ME(self, value):
        '''
        Sets only the global exist flag in checksum db from mongodb.
        '''
        globFlag = GlobalFlags.objects.first()
        if len(globFlag) == 0:
            globFlag = GlobalFlags()
            
        globFlag.globalExist = value
        answer = globFlag.save()
        return answer

    def fillRaceData(self, raceObject: MEDocument, 
                    raceData: typ.Dict[str, dict]) -> typ.Dict[str, dict]:
        '''
        Populates a prepared race template with names data.
        '''
        raceField = getattr(raceObject, 'race', None)
        if not raceField: 
            return None

        namesByCollections = self.readNamesDBByRace(raceObject)

        for collection in namesByCollections.keys():
            if collection in raceData[raceField]["Genders"].keys():
                genderData = raceData[raceField]["Genders"][collection]
                genderData["Names"]= namesByCollections[collection]

            elif collection in raceData[raceField].keys():
                raceData[raceField][collection] = namesByCollections[collection]
            
        return raceData

    def fillGlobalCountsData(self, raceKey: str, 
                            raceData: typ.Dict[str, dict]
                            ) -> typ.List[typ.Dict[str, dict]]:
        '''
        Adapts the global counts data to the mongoengine schema.
        '''
        globalCountsData = list([{
            'race': raceKey, 
            'maxNamesCount': raceData.pop('Max_Names_Count'),
            'femaleNamesCount': raceData.pop('Female_Names_Count'),
            'maleNamesCount': raceData.pop('Male_Names_Count'),
            'surnamesCount': raceData.pop('Surnames_Count'),
            'firstLettersCounts': {
                'vowelsCount': raceData['First_Letters'].pop('Vowels_Count'),
                'consonantsCount': raceData['First_Letters'].pop('Consonants_Count')
            }
        }])
        
        return globalCountsData

    def prepareGlobalCountsData(self, raceKey: str, 
                                raceData: typ.Dict[str, dict]
                                ) -> typ.Dict[str, dict]:
        '''
        Prepares and arranges the global counts data for writing.
        '''
        globalCountsData = self.fillGlobalCountsData(raceKey, raceData)

        collectionsData = {
            'GlobalCounts': {
                'collection': GlobalCounts,
                'data': globalCountsData,
                'operation': 'update_or_insert'
        }}
        return collectionsData

    @classmethod
    def fillAnalyticCountCollection(cls, raceKey: str, 
                        raceData: typ.Dict[str, dict], 
                        localAnalyticKey: str) -> typ.Dict[str, dict]:
        '''
        Adapts the analytic counts data to the mongoengine schema.
        '''
        localAnalyticData = raceData.pop(localAnalyticKey)

        collectionData = list([])
        
        for genderGroupKey in localAnalyticData:
            genderGroupData = localAnalyticData[genderGroupKey]

            for key in genderGroupData:
                keyData = genderGroupData[key]

                collectionData.append(
                    {'race': raceKey, 
                    'gender_group': genderGroupKey,
                    'key': key,
                    'count': keyData['Count'],
                    'chance': keyData['Chance']
                    }
                )

        return collectionData

    def prepareAnalyticCountCollections(self, raceKey: str, 
                                        raceData: typ.Dict[str, dict]
                                        ) -> typ.Dict[str, dict]:
        '''
        Prepares and arranges the analytic counts data for writing.        
        '''
        collectionsData = dict({})

        analyticCountCollections = dict({
            'Name_Letters_Count': NameLettersCount, 
            'Vowels_Count': VowelsCount, 
            'Consonants_Count': ConsonantsCount,
            'First_Letters': FirstLetters, 
            'Letters': Letters, 
            'Chains_Combinations': ChainsCombinations, 
            'Name_Endings': NameEndings
            })

        for localAnalyticKey in analyticCountCollections.keys():
            collectionName = analyticCountCollections[localAnalyticKey]._class_name
            collectionData = self.fillAnalyticCountCollection(raceKey, raceData, localAnalyticKey)

            collectionsData.update({
                collectionName: {
                    'collection': analyticCountCollections[localAnalyticKey],
                    'data': collectionData,
                    'operation': 'update_or_insert'
                }
            })
        
        return collectionsData

    def fillLocalChainData(self, genderGroupData: typ.Dict[str, dict]
                                                ) -> typ.Dict[str, dict]:
        '''
        Adapts the loacal analytic chain data to the mongoengine 
        embedded document schema.
        '''
        localKeysData = list([])
        for key in genderGroupData:
            keyData = genderGroupData[key]

            if 'Max_Count_In_Name' in keyData.keys():
                editedKey = key.split('_')[0]
                localKeyData = {
                    'length': editedKey, 
                    'maxCountInName': keyData['Max_Count_In_Name'], 
                    'namesCount': keyData['Names_Count'], 
                    'chance': keyData['Chance']}
                
            else:
                localKeyData = {
                    'key': key, 
                    'count': keyData['Count'], 
                    'chance': keyData['Chance']}

            localKeysData.append(localKeyData)
        
        return localKeysData
    
    def unpackAnalyticChainData(self, localAnalyticData: typ.Dict[str, dict]
                                                    ) -> typ.Dict[str, dict]:
        '''
        Unpacks the gender groups data from analytic subkeys.
        '''
        unpackedData = dict({})
        for localSubkey in localAnalyticData:
            localSubdata = localAnalyticData[localSubkey]

            for genderGroupKey in localSubdata:
                genderGroupData = localSubdata[genderGroupKey]
                localKeysData = self.fillLocalChainData(genderGroupData)

                if genderGroupKey not in unpackedData.keys():
                    unpackedData[genderGroupKey] = dict()

                unpackedData[genderGroupKey].update(
                    {localSubkey: localKeysData})
                    
        return unpackedData

    def fillAnalyticChainCollection(self, raceKey: str, 
                                    unpackedData: typ.Dict[str, dict]
                                    ) -> typ.Dict[str, dict]:
        '''
        Adapts the analytic chain data to the mongoengine schema.
        '''
        embeddedChainsKeys = {'Chains': 'chains', 
            'Chain_Frequency': 'chainFrequency', 
            'Length_Count_Names': 'lengthCountNames'}

        collectionData = list([])
        for genderGroupKey in unpackedData:
            genderGroupData = unpackedData[genderGroupKey]

            consonantsChainsData = dict({
                'race': raceKey,
                'gender_group': genderGroupKey})

            for chainKey in genderGroupData:
                chainData = genderGroupData[chainKey]

                consonantsChainsData.update({
                    embeddedChainsKeys[chainKey]: chainData})
                        
            collectionData.append(consonantsChainsData)

        return collectionData

    def prepareAnalyticChainCollection(self, raceKey: str, 
                                       raceData: typ.Dict[str, dict]
                                       ) -> typ.Dict[str, dict]:
        '''
        Prepares and arranges the analytic chain data for writing.       
        '''
        collectionsData = dict({})

        analyticCountCollections = dict({
            'Vowels_Chains': VowelsChains, 
            'Consonants_Chains': ConsonantsChains, 
            })
        
        for localAnalyticKey in analyticCountCollections.keys():
            localAnalyticData = raceData.pop(localAnalyticKey)
            unpackedData = self.unpackAnalyticChainData(localAnalyticData)

            collectionName = analyticCountCollections[localAnalyticKey]._class_name
            collectionData = self.fillAnalyticChainCollection(raceKey, unpackedData)

            collectionsData.update({
                collectionName: {
                    'collection': analyticCountCollections[localAnalyticKey],
                    'data': collectionData,
                    'operation': 'update_or_insert'
                }
            })
        
        return collectionsData

    def writeGendersDB_ME(self) -> typ.List[str]:
        '''
        Writes gender groups in own collection.
        '''
        genderGroupsData = list([])
        for gGr in self.genderGroups.keys():
            genderGroupsData.append({'gender_group': self.genderGroups[gGr]})

        collectionsData = dict({
                'GenderGroups': {
                    'collection': GenderGroups,
                    'data': genderGroupsData,
                    'operation': 'insert_only'
                }
            })
        answer = MongoDBTools.writeDatabase(collectionsData)

        if not answer:
            return list([])
        return answer

    def readBaseOfNamesDB_ME(self) -> typ.Dict[str, dict]:
        '''
        Returns a base of names grouped by races.
        '''
        baseOfNames = self.getTemplate(TEMPLATE_GLOBAL_RACE)

        objsRace = Race.objects.all()
        for raceObject in objsRace:

            raceData = self.getPreparedRaceData(raceObject)
            if not raceData: continue

            raceData = self.fillRaceData(raceObject, raceData)
            if not raceData: continue
            
            baseOfNames["Races"].append(raceData)
            
        return baseOfNames

    def writeBaseOfNamesDB_ME(self, namesDict: typ.Dict[str, dict]
                                                ) -> typ.List[str]:
        '''
        Adapts the names database to the database format 
        and writes it out.
        '''
        answers = list([])
        gGr = self.genderGroups

        answer = self.writeGendersDB_ME()
        answers.extend(answer)

        for race in namesDict['Races']:
            raceName = str(next(iter(race)))
            maleNames = race[raceName]['Genders'][
                            gGr['Male']]['Names']
            femaleNames = race[raceName]['Genders'][
                            gGr['Female']]['Names']
            surnames = race[raceName][
                            gGr['Surnames']]

            racesData= list([{'race': raceName}])
            malesData = self.prepareToWriteNamesData(raceName, maleNames)
            femalesData = self.prepareToWriteNamesData(raceName, femaleNames)
            surnamesData = self.prepareToWriteNamesData(raceName, surnames)

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
                    'collection': Surnames,
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

    def writeAnalyticsDB_ME(self, analyticDB: typ.Dict[str, dict]
                                                ) -> typ.List[str]:
        '''
        Adapts the analytic database to the database format 
        and writes it out.
        '''
        answers = list([])

        for raceKey in analyticDB['Analytics']:
            collectionsData = dict({})
            raceData = analyticDB['Analytics'][raceKey]

            collectionsData.update(
                self.prepareGlobalCountsData(raceKey, raceData)
            )
            collectionsData.update(
                self.prepareAnalyticCountCollections(raceKey, raceData)
            )
            collectionsData.update(
                self.prepareAnalyticChainCollection(raceKey, raceData)
            )

            answer = MongoDBTools.writeDatabase(collectionsData)
            if answer: 
                answers.append(answer)

        if not answers:
            answers = list(["Analytic db writed in mongoDB."])
        return answers
###FINISH FunctionalBlock


###START MainBlock
def main() -> typ.NoReturn:
    '''
    Entry point for working with databases.
    '''
    tools = ME_DBService()
    print()

###FINISH Mainblock
