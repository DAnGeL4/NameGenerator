###START ImportBlock
##systemImport
import typing as typ
import json
import mongoengine as medb

from mongomock import MongoClient
from mongomock import Database

##customImport
from configs.CFGNames import ME_SETTINGS
#from configs.CFGNames import CHECKSUM_DB_GLOBAL_FLAG
from modules.dbTools import MongoDBTools, ME_DBService

from tests.test_Service import FunctionalClass

from database.medbCheckSumSchemas import GlobalFlags
#from database.medbCheckSumSchemas import ChecksumFiles

from database.medbNameSchemas import Race, GenderGroups, Male

from database.medbAnalyticSchemas import GlobalCounts, VowelsChains
from database.medbAnalyticSchemas import FirstLettersCounts, NameLettersCount
from database.medbAnalyticSchemas import FirstLetters

###FINISH ImportBlock

###START GlobalConstantBlock
###FINISH GlobalConstantBlock

###START DecoratorBlock
###FINISH DecoratorBlock


###START FunctionalBlock            
class MongoDBTools_Test(FunctionalClass):
    '''
    Testing next methods of class #MongoDBTools:
    getMDBObject;
    getReferenceID;
    getReferenceFields;
    getFieldsContainersCollections;
    getUniqueIndexes;
    getUniqueRAWData;
    getConnectString;
    getConnect;
    registerDataBases;
    unregisterDataBases;
    eraseME_DB;
    insertEmbeddedField;
    insertField;
    setDocument;
    insertDocument;
    updateDocument;
    checkDocExist;
    updateOrInsertDocument;
    updateDocumentIfExist;
    writeDocuments;
    writeDatabase;
    '''

    ##BEGIN ConstantBlock
    mdb_alias = ME_SETTINGS.MDB_n_Aliases['mdbName']['alias']
    mdb_analytic_alias = ME_SETTINGS.MDB_n_Aliases['mdbAnalytic']['alias']

    tst_mdbNAliases = MongoDBTools.mdbNAliases
    tst_getConnectString = MongoDBTools.getConnectString
    mdb_test = 'test_db'
    mdb_test_alias = 'test_alias'
    TestFiles = {}
    ##END ConstantBlock

    ##BEGIN PrepareBlock
    @classmethod
    def setUpClass(cls) -> typ.NoReturn:
        '''Set up for class.'''
        cls.printSetUpClassMsg()
        cls.createTestFiles()

        #Using mongomock for testing
        medb.connect('mongoenginetest', 
                host='mongomock://localhost', 
                alias=cls.mdb_alias)
        medb.connect('mongoenginetest2', 
                host='mongomock://localhost', 
                alias=cls.mdb_analytic_alias)

    @classmethod
    def tearDownClass(cls) -> typ.NoReturn:
        '''Tear down for class.'''
        medb.disconnect(alias=cls.mdb_alias)
        medb.disconnect(alias=cls.mdb_analytic_alias)

        cls.removeTestFiles()
        cls.printTearDownClassMsg()

    def setUp(self) -> typ.NoReturn:
        '''Set up for test.'''
        self.printSetUpMethodMsg()

        race = Race()
        race.race = 'TestRace'
        race.save()

        genderGp = GenderGroups()
        genderGp.gender_group = 'TestGender'
        genderGp.save()

        male = Male()
        male.race = race
        male.name = 'TestName'
        male.save()

    def tearDown(self) -> typ.NoReturn:
        '''Tear down for test.'''
        #Return class data back after manipulation in tests
        MongoDBTools.mdbNAliases = self.tst_mdbNAliases
        MongoDBTools.getConnectString = self.tst_getConnectString
        
        GlobalCounts.drop_collection()
        VowelsChains.drop_collection()
        NameLettersCount.drop_collection()

        Race.drop_collection()
        GenderGroups.drop_collection()
        Male.drop_collection()

        medb.disconnect(alias=self.mdb_test_alias)

        self.printTearDownMethodMsg()

    ##END PrepareBlock
    
    @FunctionalClass.descript
    def test_getMDBObject_getingDBObjesct_expectedDatabaseObject(
            self) -> typ.NoReturn:
        '''
        Testing the method of gets mongodb database object.
        '''
        answ = MongoDBTools.getMDBObject('mdbName')
        dbObj = answ[0]
        res: type = type(dbObj)
        
        self.assertEqual(res, Database)

    @FunctionalClass.descript
    def test_getReferenceID_readingReferenceId_expectedId(
            self) -> typ.NoReturn:
        '''
        Testing the method of gets id for reference field of document.
        '''
        race = Race.objects(race='TestRace').first()
        collectionField = getattr(Male, 'race', None)

        res: str = MongoDBTools.getReferenceID(collectionField, {'race': 'TestRace'})
        
        self.assertEqual(res, race.id)

    @FunctionalClass.descript
    def test_getReferenceFields_getingTupleOfFields_expectedTupleOfFields(
            self) -> typ.NoReturn:
        '''
        Testing the method of gets tuple of mongoengine reference fields.
        '''
        referenceFields = tuple((medb.GenericReferenceField,
                                  medb.LazyReferenceField, 
                                  medb.ReferenceField))

        res: tuple = MongoDBTools.getReferenceFields()
        
        self.assertTupleEqual(res, referenceFields)

    @FunctionalClass.descript
    def test_getFieldsContainersCollections_getingTupleOfFields_expectedTupleOfFields(
            self) -> typ.NoReturn:
        '''
        Testing the method of gets tuple of mongoengine fields of collections containers.
        '''
        containersFields = tuple((medb.DynamicField, 
                                  medb.EmbeddedDocumentField, 
                                  medb.GenericEmbeddedDocumentField, 
                                  medb.EmbeddedDocumentListField))

        res: tuple = MongoDBTools.getFieldsContainersCollections()
        
        self.assertTupleEqual(res, containersFields)

    @FunctionalClass.descript
    def test_getUniqueIndexes_getingUniqueIndexes_expectedListOfIndexes(
            self) -> typ.NoReturn:
        '''
        Testing the method of Gets the unique indexes of collection.
        '''
        res: list = MongoDBTools.getUniqueIndexes(NameLettersCount)
        
        self.assertListEqual(res, [{'fields': [
                                        ('race', 1), 
                                        ('gender_group', 1), 
                                        ('key', 1)
                                    ]}])

    @FunctionalClass.descript
    def test_getUniqueRAWData_makingRawData_expectedDict(
            self) -> typ.NoReturn:
        '''
        Testing the method of gets unique fields and makes raw data from them.
        '''
        res: dict = MongoDBTools.getUniqueRAWData(Race, {'race': 'TestData'})
        
        self.assertDictEqual(res, {'race': 'TestData'})

    @FunctionalClass.descript
    def tst_getConnectString_makingMongoConnectionString_expectedConnectionString(
            self) -> typ.NoReturn:
        '''
        Testing the method of makes connection string for mongodb.
        '''
        mdbUser = ME_SETTINGS.mdbUser
        mdbPass = ME_SETTINGS.mdbPass
        mdbCluster = ME_SETTINGS.mdbCluster
        mdb = 'TestDataBase'

        connectString = "mongodb+srv://" + mdbUser + ":" + mdbPass + \
                        "@" + mdbCluster + ".9wwxd.mongodb.net/" + \
                        mdb + "?retryWrites=true&w=majority"

        res: str = MongoDBTools.getConnectString(mdb)
        
        self.assertEqual(res, connectString)

    @FunctionalClass.descript
    def test_getConnect_establishingConnection_expectedClient(
            self) -> typ.NoReturn:
        '''
        Testing the method of connects to database and sets the alias.
        '''
        @classmethod
        def mockConnectionStr(cls, mdb: str):
            '''
            Replaces the original function with a 
            new one to get a connection to mongomoсk
            '''
            return 'mongomock://localhost@' + mdb

        mdb = self.mdb_test
        alias = self.mdb_test_alias
        MongoDBTools.getConnectString = mockConnectionStr


        client = MongoDBTools.getConnect(mdb, alias)
        res: object = type(client)
        
        self.assertEqual(res, MongoClient)

    @FunctionalClass.descript
    def test_registerDataBases_establishingConnections_expectedClientsList(
            self) -> typ.NoReturn:
        '''
        Testing the method of connects to all databases by dictionary.
        '''
        @classmethod
        def mockConnectionStr(cls, mdb: str):
            '''
            Replaces the original function with a 
            new one to get a connection to mongomoсk
            '''
            return 'mongomock://localhost@' + mdb

        mdb = self.mdb_test
        alias = self.mdb_test_alias
        MongoDBTools.getConnectString = mockConnectionStr
        MongoDBTools.mdbNAliases = dict({'test': {
                                        'db_name': mdb,
                                        'alias': alias}})

        answ = MongoDBTools.registerDataBases()
        res: object = type(answ['test_alias'])
        
        self.assertEqual(res, MongoClient)

    @FunctionalClass.descript
    def test_unregisterDataBases_breakingConnections_expectedNoConnections(
            self) -> typ.NoReturn:
        '''
        Testing the method of disconnects to all databases by dictionary.
        '''
        mdb = self.mdb_test
        alias = self.mdb_test_alias
        MongoDBTools.mdbNAliases = dict({'test': {
                                        'db_name': mdb,
                                        'alias': alias}})
        
        medb.connect(mdb, host='mongomock://localhost', 
                                            alias=alias)
        _ = MongoDBTools.unregisterDataBases()

        currentConnections = medb.connection._connections
        res: typ.Any = getattr(currentConnections, alias, None)
        
        self.assertEqual(res, None)

    @FunctionalClass.descript
    def test_eraseME_DB_recreatingEmptyCollections_expectedEmptyCollections(
            self) -> typ.NoReturn:
        '''
        Testing the method of recreates empty all collections.
        '''
        mdb = 'mdbName'
        _ = MongoDBTools.eraseME_DB(mdb)
        res: int = Race.objects.count()
        
        self.assertEqual(res, 0)

    @FunctionalClass.descript
    def test_insertEmbeddedField_fillingEmbeddedField_expectedDictDataInField(
            self) -> typ.NoReturn:
        '''
        Testing the method of inserts dict data into the embedded document.
        '''
        collection = GlobalCounts
        field = 'firstLettersCounts'
        data = dict({
            field: dict({
                'vowelsCount': 3,
                'consonantsCount': 3
            })
        })

        doc = collection()
        doc = MongoDBTools.insertEmbeddedField(doc, field, data)

        tmp = doc.to_json()
        tmp = json.loads(tmp)
        res = tmp[field]

        self.assertDictEqual(res, {'vowelsCount': 3, 'consonantsCount': 3})

    @FunctionalClass.descript
    def test_insertEmbeddedField_fillingEmbeddedField_expectedListDataInField(
            self) -> typ.NoReturn:
        '''
        Testing the method of inserts list data into the embedded document.
        '''
        collection = VowelsChains
        field = 'chains'
        data = dict({
            field: list([
                {'key': 'c', 'count': 3, 'chance': 3.0}
            ])
        })

        doc = collection()
        doc = MongoDBTools.insertEmbeddedField(doc, field, data)

        tmp = doc.to_json()
        tmp = json.loads(tmp)
        res = tmp[field]

        self.assertListEqual(res, [{'key': 'c', 'count': 3, 'chance': 3.0}])

    @FunctionalClass.descript
    def test_insertField_fillingReferenceField_expectedReferenceId(
            self) -> typ.NoReturn:
        '''
        Testing the method of inserts data into the document.
        '''
        race = Race.objects(race='TestRace').first()
        collection = GlobalCounts
        field = 'race'
        data = dict({field: 'TestRace'})

        doc = collection()
        doc = MongoDBTools.insertField(doc, field, data)

        tmp = doc.to_json()
        tmp = json.loads(tmp)
        res = tmp[field]

        self.assertDictEqual(res, {'$oid': str(race.id)})

    @FunctionalClass.descript
    def test_insertField_fillingField_expectedDataInField(
            self) -> typ.NoReturn:
        '''
        Testing the method of inserts data into the document.
        '''
        collection = GlobalCounts
        field = 'maxNamesCount'
        data = dict({field: 3})

        doc = collection()
        doc = MongoDBTools.insertField(doc, field, data)

        tmp = doc.to_json()
        tmp = json.loads(tmp)
        res = tmp[field]

        self.assertEqual(res, 3)

    @FunctionalClass.descript
    def test_insertField_fillingEmbeddedField_expectedDataInEmbeddedField(
            self) -> typ.NoReturn:
        '''
        Testing the method of inserts data into the document.
        '''
        collection = GlobalCounts
        field = 'firstLettersCounts'
        data = dict({
            field: dict({
                'vowelsCount': 3,
                'consonantsCount': 3
            })
        })

        doc = collection()
        doc = MongoDBTools.insertField(doc, field, data)

        tmp = doc.to_json()
        tmp = json.loads(tmp)
        res = tmp[field]

        self.assertDictEqual(res, {'vowelsCount': 3, 'consonantsCount': 3})

    @FunctionalClass.descript
    def test_setDocument_fillingAllFields_expectedFilledDocument(
            self) -> typ.NoReturn:
        '''
        Testing the method of prepraires and inserts data into the document.
        '''
        race = Race.objects(race='TestRace').first()
        collection = GlobalCounts
        data = dict({
            'race': 'TestRace',
            'maxNamesCount': 9,
            'femaleNamesCount': 3,
            'maleNamesCount': 3,
            'surnamesCount': 3,
            'firstLettersCounts': dict({
                'vowelsCount': 3,
                'consonantsCount': 3
            })
        })

        doc = MongoDBTools.setDocument(collection, data)

        tmp = doc.to_json()
        res = json.loads(tmp)

        self.assertDictEqual(res, { 'race': {'$oid': str(race.id)},
                                    'maxNamesCount': 9,
                                    'femaleNamesCount': 3,
                                    'maleNamesCount': 3,
                                    'surnamesCount': 3,
                                    'firstLettersCounts': {
                                        'vowelsCount': 3,
                                        'consonantsCount': 3}
                                })

    @FunctionalClass.descript
    def test_insertDocument_savingDocument_expectedSavedDocument(
            self) -> typ.NoReturn:
        '''
        Testing the method of prepaires and saves document.
        '''
        collection = Race
        data = dict({
            'race': 'NewTestRace'
        })

        _ = MongoDBTools.insertDocument(collection, data)
        res = Race.objects(race='NewTestRace').count()

        self.assertEqual(res, 1)

    @FunctionalClass.descript
    def test_insertDocument_savingExistingDocument_expectedWarningAnswer(
            self) -> typ.NoReturn:
        '''
        Testing the method of prepaires and saves document.
        '''
        collection = Race
        data = dict({
            'race': 'TestRace'
        })

        res = MongoDBTools.insertDocument(collection, data)

        self.assertEqual(res, "INF: Document already exist. Insert canceled.")

    @FunctionalClass.descript
    def test_insertDocument_savingExistingDocument_expectedNoDuplicate(
            self) -> typ.NoReturn:
        '''
        Testing the method of prepaires and saves document.
        '''
        collection = Race
        data = dict({
            'race': 'TestRace'
        })

        _ = MongoDBTools.insertDocument(collection, data)
        res = Race.objects(race='TestRace').count()

        self.assertEqual(res, 1)

    @FunctionalClass.descript
    def test_updateDocument_savingExistingDocument_expectedChangedDocument(
            self) -> typ.NoReturn:
        '''
        Testing the method of prepaires and updates document.
        '''
        race = Race.objects(race='TestRace').first()
        collection = GlobalCounts
        data = dict({
            'race': 'TestRace',
            'maxNamesCount': 9,
            'femaleNamesCount': 3,
            'maleNamesCount': 3,
            'surnamesCount': 3,
            'firstLettersCounts': dict({
                'vowelsCount': 3,
                'consonantsCount': 3
            })
        })
        
        doc = collection()
        doc.race = race.id
        doc.firstLettersCounts = FirstLettersCounts()
        doc.save()

        _ = MongoDBTools.updateDocument(doc, data)

        doc = GlobalCounts.objects.first()
        tmp = doc.to_json()
        res = json.loads(tmp)
        _ = res.pop('_id')

        self.assertDictEqual(res, { 'race': {'$oid': str(race.id)},
                                    'maxNamesCount': 9,
                                    'femaleNamesCount': 3,
                                    'maleNamesCount': 3,
                                    'surnamesCount': 3,
                                    'firstLettersCounts': {
                                        'vowelsCount': 3,
                                        'consonantsCount': 3}
                                })

    @FunctionalClass.descript
    def test_checkDocExist_checkingExistingDocument_expectedExist(
            self) -> typ.NoReturn:
        '''
        Testing the method of checks if documents already exists in db.
        '''
        collection = Race
        data = dict({
            'race': 'TestRace'
        })

        res = MongoDBTools.checkDocExist(collection, data)
        self.assertIsNotNone(res)

    @FunctionalClass.descript
    def test_checkDocExist_checkingExistingDocument_expectedNotExist(
            self) -> typ.NoReturn:
        '''
        Testing the method of checks if documents already exists in db.
        '''
        collection = Race
        data = dict({
            'race': 'NotExistRace'
        })

        res = MongoDBTools.checkDocExist(collection, data)
        self.assertIsNone(res)

    @FunctionalClass.descript
    def test_updateOrInsertDocument_savingExistingDocument_expectedChangedDocument(
            self) -> typ.NoReturn:
        '''
        Testing the method of prepaires and updates document.
        '''
        race = Race.objects(race='TestRace').first()
        collection = GlobalCounts
        data = dict({
            'race': 'TestRace',
            'maxNamesCount': 9,
            'femaleNamesCount': 3,
            'maleNamesCount': 3,
            'surnamesCount': 3,
            'firstLettersCounts': dict({
                'vowelsCount': 3,
                'consonantsCount': 3
            })
        })
        
        doc = collection()
        doc.race = race.id
        doc.firstLettersCounts = FirstLettersCounts()
        doc.save()

        _ = MongoDBTools.updateOrInsertDocument(collection, data)

        doc = GlobalCounts.objects.first()
        tmp = doc.to_json()
        res = json.loads(tmp)
        _ = res.pop('_id')

        self.assertDictEqual(res, { 'race': {'$oid': str(race.id)},
                                    'maxNamesCount': 9,
                                    'femaleNamesCount': 3,
                                    'maleNamesCount': 3,
                                    'surnamesCount': 3,
                                    'firstLettersCounts': {
                                        'vowelsCount': 3,
                                        'consonantsCount': 3}
                                })

    @FunctionalClass.descript
    def test_updateOrInsertDocument_savingNewDocument_expectedDocument(
            self) -> typ.NoReturn:
        '''
        Testing the method of prepaires and updates document.
        '''
        collection = Race
        data = dict({
            'race': 'NewTestRace'
        })

        _ = MongoDBTools.updateOrInsertDocument(collection, data)

        res = Race.objects(race='NewTestRace').count()
        self.assertEqual(res, 1)

    @FunctionalClass.descript
    def test_updateDocumentIfExist_updatingExistingDocument_expectedChangedDocument(
            self) -> typ.NoReturn:
        '''
        Testing the method of only updates the document.
        '''
        race = Race.objects(race='TestRace').first()
        collection = GlobalCounts
        data = dict({
            'race': 'TestRace',
            'maxNamesCount': 9,
            'femaleNamesCount': 3,
            'maleNamesCount': 3,
            'surnamesCount': 3,
            'firstLettersCounts': dict({
                'vowelsCount': 3,
                'consonantsCount': 3
            })
        })
        
        doc = collection()
        doc.race = race.id
        doc.firstLettersCounts = FirstLettersCounts()
        doc.save()

        _ = MongoDBTools.updateDocumentIfExist(collection, data)

        doc = GlobalCounts.objects.first()
        tmp = doc.to_json()
        res = json.loads(tmp)
        _ = res.pop('_id')

        self.assertDictEqual(res, { 'race': {'$oid': str(race.id)},
                                    'maxNamesCount': 9,
                                    'femaleNamesCount': 3,
                                    'maleNamesCount': 3,
                                    'surnamesCount': 3,
                                    'firstLettersCounts': {
                                        'vowelsCount': 3,
                                        'consonantsCount': 3}
                                })

    @FunctionalClass.descript
    def test_updateDocumentIfExist_updatingNewDocument_expectedWarningAnswer(
            self) -> typ.NoReturn:
        '''
        Testing the method of only updates the document.
        '''
        collection = Race
        data = dict({
            'race': 'NewTestRace'
        })

        res = MongoDBTools.updateDocumentIfExist(collection, data)
        self.assertEqual(res, "WRN: Document not exist. Update canceled.")

    @FunctionalClass.descript
    def test_writeDocuments_sendingIncorrectOperation_expectedRightAnswer(
            self) -> typ.NoReturn:
        '''
        Testing the method of writes document data for the entire collection.
        '''
        oprtn = 'incorrect'

        res = MongoDBTools.writeDocuments(None, None, oprtn)
        self.assertListEqual(res, ['ERR: Unknown operation.'])

    @FunctionalClass.descript
    def test_writeDocuments_savingNewDocuments_expectedDocuments(
            self) -> typ.NoReturn:
        '''
        Testing the method of writes document data for the 
        entire collection. Checking the insertion of a new document 
        and canceling the insertion of an existing one.
        '''
        collection = Race
        dataList = list([
            {'race': 'TestRace'},
            {'race': 'NewTestRace'},
            {'race': 'NewSecTestRace'}
        ])
        oprtn = 'insert_only'

        _ = MongoDBTools.writeDocuments(collection, dataList, oprtn)

        res = Race.objects.count()
        self.assertEqual(res, 3)

    @FunctionalClass.descript
    def test_writeDocuments_savingNewDocuments_expectedRightAnswer(
            self) -> typ.NoReturn:
        '''
        Testing the method of writes document data for the 
        entire collection. Checking the insertion of a new document 
        and canceling the insertion of an existing one.
        '''
        collection = Race
        dataList = list([
            {'race': 'TestRace'},
            {'race': 'NewTestRace'},
            {'race': 'NewSecTestRace'}
        ])
        oprtn = 'insert_only'

        res = MongoDBTools.writeDocuments(collection, dataList, oprtn)
        self.assertListEqual(res, 
                        ["INF: Document already exist. Insert canceled."])

    @FunctionalClass.descript
    def test_writeDocuments_updatingOrInsertingDocuments_expectedChangedDocuments(
            self) -> typ.NoReturn:
        '''
        Testing the method of prepaires and updates document.
        Checking inserting a new document and updating an existing one.
        '''
        race = Race.objects(race='TestRace').first()
        gender = GenderGroups.objects(gender_group='TestGender').first()
        collection = NameLettersCount
        dataList = list([
            {'race': 'TestRace',
            'gender_group': 'TestGender',
            'key': 3,
            'count': 3,
            'chance': 3.3},
            {'race': 'TestRace',
            'gender_group': 'TestGender',
            'key': 4,
            'count': 4,
            'chance': 4.4}
        ])
        oprtn = 'update_or_insert'
        
        doc = collection()
        doc.race = race.id
        doc.gender_group = gender.id
        doc.key = 3
        doc.save()

        _ = MongoDBTools.writeDocuments(collection, dataList, oprtn)
        
        docs = NameLettersCount.objects()
        tmp = docs.to_json()
        res: list = json.loads(tmp)

        for r in res:
            _ = r.pop('_id')
            _ = r.pop('_cls')

        self.assertListEqual(res, [{'race': {'$oid': str(race.id)},
                                    'gender_group': {'$oid': str(gender.id)},
                                    'key': 3,
                                    'count': 3,
                                    'chance': 3.3},
                                    {'race': {'$oid': str(race.id)},
                                    'gender_group': {'$oid': str(gender.id)},
                                    'key': 4,
                                    'count': 4,
                                    'chance': 4.4}])

    @FunctionalClass.descript
    def test_writeDocuments_updatingOrInsertingDocuments_expectedRightAnswer(
            self) -> typ.NoReturn:
        '''
        Testing the method of prepaires and updates document.
        Checking inserting a new document and updating an existing one.
        '''
        race = Race.objects(race='TestRace').first()
        gender = GenderGroups.objects(gender_group='TestGender').first()
        collection = NameLettersCount
        dataList = list([
            {'race': 'TestRace',
            'gender_group': 'TestGender',
            'key': 3,
            'count': 3,
            'chance': 3.3},
            {'race': 'TestRace',
            'gender_group': 'TestGender',
            'key': 4,
            'count': 4,
            'chance': 4.4}
        ])
        oprtn = 'update_or_insert'
        
        doc = collection()
        doc.race = race.id
        doc.gender_group = gender.id
        doc.key = 3
        doc.save()

        res = MongoDBTools.writeDocuments(collection, dataList, oprtn)
        self.assertIsNone(res)

    @FunctionalClass.descript
    def test_writeDocuments_onlyUpdatingDocuments_expectedChangedSomeDocuments(
            self) -> typ.NoReturn:
        '''
        Testing the method of prepaires and updates document.
        Checking only updating an existing document.
        '''
        race = Race.objects(race='TestRace').first()
        gender = GenderGroups.objects(gender_group='TestGender').first()
        collection = NameLettersCount
        dataList = list([
            {'race': 'TestRace',
            'gender_group': 'TestGender',
            'key': 3,
            'count': 3,
            'chance': 3.3},
            {'race': 'TestRace',
            'gender_group': 'TestGender',
            'key': 4,
            'count': 4,
            'chance': 4.4}
        ])
        oprtn = 'update_only'
        
        doc = collection()
        doc.race = race.id
        doc.gender_group = gender.id
        doc.key = 3
        doc.save()

        _ = MongoDBTools.writeDocuments(collection, dataList, oprtn)
        
        docs = NameLettersCount.objects()
        tmp = docs.to_json()
        res: list = json.loads(tmp)

        for r in res:
            _ = r.pop('_id')
            _ = r.pop('_cls')

        self.assertListEqual(res, [{'race': {'$oid': str(race.id)},
                                    'gender_group': {'$oid': str(gender.id)},
                                    'key': 3,
                                    'count': 3,
                                    'chance': 3.3}])

    @FunctionalClass.descript
    def test_writeDocuments_onlyUpdatingDocuments_expectedRightAnswer(
            self) -> typ.NoReturn:
        '''
        Testing the method of prepaires and updates document.
        Checking only updating an existing document.
        '''
        race = Race.objects(race='TestRace').first()
        gender = GenderGroups.objects(gender_group='TestGender').first()
        collection = NameLettersCount
        dataList = list([
            {'race': 'TestRace',
            'gender_group': 'TestGender',
            'key': 3,
            'count': 3,
            'chance': 3.3},
            {'race': 'TestRace',
            'gender_group': 'TestGender',
            'key': 4,
            'count': 4,
            'chance': 4.4}
        ])
        oprtn = 'update_only'
        
        doc = collection()
        doc.race = race.id
        doc.gender_group = gender.id
        doc.key = 3
        doc.save()

        res = MongoDBTools.writeDocuments(collection, dataList, oprtn)
        self.assertListEqual(res, ["WRN: Document not exist. Update canceled."])

    @FunctionalClass.descript
    def test_writeDatabase_insertingDocumentsForFewCollections_expectedRightData(
            self) -> typ.NoReturn:
        '''
        Testing the method of writes prepared data for 
        few collections in the database.
        '''
        collectionsData = dict({
            'Race': {
                'collection': Race,
                'data': list([
                    {'race': 'TestRace'},       #already exist
                    {'race': 'NewTestRace'},
                    {'race': 'NewSecTestRace'}]),
                'operation': 'insert_only'
            },
            'Male': {
                'collection': Male,
                'data': list([
                    {'race': 'TestRace',        #already exist
                    'name': 'TestName'},
                    {'race': 'NewTestRace',
                    'name': 'NewTestName'}]),
                'operation': 'insert_only'
            }
        })

        _ = MongoDBTools.writeDatabase(collectionsData)
        
        res = list()
        for collection in [Race, Male]:
            docs = collection.objects()
            tmp = docs.to_json()
            res.extend(json.loads(tmp))
        for r in res:
            _ = r.pop('_id')

        race1 = Race.objects(race='TestRace').first()
        race2 = Race.objects(race='NewTestRace').first()
        
        self.assertListEqual(res, [ {'race': 'TestRace'},
                                    {'race': 'NewTestRace'},
                                    {'race': 'NewSecTestRace'},
                                    {'_cls': 'Male',
                                    'race': {'$oid': str(race1.id)},
                                    'name': 'TestName'},
                                    {'_cls': 'Male',
                                    'race': {'$oid': str(race2.id)},
                                    'name': 'NewTestName'}
                                ])

    @FunctionalClass.descript
    def test_writeDatabase_insertingDocumentsForFewCollections_expectedRightAnswer(
            self) -> typ.NoReturn:
        '''
        Testing the method of writes prepared data for 
        few collections in the database.
        '''
        collectionsData = dict({
            'Race': {
                'collection': Race,
                'data': list([
                    {'race': 'TestRace'},       #already exist
                    {'race': 'NewTestRace'},
                    {'race': 'NewSecTestRace'}]),
                'operation': 'insert_only'
            },
            'Male': {
                'collection': Male,
                'data': list([
                    {'race': 'TestRace',        #already exist
                    'name': 'TestName'},
                    {'race': 'NewTestRace',
                    'name': 'NewTestName'}]),
                'operation': 'insert_only'
            }
        })

        res = MongoDBTools.writeDatabase(collectionsData)
        self.assertListEqual(res, [
            "INF: Document already exist. Insert canceled.",
            "INF: Document already exist. Insert canceled."])


class ME_DBService_Test(FunctionalClass):
    '''
    Testing next methods of class #MongoDBTools:
    getTemplate;
    getNamesByRace;
    getPreparedRaceData;
    getIdByField;
    getLocalAnalyticDataByKeys;
    prepareToWriteNamesData;
    readNamesDBByRace;
    setChecksumGlobalDB_ME;
    fillRaceData;
    fillGlobalCountsData;
    prepareGlobalCountsData;
    fillAnalyticCountCollection;
    prepareAnalyticCountCollections;
    fillLocalChainData;
    unpackAnalyticChainData;
    fillAnalyticChainCollection;
    prepareAnalyticChainCollection;
    
    writeGendersDB_ME;
    readBaseOfNamesDB_ME;
    writeBaseOfNamesDB_ME;
    readChecksumDB_ME;
    writeChecksumDB_ME;
    writeAnalyticsDB_ME.
    '''

    ##BEGIN ConstantBlock
    mdb_alias = ME_SETTINGS.MDB_n_Aliases['mdbName']['alias']
    mdb_analytic_alias = ME_SETTINGS.MDB_n_Aliases['mdbAnalytic']['alias']
    mdb_checksum_alias = ME_SETTINGS.MDB_n_Aliases['mdbCheckSum']['alias']

    #tst_mdbNAliases = MongoDBTools.mdbNAliases
    #tst_getConnectString = MongoDBTools.getConnectString
    #mdb_test = 'test_db'
    #mdb_test_alias = 'test_alias'
    TestFiles = {}
    ##END ConstantBlock

    ##BEGIN PrepareBlock
    @classmethod
    def setUpClass(cls) -> typ.NoReturn:
        '''Set up for class.'''
        cls.printSetUpClassMsg()
        cls.createTestFiles()

        #Using mongomock for testing
        medb.connect('mongoenginetest', 
                host='mongomock://localhost', 
                alias=cls.mdb_alias)
        medb.connect('mongoenginetest2', 
                host='mongomock://localhost', 
                alias=cls.mdb_analytic_alias)
        medb.connect('mongoenginetest3', 
                host='mongomock://localhost', 
                alias=cls.mdb_checksum_alias)

    @classmethod
    def tearDownClass(cls) -> typ.NoReturn:
        '''Tear down for class.'''
        medb.disconnect(alias=cls.mdb_alias)
        medb.disconnect(alias=cls.mdb_analytic_alias)
        medb.disconnect(alias=cls.mdb_checksum_alias)

        cls.removeTestFiles()
        cls.printTearDownClassMsg()

    def setUp(self) -> typ.NoReturn:
        '''Set up for test.'''
        self.printSetUpMethodMsg()

        race = Race()
        race.race = 'TestRace'
        race.save()

        genderGp = GenderGroups()
        genderGp.gender_group = 'TestGender'
        genderGp.save()

        male = Male()
        male.race = race
        male.name = 'TestName'
        male.save()
        
        lettersCount = NameLettersCount()
        lettersCount.race = race.id
        lettersCount.gender_group = genderGp.id
        lettersCount.key = 3
        lettersCount.save()

        existFlag = GlobalFlags()
        existFlag.globalExist = True
        existFlag.save()

    def tearDown(self) -> typ.NoReturn:
        '''Tear down for test.'''
        #Return class data back after manipulation in tests
        #MongoDBTools.mdbNAliases = self.tst_mdbNAliases
        #MongoDBTools.getConnectString = self.tst_getConnectString
        
        GlobalCounts.drop_collection()
        #VowelsChains.drop_collection()
        #NameLettersCount.drop_collection()

        Race.drop_collection()
        GenderGroups.drop_collection()
        Male.drop_collection()
        
        GlobalFlags.drop_collection()

        #medb.disconnect(alias=self.mdb_test_alias)

        self.printTearDownMethodMsg()

    ##END PrepareBlock

    @FunctionalClass.descript
    def test_getTemplate_gettingDeepCopy_expectedSeparateDict(
            self) -> typ.NoReturn:
        '''
        Testing the method of gets fast deepcopy of template.
        '''
        data = dict({'test_key': 1})
        template = dict({
            'SomeTemplate': {
                'some_list': list(),
                'some_dict': {'data': data}}
        })

        res = ME_DBService().getTemplate(template)
        data['test_key'] = 3

        self.assertDictEqual(res, { 'SomeTemplate': {
                                        'some_list': [],
                                        'some_dict': {
                                            'data': {'test_key': 1}
                                        }}})

    @FunctionalClass.descript
    def test_getNamesByRace_gettingDeepCopy_expectedSeparateDict(
            self) -> typ.NoReturn:
        '''
        Testing the method of gets fast deepcopy of template.
        '''
        race = Race.objects(race='TestRace').first()

        res = ME_DBService().getNamesByRace(race, Male)
        self.assertListEqual(res, ['TestName'])

    @FunctionalClass.descript
    def test_getPreparedRaceData_preparingTemplate_expectedCorrectTemplate(
            self) -> typ.NoReturn:
        '''
        Testing the method of prepairs template by current race.
        '''
        race = Race.objects(race='TestRace').first()

        res = ME_DBService().getPreparedRaceData(race)
        self.assertDictEqual(res, {"TestRace": {
                                    "Genders": {
                                        "Female": {"Names": []}, 
                                        "Male": {"Names": []}},
                                    "Surnames": []
                                    }})

    @FunctionalClass.descript
    def test_getIdByField_gettingDocID_expectedDocID(
            self) -> typ.NoReturn:
        '''
        Testing the method of gets id by field from collection.
        '''
        race = Race.objects(race='TestRace').first()

        res = ME_DBService.getIdByField(Male, 'race', 'TestRace')
        self.assertEqual(res, race.id)

    @FunctionalClass.descript
    def test_getLocalAnalyticDataByKeys_readingData_expectedDict(
            self) -> typ.NoReturn:
        '''
        Testing the method of reads analytic data 
        from collection by target keys.
        '''
        race = Race.objects(race='TestRace').first()
        gender = GenderGroups.objects(gender_group='TestGender').first()

        res = ME_DBService.getLocalAnalyticDataByKeys(NameLettersCount, 
                                            'TestRace', 'TestGender')
        for r in res:
            _ = r.pop('_id')
            _ = r.pop('_cls')

        self.assertListEqual(res, [{'race': {'$oid': str(race.id)},
                                    'gender_group': {'$oid': str(gender.id)},
                                    'key': 3,
                                    'count': 0,
                                    'chance': 0.0}])

    @FunctionalClass.descript
    def test_prepareToWriteNamesData_preparingData_expectedAdaptedData(
            self) -> typ.NoReturn:
        '''
        Testing the method of adapts the names database 
        to the mongoengine schema.
        '''
        race = 'TestRace'
        data = list([
            'TestName1',
            'TestName2'
        ])

        res = ME_DBService().prepareToWriteNamesData(race, data)

        self.assertListEqual(res, [{'name': 'TestName1', 'race': 'TestRace'},
                                    {'name': 'TestName2', 'race': 'TestRace'}])

    @FunctionalClass.descript
    def test_readNamesDBByRace_readingData_expectedGroupedData(
            self) -> typ.NoReturn:
        '''
        Testing the method of reading the base of names.
        '''
        race = Race.objects(race='TestRace').first()

        res = ME_DBService().readNamesDBByRace(race)
        self.assertDictEqual(res, {'Male': ['TestName'], 
                                    'Female': [], 'Surnames': []})

    @FunctionalClass.descript
    def test_setChecksumGlobalDB_ME_settingFlag_expectedRightValue(
            self) -> typ.NoReturn:
        '''
        Testing the method of sets the global exist flag.
        '''
        _ = ME_DBService().setChecksumGlobalDB_ME(False)
        res = GlobalFlags.objects.first()
        
        self.assertFalse(res.globalExist)

    @FunctionalClass.descript
    def test_fillRaceData_fillingTemplate_expectedFilledTemplate(
            self) -> typ.NoReturn:
        '''
        Testing the method of populates a prepared race template 
        with names data for analytic module.
        '''
        race = Race.objects(race='TestRace').first()
        namesTemplate = {"TestRace": {
                            "Genders": {
                                "Female": {"Names": []}, 
                                "Male": {"Names": []}},
                            "Surnames": []
                            }}

        res = ME_DBService().fillRaceData(race, namesTemplate)
        self.assertDictEqual(res, {"TestRace": {
                                    "Genders": {
                                        "Female": {"Names": []}, 
                                        "Male": {"Names": ['TestName']}},
                                    "Surnames": []
                                    }})

    @FunctionalClass.descript
    def test_fillGlobalCountsData_adaptingData_expectedFilledSchema(
            self) -> typ.NoReturn:
        '''
        Testing the method of adapts the global counts data 
        to the mongoengine schema.
        '''
        race = 'TestRace'
        analyticData = {
            'Max_Names_Count': 1,
            'Male_Names_Count': 2,
            'Female_Names_Count': 3,
            'Surnames_Count': 4,
            "First_Letters": {
                "Vowels_Count": 5,
                "Consonants_Count": 6,}
        }

        res = ME_DBService().fillGlobalCountsData(race, analyticData)
        self.assertListEqual(res, [{'race': 'TestRace', 
                                    'maxNamesCount': 1,
                                    'maleNamesCount': 2,
                                    'femaleNamesCount': 3,
                                    'surnamesCount': 4,
                                    'firstLettersCounts': {
                                        'vowelsCount': 5,
                                        'consonantsCount': 6}
                                    }])

    @FunctionalClass.descript
    def test_prepareGlobalCountsData_preparingData_expectedCorrectData(
            self) -> typ.NoReturn:
        '''
        Testing the method of prepares and arranges 
        the global counts data for writing.
        '''
        race = 'TestRace'
        analyticData = {
            'Max_Names_Count': 1,
            'Male_Names_Count': 2,
            'Female_Names_Count': 3,
            'Surnames_Count': 4,
            "First_Letters": {
                "Vowels_Count": 5,
                "Consonants_Count": 6,}
        }

        res = ME_DBService().prepareGlobalCountsData(race, analyticData)
        self.assertDictEqual(res, { 'GlobalCounts': {
                                        'collection': GlobalCounts,
                                        'data': [{'race': 'TestRace', 
                                                'maxNamesCount': 1,
                                                'maleNamesCount': 2,
                                                'femaleNamesCount': 3,
                                                'surnamesCount': 4,
                                                'firstLettersCounts': {
                                                    'vowelsCount': 5,
                                                    'consonantsCount': 6}
                                                }],
                                        'operation': 'update_or_insert'
                                    }})

    @FunctionalClass.descript
    def test_fillAnalyticCountCollection_adaptingData_expectedFilledSchema(
            self) -> typ.NoReturn:
        '''
        Testing the method of adapts the analytic counts data.
        '''
        race = 'TestRace'
        analyticData = {
            'Name_Letters_Count': {
                'TestGender': {
                    3: {'Count': 3, 'Chance': 3.3}
                }}
        }

        res = ME_DBService().fillAnalyticCountCollection(race, 
                            analyticData, 'Name_Letters_Count')
        self.assertListEqual(res, [{'race': 'TestRace', 
                                    'gender_group': 'TestGender',
                                    'key': 3,
                                    'count': 3,
                                    'chance': 3.3}])

    @FunctionalClass.descript
    def test_prepareAnalyticCountCollections_preparingData_expectedCorrectData(
            self) -> typ.NoReturn:
        '''
        Testing the method of prepares and arranges 
        the analytic counts data for writing.   
        '''
        race = 'TestRace'
        analyticData = {
            'Name_Letters_Count': {
                'TestGender': {
                    3: {'Count': 3, 'Chance': 3.3}
                }},
            'First_Letters': {
                'TestGender': {
                    'a': {'Count': 1, 'Chance': 1.1}
                }}
        }

        res = ME_DBService().prepareAnalyticCountCollections(race, 
                                                analyticData)
        self.assertDictEqual(res,  { 'NameLettersCount': {
                                        'collection': NameLettersCount,
                                        'data': [{'race': 'TestRace', 
                                                'gender_group': 'TestGender',
                                                'key': 3,
                                                'count': 3,
                                                'chance': 3.3}],
                                        'operation': 'update_or_insert'
                                    },
                                    'FirstLetters': {
                                        'collection': FirstLetters,
                                        'data': [{'race': 'TestRace', 
                                                'gender_group': 'TestGender',
                                                'key': 'a',
                                                'count': 1,
                                                'chance': 1.1}],
                                        'operation': 'update_or_insert'
                                    }})

    @FunctionalClass.descript
    def test_fillLocalChainData_adaptingData_expectedFilledSchema(
            self) -> typ.NoReturn:
        '''
        Testing the method of adapts the analytic chain data.
        '''
        genderAnalyticData = {1: {'Count': 1, 'Chance': 1.1}}

        res = ME_DBService().fillLocalChainData(genderAnalyticData)
        self.assertListEqual(res, [{'key': 1,
                                    'count': 1,
                                    'chance': 1.1}])

    @FunctionalClass.descript
    def test_fillLocalChainData_adaptingData_expectedFilledLengthCountSchema(
            self) -> typ.NoReturn:
        '''
        Testing the method of adapts the local analytic chain data.
        '''
        genderAnalyticData = {'1_1': {'Max_Count_In_Name': 1, 
                                    'Names_Count': 1, 'Chance': 1.1}}

        res = ME_DBService().fillLocalChainData(genderAnalyticData)
        self.assertListEqual(res, [{'length': 1, 
                                    'maxCountInName': 1, 
                                    'namesCount': 1, 
                                    'chance': 1.1}])

    @FunctionalClass.descript
    def test_unpackAnalyticChainData_adaptingData_expectedPreparedData(
            self) -> typ.NoReturn:
        '''
        Testing the method of unpacks the gender groups data 
        from analytic subkeys.
        '''
        analyticData = {
            'Chain_Frequency': {
                'TestGender': {
                    1: {'Count': 1, 'Chance': 1.1}
                }}, 
            'Length_Count_Names': {
                'TestGender': {
                    '1_1': {'Max_Count_In_Name': 1, 
                            'Names_Count': 1, 'Chance': 1.1}
                }}}
        

        res = ME_DBService().unpackAnalyticChainData(analyticData)
        self.assertDictEqual(res, {'TestGender': {
                                        'Chain_Frequency': [
                                            {'key': 1,
                                            'count': 1,
                                            'chance': 1.1}],
                                        'Length_Count_Names': [
                                            {'length': 1, 
                                            'maxCountInName': 1, 
                                            'namesCount': 1, 
                                            'chance': 1.1}]
                                    }})

    @FunctionalClass.descript
    def test_fillAnalyticChainCollection_adaptingData_expectedPreparedData(
            self) -> typ.NoReturn:
        '''
        Testing the method of adapts the analytic chain data.
        '''
        race = 'TestRace'
        unpackedData = {
            'TestGender': {
                'Chains': [],
                'Chain_Frequency': [
                    {'key': 1,
                    'count': 1,
                    'chance': 1.1}],
                'Length_Count_Names': [
                    {'length': 1, 
                    'maxCountInName': 1, 
                    'namesCount': 1, 
                    'chance': 1.1}]
            }}

        res = ME_DBService().fillAnalyticChainCollection(race, unpackedData)
        self.assertListEqual(res, [{'race': 'TestRace',
                                    'gender_group': 'TestGender',
                                    'chains': [],
                                    'chainFrequency': [
                                        {'key': 1,
                                        'count': 1,
                                        'chance': 1.1}],
                                    'lengthCountNames': [
                                        {'length': 1, 
                                        'maxCountInName': 1, 
                                        'namesCount': 1, 
                                        'chance': 1.1}]
                                   }])

    @FunctionalClass.descript
    def test_prepareAnalyticChainCollection_preparingData_expectedCorrectData(
            self) -> typ.NoReturn:
        '''
        Testing the method of prepares and arranges 
        the analytic chain data for writing.
        '''
        race = 'TestRace'
        analyticData = {
            'Vowels_Chains':{
                'Chains': {'TestGender': {}},
                'Chain_Frequency': {
                    'TestGender': {
                        1: {'Count': 1, 'Chance': 1.1}
                    }}, 
                'Length_Count_Names': {
                    'TestGender': {
                        '1_1': {'Max_Count_In_Name': 1, 
                                'Names_Count': 1, 'Chance': 1.1}
                    }}
            }}

        res = ME_DBService().prepareAnalyticChainCollection(race, 
                                                    analyticData)
        self.assertDictEqual(res, { 'VowelsChains': {
                                        'collection': VowelsChains,
                                        'data': [{'race': 'TestRace',
                                                'gender_group': 'TestGender',
                                                'chains': [],
                                                'chainFrequency': [
                                                    {'key': 1,
                                                    'count': 1,
                                                    'chance': 1.1}],
                                                'lengthCountNames': [
                                                    {'length': 1, 
                                                    'maxCountInName': 1, 
                                                    'namesCount': 1, 
                                                    'chance': 1.1}]}],
                                        'operation': 'update_or_insert'
                                    }})
                            
###FINISH FunctionalBlock

###START MainBlock
def main() -> typ.NoReturn:
    pass
###FINISH Mainblock
