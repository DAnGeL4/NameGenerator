###START ImportBlock
##systemImport
import typing as typ
import mongoengine as medb

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


class ME_DBService_Test(FunctionalClass):
    pass
                            
###FINISH FunctionalBlock

###START MainBlock
def main() -> typ.NoReturn:
    pass
###FINISH Mainblock
