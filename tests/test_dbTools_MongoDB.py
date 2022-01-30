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
from modules.dbTools import MongoDBTools

from tests.test_Service import FunctionalClass

#from database.medbCheckSumSchemas import GlobalFlags
#from database.medbCheckSumSchemas import ChecksumFiles

from database.medbNameSchemas import Race, GenderGroups
from database.medbNameSchemas import Male, Female, Surnames

from database.medbAnalyticSchemas import GlobalCounts, VowelsChains
from database.medbAnalyticSchemas import FirstLettersCounts

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

        Race.drop_collection()
        GenderGroups.drop_collection()
        Male.drop_collection()
        Female.drop_collection()
        Surnames.drop_collection()

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
        doc = MongoDBTools.insertEmbeddedField(doc, collection, field, data)

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
        doc = MongoDBTools.insertEmbeddedField(doc, collection, field, data)

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
        doc = MongoDBTools.insertField(doc, collection, field, data)

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
        doc = MongoDBTools.insertField(doc, collection, field, data)

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
        doc = MongoDBTools.insertField(doc, collection, field, data)

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

        self.assertEqual(res, "INF: Document already exist. Insert canceled")

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


class ME_DBService_Test(FunctionalClass):
    pass
                            
###FINISH FunctionalBlock

###START MainBlock
def main() -> typ.NoReturn:
    pass
###FINISH Mainblock
